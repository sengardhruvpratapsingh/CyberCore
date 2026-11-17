from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta
import os


MAX_RISK_SCORE = 10
DISPLAY_SCORE_DENOMINATOR = 10
HIGH_VALUE_THRESHOLD = float(
    os.getenv("CYBERCORE_HIGH_VALUE_THRESHOLD", "20000")
)


@dataclass(frozen=True)
class RiskScoringConfig:
    high_value_threshold: float = HIGH_VALUE_THRESHOLD


def get_risk_level(score: int) -> str:
    if score <= 3:
        return "LOW"

    if score <= 6:
        return "MEDIUM"

    return "HIGH"


def _signal(name, points, evidence_refs):
    return {
        "name": name,
        "points": points,
        "evidence_refs": sorted(set(evidence_refs))
    }


def _transaction_ref(transaction):
    return str(transaction.transaction_id)


def _rapid_routing_refs(transactions, window):
    ordered = sorted(transactions, key=lambda item: item.timestamp)
    refs = []

    for previous_index, previous in enumerate(ordered):
        for current in ordered[previous_index + 1:]:
            interval = current.timestamp - previous.timestamp
            if interval > window:
                break
            if previous.receiver == current.sender:
                refs.extend([
                    _transaction_ref(previous),
                    _transaction_ref(current)
                ])

    return refs


def _fan_out_refs(transactions, receiver_threshold):
    receiver_refs = defaultdict(list)

    for transaction in transactions:
        receiver_refs[transaction.sender].append(transaction)

    refs = []
    for sender_transactions in receiver_refs.values():
        receivers = {transaction.receiver for transaction in sender_transactions}
        if len(receivers) >= receiver_threshold:
            refs.extend(
                _transaction_ref(transaction)
                for transaction in sender_transactions
            )

    return refs


def _cross_evidence_refs(transactions, device_records, email_artifacts):
    transaction_entities = {
        str(entity).lower()
        for transaction in transactions
        for entity in (transaction.sender, transaction.receiver)
    }
    device_entities = {
        str(record.phone_number).lower()
        for record in device_records
    }
    email_entities = {
        str(address).lower()
        for artifact in email_artifacts
        for address in (artifact.from_address, artifact.reply_to)
        if address
    }

    refs = []
    if transaction_entities & device_entities:
        refs.extend(sorted(transaction_entities & device_entities))
    if transaction_entities & email_entities:
        refs.extend(sorted(transaction_entities & email_entities))

    return refs


def calculate_risk_assessment(
    transactions=None,
    transaction_chains=None,
    high_value_transactions=None,
    **_ignored
):
    """Apply the original count-based rule with a compatible response shape."""
    chain_count = (
        transaction_chains
        if isinstance(transaction_chains, int)
        else len(transaction_chains or [])
    )
    high_value_count = (
        high_value_transactions
        if isinstance(high_value_transactions, int)
        else len(high_value_transactions or [])
    )
    score = calculate_risk_score(chain_count, high_value_count)
    signals = []

    if chain_count >= 1:
        signals.append(_signal(
            "Transaction chains",
            2,
            [
                str(transaction_id)
                for chain in (transaction_chains or [])
                if isinstance(chain, dict)
                for transaction_id in chain.get("transaction_ids", [])
            ]
        ))

    if chain_count >= 3:
        signals.append(_signal(
            "Three or more transaction chains",
            2,
            []
        ))

    if high_value_count >= 1:
        signals.append(_signal(
            "High-value transactions",
            2,
            [
                str(transaction.transaction_id)
                for transaction in (high_value_transactions or [])
                if hasattr(transaction, "transaction_id")
            ]
        ))

    if high_value_count >= 3:
        signals.append(_signal(
            "Three or more high-value transactions",
            2,
            []
        ))

    return {
        "score": score,
        "level": get_risk_level(score),
        "signals": signals,
        "maximum": MAX_RISK_SCORE,
        "display_denominator": DISPLAY_SCORE_DENOMINATOR
    }


def calculate_risk_score(
    transaction_chains: int,
    high_value_transactions: int
) -> int:
    """Apply the original deterministic count-based risk rule."""
    score = 1
    if transaction_chains >= 1:
        score += 2
    if transaction_chains >= 3:
        score += 2
    if high_value_transactions >= 1:
        score += 2
    if high_value_transactions >= 3:
        score += 2

    return min(score, MAX_RISK_SCORE)