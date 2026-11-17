"""Small, local-only Ollama adapter for Copilot tool selection."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.schemas.copilot import ToolSelection


class SLMSelectionError(RuntimeError):
    """Raised when the local model cannot produce a valid tool selection."""


def slm_enabled():
    return os.getenv("CYBERCORE_SLM_ENABLED", "true").lower() in {
        "1", "true", "yes", "on"
    }


def slm_model():
    return os.getenv("CYBERCORE_SLM_MODEL", "qwen3.5:9b-q4_K_M")


def ollama_base_url():
    return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").rstrip("/")


def _selection_prompt():
    return (
        "You select exactly one approved forensic tool for the investigator question. "
        "Return JSON only with exactly these keys: tool and arguments. "
        "Never calculate risk, infer evidence, invent identifiers, or answer the question. "
        "Use {} when a tool needs no arguments. Approved tools and arguments are: "
        "find_entity requires entity_type and entity_value; "
        "get_transactions accepts optional entity_type, entity_value, transaction_id, "
        "high_value_only, and min_amount; "
        "get_connected_entities requires entity_type and entity_value; "
        "get_fund_paths accepts {}; get_risk_findings accepts {}; get_timeline accepts {}; "
        "generate_case_brief accepts {}; get_email_findings accepts {}."
    )


def _extract_content(payload):
    if not isinstance(payload, dict):
        raise SLMSelectionError("Ollama returned an invalid response")

    message = payload.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if content is None:
        content = payload.get("response")
    if not isinstance(content, str) or not content.strip():
        raise SLMSelectionError("Ollama returned no JSON content")
    return content


def select_tool(question):
    if not slm_enabled():
        raise SLMSelectionError("Local SLM is disabled")

    request_body = json.dumps({
        "model": slm_model(),
        "stream": False,
        "format": "json",
        "think": False,
        "keep_alive": "10m",
        "options": {"temperature": 0},
        "messages": [
            {"role": "system", "content": _selection_prompt()},
            {"role": "user", "content": question},
        ],
    }).encode("utf-8")
    request = Request(
        f"{ollama_base_url()}/api/chat",
        data=request_body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        timeout = float(os.getenv("CYBERCORE_SLM_TIMEOUT_SECONDS", "60"))
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, OSError, ValueError) as error:
        raise SLMSelectionError(f"Ollama request failed: {error}") from error

    try:
        selection = json.loads(_extract_content(payload))
        return ToolSelection.model_validate(selection)
    except (TypeError, ValueError) as error:
        raise SLMSelectionError("Ollama returned malformed tool JSON") from error