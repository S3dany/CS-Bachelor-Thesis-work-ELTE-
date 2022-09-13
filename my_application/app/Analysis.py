import networkx as nx
import pandas as pd


def create_directed_graph(dataframe):
    dataframe = dataframe.values.tolist()
    directed_graph = nx.DiGraph()
    for i in dataframe:
        directed_graph.add_edge(i[0], i[1], capacity=i[2])
    return directed_graph


def find_strongly_connected_components(directed_graph):
    strongly_connected_components = list(nx.kosaraju_strongly_connected_components(directed_graph))
    for component in strongly_connected_components:
        if len(component) == 1:
            directed_graph.remove_node(list(component)[0])
    filtered_strongly_connected_components = filter(lambda a: len(a) > 1,
                                                    strongly_connected_components)
    return list(filtered_strongly_connected_components)


def get_subgraphs(graph):
    list_strongly_connected_graphs = []
    for i in list(graph.subgraph(c)
                  for c in find_strongly_connected_components(graph)):
        subgraph = graph.subgraph(list(i))
        strongly_connected_graph = graph.__class__()
        strongly_connected_graph.add_edges_from((n, nbr, d)
                                                for n, nbrs in graph.adj.items() if n in subgraph
                                                for nbr, d in nbrs.items() if nbr in subgraph)
        strongly_connected_graph.graph.update(graph.graph)
        list_strongly_connected_graphs.append(strongly_connected_graph)

    return list_strongly_connected_graphs


def find_max_cycle_flow_sum(strongly_connected_graph):
    flows = []
    done = []
    strongly_connected_graph.add_node("S")
    for edge in strongly_connected_graph.edges:
        if edge not in done:
            strongly_connected_graph.add_edge(edge[0], "S",
                                              capacity=strongly_connected_graph.get_edge_data(*edge)["capacity"])
            cycle_flow_sum = 0
            residual = nx.algorithms.flow.dinitz(strongly_connected_graph, edge[1], "S")
            if residual.graph['flow_value'] != 0:
                cycle_flow_sum = sum(map(lambda e: residual.get_edge_data(*e)["flow"] if
                residual.get_edge_data(*e)["flow"] > 0 else 0,
                                         strongly_connected_graph.edges))
            flows.append([cycle_flow_sum, residual, edge])
            strongly_connected_graph.remove_edge(edge[0], "S")
    max_cycle_flow = max(flows, key=lambda x: float(x[0]))
    return max_cycle_flow


def update_directed_graph(directed_graph, max_cycle_flow):
    directed_graph[max_cycle_flow[2][0]][max_cycle_flow[2][1]]["capacity"] -= max_cycle_flow[1].graph["flow_value"]
    if directed_graph[max_cycle_flow[2][0]][max_cycle_flow[2][1]]["capacity"] == 0:
        directed_graph.remove_edge(max_cycle_flow[2][0], max_cycle_flow[2][1])
    done = []
    for k in directed_graph.edges:
        if max_cycle_flow[1][k[0]][k[1]]["flow"] > 0 and "S" not in k:
            directed_graph[k[0]][k[1]]["capacity"] -= max_cycle_flow[1][k[0]][k[1]]["flow"]
            if directed_graph[k[0]][k[1]]["capacity"] == 0:
                done.append((k[0], k[1]))
    for e in done:
        directed_graph.remove_edge(e[0], e[1])
    directed_graph.remove_node("S")
    return directed_graph


def choose_max_cycle_flow(strongly_connected_graph):
    max_cycle_flow = find_max_cycle_flow_sum(strongly_connected_graph)
    update_directed_graph(strongly_connected_graph, max_cycle_flow)
    return max_cycle_flow


def analyse(file):
    cycles_df = pd.DataFrame(columns=["cycle_flow", "cycle_flow_value", "cycle_total_value"])
    total_local_transactions = 0
    local_transactions_df = pd.DataFrame(columns=["from", "to", "local_amount"])

    initial_transactions_df = pd.read_csv(file)
    initial_transactions_df = initial_transactions_df.groupby(['from', 'to'])['amount'].sum().reset_index()

    no_of_initial_transactions = len(initial_transactions_df.index)
    total_initial_amount = initial_transactions_df['amount'].sum()
    graph = create_directed_graph(initial_transactions_df)
    no_of_initial_countries = graph.number_of_nodes()

    for i in get_subgraphs(graph):
        while len(get_subgraphs(i)) > 0:
            chosen_cycle_flow_result = choose_max_cycle_flow(i)
            total_local_transactions += chosen_cycle_flow_result[0]

            for e in chosen_cycle_flow_result[1].edges:
                if "S" not in e and chosen_cycle_flow_result[1].get_edge_data(*e)['flow'] > 0:
                    local_transactions_df = local_transactions_df.append({"from": e[0], "to": e[1],
                                                                          "local_amount":
                                                                              chosen_cycle_flow_result[1].
                                                                         get_edge_data(*e)['flow']},
                                                                         ignore_index=True)
            local_transactions_df = local_transactions_df.append(
                {"from": chosen_cycle_flow_result[2][0], "to": chosen_cycle_flow_result[2][1],
                 "local_amount": chosen_cycle_flow_result[1].graph['flow_value'], },
                ignore_index=True)
            local_transactions_df = local_transactions_df.groupby(['from', 'to'])['local_amount'].sum().reset_index()

            chosen_cycle_flow_edges = list(filter(lambda a: "S" not in a and
                                                            chosen_cycle_flow_result[1].get_edge_data(*a)[
                                                                'flow'] > 0,
                                                  chosen_cycle_flow_result[1].edges))

            chosen_cycle_flow_edges.append(chosen_cycle_flow_result[2])
            cycle = {"cycle_flow": chosen_cycle_flow_edges,
                     "cycle_flow_value": chosen_cycle_flow_result[1].graph['flow_value'],
                     "cycle_total_value": chosen_cycle_flow_result[0]}
            cycles_df = cycles_df.append(cycle, ignore_index=True)

    no_of_local_countries = len(pd.unique(local_transactions_df[["from", "to"]].values.ravel()))
    no_of_local_transactions = len(local_transactions_df.index)
    local_transactions_df = pd.merge(initial_transactions_df, local_transactions_df, how='right',
                                     left_on=['from', 'to'],
                                     right_on=['from', 'to'])

    local_countries_df = local_transactions_df[['to', 'local_amount']].groupby(['to']).sum().reset_index()
    local_countries_df = local_countries_df.rename(columns={'to': 'country'})

    no_of_cycle_flows = len(cycles_df.index)
    no_complete_local_transactions = local_transactions_df[local_transactions_df.amount ==
                                                           local_transactions_df.local_amount].shape[0]

    return cycles_df, local_transactions_df, total_local_transactions, total_initial_amount, initial_transactions_df, \
           local_countries_df, no_of_initial_transactions, no_of_initial_countries, no_of_local_countries, \
           no_of_cycle_flows, no_of_local_transactions, no_complete_local_transactions
