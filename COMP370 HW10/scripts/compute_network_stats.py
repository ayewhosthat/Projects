import argparse
import json
import networkx as nx
import os
from pathlib import Path

def load_interaction_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compute_deg_centrality(G):
    return nx.degree_centrality(G)

def compute_weighted_degree_centrality(G):
    weighted_degree_centrality = {node: sum(G[node][neighbor]['weight'] for neighbor in G[node]) for node in G}
    # summing the weights of all neighbouring edges
    return weighted_degree_centrality

def compute_closeness_centrality(G):
    return nx.closeness_centrality(G)

def compute_betweenness_centrality(G):
    return nx.betweenness_centrality(G)

def write_to_json(data, json_file_path):
    directory = os.path.dirname(json_file_path)
    # extracting directory from the file path so that we can create the directory, the file gets created with open

    # Create the directory if it doesn't exist
    if directory == '':
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_json', required=True, help='Path to interaction_network.json')
    parser.add_argument('-o', '--output_json', required=True, help='Path to stats.json')
    args = parser.parse_args()
    input_json = args.input_json
    output_json = args.output_json
    interaction_json_path = Path(input_json)
    interaction_data = load_interaction_data(interaction_json_path)
    
    # create weighted graph manually
    G = nx.Graph()
    for character, interactions in interaction_data.items():
        for neighbor, weight in interactions.items():
            if neighbor not in G:
                G.add_node(neighbor)
                # add node as neighbour if not already
            if G.has_edge(character, neighbor):
                G[character][neighbor]['weight'] += weight
                # update weight to neighbouring node
            else:
                # add edge if it doesn't exist
                G.add_edge(character, neighbor, weight=weight)

    degree = compute_deg_centrality(G)
    top_degree = sorted(degree, key=degree.get, reverse=True)[:3]
    weighted_degree = compute_weighted_degree_centrality(G)
    top_weight_degree = sorted(weighted_degree, key=weighted_degree.get, reverse=True)[:3]
    closeness = compute_closeness_centrality(G)
    top_closeness = sorted(closeness, key=closeness.get, reverse=True)[:3]
    betweenness = compute_betweenness_centrality(G)
    top_betweenness = sorted(betweenness, key=betweenness.get, reverse=True)[:3]

    stats = {
        'degree': top_degree,
        'weighted_degree': top_weight_degree,
        'closeness': top_closeness,
        'betweenness': top_betweenness
    }
    stats_json_path = Path(output_json)
    
    write_to_json(stats, stats_json_path)

if __name__ == '__main__':
    main()