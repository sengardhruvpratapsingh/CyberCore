"""Grounded Copilot with a local SLM selector and deterministic execution.

Every answer is produced by calling one of a fixed set of
tool functions against the case's real, already-computed
evidence. Nothing is invented: if no tool matches the
question, the Copilot says so instead of guessing.
"""

from datetime import date, datetime
from decimal import Decimal

from pydantic import ValidationError

from app.forensic.case_brief import generate_case_brief
from app.forensic.slm import SLMSelectionError, select_tool, slm_enabled, slm_model
from app.forensic.timeline import build_case_timeline
from app.schemas.copilot import (
    ConnectedEntityArguments,
    EntityArguments,
    StrictArguments,
    ToolSelection,
    TransactionArguments,
)


def tool_get_risk_findings(data):
    signals = data.get("risk_signals", [])
    signal_summary = ", ".join(
        f"{signal['name']} (+{signal['points']})"
        for signal in signals
    ) or "no verified risk signals"

    return {
        "tool": "get_risk_findings",
        "answer": (
            f"This case has a risk score of "
            f"{data['risk_score']}/10 "
            f"({data['risk_level']}), based on: "
            f"{signal_summary}."
        ),
        "grounded_on": {
            "risk_score": data["risk_score"],
            "risk_level": data["risk_level"],
            "risk_signals": signals
        }
    }


def tool_get_fund_paths(data):

    chains = data["chains"]

    if not chains:
        answer = (
            "No suspicious multi-hop transaction chains "
            "were found in this case's evidence."
        )
    else:
        first = chains[0]

        answer = (
            f"{len(chains)} suspicious transaction chain(s) "
            "were found. Example: "
            + " -> ".join(first["path"])
            + f" completed within {first['duration_hours']}h."
        )

    return {
        "tool": "get_fund_paths",
        "answer": answer,
        "grounded_on": chains
    }


def tool_get_high_value_transactions(data):

    high_value = data["high_value"]

    if not high_value:
        answer = (
            "No transactions above the high-value threshold "
            "were found in this case's evidence."
        )
    else:
        answer = (
            f"{len(high_value)} high-value transaction(s) "
            "were found, the largest being "
            f"{max(t.amount for t in high_value)}."
        )

    return {
        "tool": "get_high_value_transactions",
        "answer": answer,
        "grounded_on": high_value
    }


def tool_get_connected_entities(data):

    shared_devices = data["shared_devices"]

    if not shared_devices:
        answer = (
            "No shared-device associations were found in "
            "this case's evidence."
        )
    else:
        finding = shared_devices[0]

        answer = (
            f"{len(shared_devices)} shared-device "
            "association(s) were found. Example: IMEI "
            f"{finding['imei']} was observed with "
            f"{len(finding['phone_numbers'])} different "
            "phone numbers. This is an observed "
            "association, not proof of shared identity."
        )

    return {
        "tool": "get_connected_entities",
        "answer": answer,
        "grounded_on": shared_devices
    }


def tool_get_email_findings(data):

    email_findings = data["email_findings"]

    if not email_findings:
        answer = (
            "No From/Reply-To header mismatches were found "
            "in this case's email evidence."
        )
    else:
        answer = (
            f"{len(email_findings)} email header mismatch(es) "
            "were found. This does not confirm spoofing on "
            "its own - it is an observed inconsistency only."
        )

    return {
        "tool": "get_email_findings",
        "answer": answer,
        "grounded_on": email_findings
    }


# Keyword -> tool routing table. Checked in order; the first
# matching keyword set wins.
ROUTING_TABLE = [
    (
        ["risk", "score"],
        tool_get_risk_findings
    ),
    (
        ["chain", "mule", "route", "hop", "fund path"],
        tool_get_fund_paths
    ),
    (
        ["high value", "high-value", "large transaction",
         "biggest", "largest"],
        tool_get_high_value_transactions
    ),
    (
        ["device", "imei", "phone", "sim"],
        tool_get_connected_entities
    ),
    (
        ["email", "spoof", "reply-to", "reply to"],
        tool_get_email_findings
    )
]


DECLINE_ANSWER = (
    "I can't answer that from this case's evidence. I can "
    "answer questions about the risk score, transaction "
    "chains, high-value transactions, shared devices, and "
    "email header findings."
)


def answer_question(question, data):
    """
    Route a question to the first matching tool. If nothing
    matches, decline instead of guessing.
    """

    lowered_question = question.lower()

    for keywords, tool in ROUTING_TABLE:

        if any(
            keyword in lowered_question
            for keyword in keywords
        ):
            return tool(data)

    return {
        "tool": None,
        "answer": DECLINE_ANSWER,
        "grounded_on": None
    }


TOOL_ARGUMENT_MODELS = {
    "find_entity": EntityArguments,
    "get_transactions": TransactionArguments,
    "get_connected_entities": ConnectedEntityArguments,
    "get_fund_paths": StrictArguments,
    "get_risk_findings": StrictArguments,
    "get_timeline": StrictArguments,
    "generate_case_brief": StrictArguments,
    "get_email_findings": StrictArguments,
}


def validate_tool_selection(selection):
    """Validate both the tool name and its exact argument shape."""
    if isinstance(selection, ToolSelection):
        selection = selection.model_dump()
    validated = ToolSelection.model_validate(selection)
    arguments = TOOL_ARGUMENT_MODELS[validated.tool].model_validate(
        validated.arguments
    )
    return validated.tool, arguments.model_dump(exclude_none=True)


def _jsonable(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "__dict__"):
        return {
            key: _jsonable(item)
            for key, item in vars(value).items()
            if not key.startswith("_")
        }
    return value


def _matches_entity(entity_type, entity_value, record):
    key = entity_type.lower().replace(" ", "_")
    field_map = {
        "imei": "imei",
        "device": "imei",
        "phone": "phone_number",
        "phone_number": "phone_number",
        "account": "sender",
        "email": "from_address",
    }
    field = field_map.get(key)
    if field and hasattr(record, field):
        return str(getattr(record, field)) == entity_value
    return entity_value in {
        str(getattr(record, field, ""))
        for field in ("sender", "receiver", "phone_number", "imei", "from_address", "to_address", "reply_to")
    }


def _tool_find_entity(arguments, data):
    matches = []
    for source, records in (
        ("transactions", data["transactions"]),
        ("device records", data["device_records"]),
        ("email artifacts", data["email_artifacts"]),
    ):
        for record in records:
            if _matches_entity(arguments["entity_type"], arguments["entity_value"], record):
                matches.append({"source": source, "record": _jsonable(record)})
    return {"match_count": len(matches), "matches": matches, "evidence_refs": [item["source"] for item in matches]}


def _tool_get_transactions(arguments, data):
    records = data["transactions"]
    if arguments.get("high_value_only"):
        records = data["high_value"]
    if arguments.get("min_amount") is not None:
        records = [item for item in records if float(item.amount) >= arguments["min_amount"]]
    if arguments.get("transaction_id"):
        records = [item for item in records if item.transaction_id == arguments["transaction_id"]]
    if arguments.get("entity_value"):
        records = [item for item in records if _matches_entity(arguments.get("entity_type") or "entity", arguments["entity_value"], item)]
    return {"transaction_count": len(records), "transactions": _jsonable(records), "evidence_refs": ["transactions"]}


def _tool_get_connected_entities(arguments, data):
    findings = data["shared_devices"]
    entity_value = arguments.get("entity_value")
    if entity_value:
        records = [item for item in data["device_records"] if _matches_entity(arguments["entity_type"], entity_value, item)]
        entities = sorted({item.phone_number if arguments["entity_type"].lower() == "imei" else item.imei for item in records})
        return {"connection_count": len(entities), "entities": entities, "relationships": _jsonable(records), "evidence_refs": ["device records"]}
    return {"connection_count": len(findings), "entities": _jsonable(findings), "evidence_refs": ["device records"]}


def execute_tool(tool, arguments, data, case=None):
    """Execute only a validated, registered forensic tool."""
    tool, arguments = validate_tool_selection({"tool": tool, "arguments": arguments})
    if tool == "find_entity":
        return _tool_find_entity(arguments, data)
    if tool == "get_transactions":
        return _tool_get_transactions(arguments, data)
    if tool == "get_connected_entities":
        return _tool_get_connected_entities(arguments, data)
    if tool == "get_fund_paths":
        return {"chain_count": len(data["chains"]), "chains": _jsonable(data["chains"]), "evidence_refs": ["transactions"]}
    if tool == "get_risk_findings":
        return {"risk_score": data["risk_score"], "risk_level": data["risk_level"], "signals": _jsonable(data["risk_signals"]), "evidence_refs": ["risk assessment"]}
    if tool == "get_timeline":
        events = build_case_timeline(data["transactions"], data["device_records"], data["email_artifacts"])
        return {"event_count": len(events), "events": _jsonable(events), "evidence_refs": ["transactions", "device records", "email artifacts"]}
    if tool == "generate_case_brief":
        if case is None:
            raise ValueError("Case is required for generate_case_brief")
        result = generate_case_brief(
            case=case,
            transactions=data["transactions"],
            device_records=data["device_records"],
            email_artifacts=data["email_artifacts"],
            transaction_chains=data["chains"],
            high_value_transactions=data["high_value"],
            shared_device_findings=data["shared_devices"],
            email_findings=data["email_findings"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            risk_signals=data["risk_signals"],
            risk_score_maximum=data["risk_score_maximum"],
            risk_score_display_denominator=data["risk_score_display_denominator"],
        )
        result = _jsonable(result)
        result["evidence_refs"] = ["case brief"]
        return result
    return {"finding_count": len(data["email_findings"]), "findings": _jsonable(data["email_findings"]), "evidence_refs": ["email artifacts"]}


def _fallback_selection(question):
    lowered = question.lower()
    if any(keyword in lowered for keyword in ("risk", "score")):
        return "get_risk_findings", {}
    if any(keyword in lowered for keyword in ("chain", "mule", "route", "hop", "fund path")):
        return "get_fund_paths", {}
    if any(keyword in lowered for keyword in ("high value", "high-value", "large transaction", "biggest", "largest")):
        return "get_transactions", {"high_value_only": True}
    if any(keyword in lowered for keyword in ("device", "imei", "phone", "sim")):
        return "get_connected_entities", {}
    if any(keyword in lowered for keyword in ("email", "spoof", "reply-to", "reply to")):
        return "get_email_findings", {}
    return None, {}


def _grounded_answer(tool, result):
    if tool == "get_risk_findings":
        signals = ", ".join(f"{item['name']} (+{item['points']})" for item in result["signals"]) or "no verified risk signals"
        return (
            f"The observed risk score is {result['risk_score']}/10 "
            f"({result['risk_level']}). The verified signals are: {signals}. "
            "This is an investigative finding from the analyzed evidence, "
            "not a conclusion about a person."
        )
    if tool == "get_connected_entities":
        entities = result.get("entities", [])
        details = ", ".join(str(item) for item in entities[:8])
        suffix = "" if len(entities) <= 8 else f" and {len(entities) - 8} more"
        return (
            f"The evidence shows {result['connection_count']} observed connected "
            f"entit{'y' if result['connection_count'] == 1 else 'ies'}. "
            f"Returned entities: {details or 'none'}{suffix}. "
            "These are observed relationships and do not prove shared identity or intent."
        )
    if tool == "get_transactions":
        transactions = result.get("transactions", [])
        details = "; ".join(
            f"{item.get('transaction_id', 'unknown')} from "
            f"{item.get('sender', 'unknown')} to {item.get('receiver', 'unknown')} "
            f"for {item.get('amount', 'unknown')} at {item.get('timestamp', 'unknown')}"
            for item in transactions[:5]
        )
        suffix = "" if len(transactions) <= 5 else f"; plus {len(transactions) - 5} more"
        return (
            f"The evidence contains {result['transaction_count']} matching transaction(s). "
            f"Observed details: {details or 'none'}{suffix}."
        )
    if tool == "get_fund_paths":
        chains = result.get("chains", [])
        details = "; ".join(
            f"{' -> '.join(map(str, chain.get('path', [])))} "
            f"over {chain.get('duration_hours', 'unknown')} hours "
            f"(transactions: {', '.join(map(str, chain.get('transaction_ids', [])))})"
            for chain in chains[:3]
        )
        suffix = "" if len(chains) <= 3 else f"; plus {len(chains) - 3} more"
        return (
            f"The evidence contains {result['chain_count']} observed transaction chain(s). "
            f"Observed paths: {details or 'none'}{suffix}."
        )
    if tool == "get_timeline":
        events = result.get("events", [])
        details = "; ".join(
            f"{event.get('timestamp', 'unknown')}: {event.get('summary', event.get('description', 'event'))}"
            for event in events[:5]
        )
        suffix = "" if len(events) <= 5 else f"; plus {len(events) - 5} more"
        return (
            f"The evidence contains {result['event_count']} chronological event(s). "
            f"Observed timeline: {details or 'none'}{suffix}."
        )
    if tool == "find_entity":
        matches = result.get("matches", [])
        details = "; ".join(
            f"{item.get('source', 'unknown source')}: "
            f"{_summarize_record(item.get('record', {}))}"
            for item in matches[:5]
        )
        suffix = "" if len(matches) <= 5 else f"; plus {len(matches) - 5} more"
        return (
            f"The evidence contains {result['match_count']} matching record(s) "
            f"for the requested entity. Observed records: {details or 'none'}{suffix}."
        )
    if tool == "get_email_findings":
        findings = result.get("findings", [])
        details = "; ".join(
            _summarize_record(finding) for finding in findings[:5]
        )
        suffix = "" if len(findings) <= 5 else f"; plus {len(findings) - 5} more"
        return (
            f"The evidence contains {result['finding_count']} observed email finding(s). "
            f"Observed details: {details or 'none'}{suffix}."
        )
    return "A verified case brief was generated from the analyzed evidence."


def _summarize_record(record):
    if not isinstance(record, dict):
        return str(record)
    excluded = {"id", "case_id"}
    return ", ".join(
        f"{key.replace('_', ' ')}={value}"
        for key, value in record.items()
        if key not in excluded and value not in (None, "")
    ) or "no additional fields"


def answer_with_router(question, data, case=None):
    mode = "slm"
    limitations = []
    try:
        selection = select_tool(question)
        tool, arguments = validate_tool_selection(selection)
    except (SLMSelectionError, ValidationError, ValueError) as error:
        mode = "fallback"
        limitations.append("Local SLM selection was unavailable or invalid; deterministic routing was used.")
        tool, arguments = _fallback_selection(question)

    if tool is None:
        return {
            "answer": DECLINE_ANSWER,
            "mode": mode,
            "tool": None,
            "arguments": {},
            "result": {},
            "grounded_on": [],
            "limitations": limitations + ["The question is outside the available forensic tools."],
        }

    result = execute_tool(tool, arguments, data, case=case)
    return {
        "answer": _grounded_answer(tool, result),
        "mode": mode,
        "tool": tool,
        "arguments": arguments,
        "result": result,
        "grounded_on": result.get("evidence_refs", []),
        "limitations": limitations,
    }


def copilot_status():
    return {
        "slm_enabled": slm_enabled(),
        "model": slm_model(),
        "tools": list(TOOL_ARGUMENT_MODELS),
        "fallback_available": True,
    }
