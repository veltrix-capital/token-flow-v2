import graphnetworkx as nx

def verify_graph_lib():
    graph = nx.DiGraph(weighted=True, directed=True)
    edges = [
        ('A', 'B', 3),
        ('B', 'C', 1),
        ('A', 'C', 5)
    ]

    for edge in edges:
        graph.add_edge(edge[0], edge[1], weight=edge[2])

    expected = ['A', 'B', 'C']    
    shortest = nx.shortest_path(graph, 'A', 'C', weight='weight')

    if shortest != expected:
        raise Exception('Invalid graph module')

def get_graph(edges, weighted=True, multi=True):
    graph = nx.DiGraph(weighted=weighted, directed=True) if not multi else nx.MultiDiGraph(weighted=weighted, directed=True)

    total_weight = {}
    for edge in edges:
        if weighted:
            edge_id = edge['from'] + '_' + edge['to']
            if multi:
                graph.add_edge(edge['from'], edge['to'], weight=edge.get('weight', 1))
            else:
                if edge_id not in total_weight:
                    graph.add_edge(edge['from'], edge['to'], weight=edge.get('weight', 0))
                    total_weight[edge_id] = edge['weight']
                else:
                    total_weight[edge_id] += edge['weight']
                    graph[edge['from']][edge['to']].update({ 'weight': total_weight[edge_id] })
        else:
            graph.add_edge(edge['from'], edge['to'])
    
    return graph

def get_reversed_edge(edge, weighted=True):
    if weighted:
        return {
            'from': edge['to'],
            'to': edge['from'],
            'weight': edge['weight']
        }

    return {
        'from': edge['to'],
        'to': edge['from'],
    }
