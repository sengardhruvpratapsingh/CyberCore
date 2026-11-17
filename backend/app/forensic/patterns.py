import networkx as nx


def find_transaction_chains(
    graph,
    transactions,
    minimum_length=3,
    time_window_hours=24
):
    chains = []

    # Create a lookup:
    # (sender, receiver) -> list of transactions
    transaction_map = {}

    for transaction in transactions:
        key = (transaction.sender, transaction.receiver)

        if key not in transaction_map:
            transaction_map[key] = []

        transaction_map[key].append(transaction)

    for start_node in graph.nodes:

        for end_node in graph.nodes:

            if start_node == end_node:
                continue

            paths = nx.all_simple_paths(
                graph,
                start_node,
                end_node,
                cutoff=minimum_length - 1
            )

            for path in paths:

                if len(path) < minimum_length:
                    continue

                # Get transactions corresponding to each edge
                path_transactions = []

                valid_path = True

                for i in range(len(path) - 1):

                    sender = path[i]
                    receiver = path[i + 1]

                    key = (sender, receiver)

                    if key not in transaction_map:
                        valid_path = False
                        break

                    path_transactions.append(
                        transaction_map[key]
                    )

                if not valid_path:
                    continue

                # Use the earliest transaction for each edge
                selected_transactions = []

                for edge_transactions in path_transactions:

                    edge_transactions = sorted(
                        edge_transactions,
                        key=lambda x: x.timestamp
                    )

                    selected_transactions.append(
                        edge_transactions[0]
                    )

                # Get start and end time
                start_time = min(
                    transaction.timestamp
                    for transaction in selected_transactions
                )

                end_time = max(
                    transaction.timestamp
                    for transaction in selected_transactions
                )

                duration = end_time - start_time

                duration_hours = (
                    duration.total_seconds() / 3600
                )

                # Only accept chains inside time window
                if duration_hours <= time_window_hours:

                    chains.append({
                        "path": path,
                        "start_time": start_time,
                        "end_time": end_time,
                        "duration_hours": round(
                            duration_hours,
                            2
                        ),
                        "transaction_ids": [
                            transaction.transaction_id
                            for transaction in selected_transactions
                        ]
                    })

    return chains


def find_high_value_transactions(
    transactions,
    threshold=100000
):
    """Return all transactions above the configured high-value threshold."""
    return [
        transaction
        for transaction in transactions
        if float(transaction.amount) >= float(threshold)
    ]