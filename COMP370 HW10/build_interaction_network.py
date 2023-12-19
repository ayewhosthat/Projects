import json
import os
import argparse
import pandas as pd
from pathlib import Path
from collections import defaultdict

words_to_exclude = ['others', 'ponies', 'and', 'all']

def load_dialog(input_csv):
    with open(input_csv, 'r', encoding='utf-8') as f:
        return pd.read_csv(input_csv)
    
def group_by_epsiode(mlp_df):
    return mlp_df.groupby(['title'], as_index=False)

def get_number_interactions(mlp_dialog_grouped_by_episode):
    interactions = defaultdict(lambda: defaultdict(int))
    for episode, group in mlp_dialog_grouped_by_episode:
        # episode is the unique title of the episode, group refers to all the interactions within that episode
        current_speaker = group.iloc[1]['pony']
        for i, interaction in group.iterrows():
            pony = interaction['pony']
            if any([word in pony for word in words_to_exclude]):
                continue # we skip this interaction
            # if there was a valid current speaker it gets reset as the interaction is voided
            if pony == current_speaker:
                current_speaker = pony
                continue
            # at this point, we have established that there is a valid current speaker
            if i == 0:
                continue
            else:         
                # undirected graph: each interaction counts as 1 for each
                interactions[pony][current_speaker] += 1
                interactions[current_speaker][pony] += 1
                current_speaker = pony

    return interactions

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
    parser.add_argument('-i', '--input_csv', required=True, help='Path to clean_dialog.csv')
    parser.add_argument('-o', '--path_output', required=True, help='Path to interaction_network.json')
    args = parser.parse_args()
    input_csv = args.input_csv
    output_json = args.path_output
    path_dialog = Path(input_csv)
    
    dialog = load_dialog(path_dialog)
    grouped_by_epsiode = group_by_epsiode(dialog)
    interactions = get_number_interactions(grouped_by_epsiode)

    top_frequent = sorted(interactions, key=lambda pony: sum(interactions.get(pony).values()), reverse=True)[:101]
    # get 101 most frequent speakers based on the sum of values of their respective dictionaries
    filtered_interactions = dict(filter(lambda item: item[0] in top_frequent, interactions.items()))
    # we filter to extract those rows which contain these speakers

    path_json_output = Path(output_json)
    
    write_to_json(filtered_interactions, path_json_output)
    
if __name__ == '__main__':
    main()

# a pony X speaks to another pony Y when a line from X follows a line from Y
# pony cannot talk to itself
# when skipping characters that have 'others', 'ponies', 'and', 'all' in their names, the line before gets 'voided' - the interaction doesn't count
# interactions shouldn't cross epsiodes
# interactions go both ways: if X speaks to Y, X has had an interaction with 
