from email.utils import parseaddr

import networkx as nx


def _normalize_email_address(value):
    if not value:
        return None

    _, email = parseaddr(str(value))
    return email.lower() if email else None


def build_unified_graph(
    transactions,
    device_records,
    email_artifacts
):
    """
    Combine financial, device and email evidence into one
    graph. Every edge is tagged with a "kind" so the caller
    can tell which evidence type produced it - the graph
    links entities, it does not merge evidence types into
    an unlabelled blob.
    """

    graph = nx.MultiDiGraph()

    # --------------------------------
    # Financial edges: sender -> receiver
    # --------------------------------

    for transaction in transactions:

        graph.add_edge(
            transaction.sender,
            transaction.receiver,
            kind="financial",
            transaction_id=transaction.transaction_id,
            amount=transaction.amount,
            timestamp=transaction.timestamp
        )

    # --------------------------------
    # Device edges: every phone number sharing an IMEI
    # is connected to that IMEI as a hub node
    # --------------------------------

    imei_to_numbers = {}

    for record in device_records:

        imei_to_numbers.setdefault(
            record.imei,
            set()
        ).add(record.phone_number)

    for imei, numbers in imei_to_numbers.items():

        if len(numbers) > 1:

            for number in numbers:

                graph.add_edge(
                    number,
                    imei,
                    kind="device"
                )

    # --------------------------------
    # Email edges: from -> reply-to, only when they differ
    # --------------------------------

    from app.forensic.email_analysis import find_email_findings

    for finding in find_email_findings(email_artifacts):
        from_email = _normalize_email_address(finding.get("from_address"))
        reply_to_email = _normalize_email_address(finding.get("reply_to"))

        if not from_email or not reply_to_email:
            continue

        graph.add_edge(
            from_email,
            reply_to_email,
            kind="email",
            message_id=finding["message_id"]
        )

    return graph


def serialize_unified_graph(graph):
    """
    Convert the NetworkX graph into a plain node/edge JSON
    shape for the API and any future frontend visualizer.
    """

    nodes = [
        {"id": node}
        for node in graph.nodes()
    ]

    edges = []

    for source, target, data in graph.edges(data=True):

        edge = {
            "source": source,
            "target": target,
            "kind": data.get("kind")
        }

        if "amount" in data:
            edge["amount"] = data["amount"]

        if "transaction_id" in data:
            edge["transaction_id"] = data["transaction_id"]

        if "message_id" in data:
            edge["message_id"] = data["message_id"]

        edges.append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }
