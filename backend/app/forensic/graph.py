import networkx as nx


def build_transaction_graph(transactions):
    graph = nx.MultiDiGraph()

    for transaction in transactions:
        graph.add_edge(
            transaction.sender,
            transaction.receiver,
            transaction_id=transaction.transaction_id,
            amount=transaction.amount,
            timestamp=transaction.timestamp
        )

    return graph