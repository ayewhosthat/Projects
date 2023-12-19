import argparse
import json
import pandas as pd
import re # regular expression to replace punctuation
from pathlib import Path
from collections import defaultdict
# we use a defaultdict to handle missing keys when we try to access them
import os

# valid speech acts - exact match for one of the character ponies
# treat words as case-insensitive - store in lowercase
# replace punctuation characters with space
# remove stopwords
# words only contain letters

MAIN_PONIES = ['fluttershy', 'rarity', 'applejack', 'pinkie pie', 'rainbow dash', 'twilight sparkle']
# main ponies

def load_stopwords(stopwords_path):
    with open(stopwords_path, 'r') as f:
        stopwords_list = [line.strip() for line in f]
    return set(stopwords_list)

def remove_punctuation(text):
    return re.sub(r'[()\[\],\-.\?!:;#&]', ' ', text)
    # replacing all special characters with spaces

def fix_dialog(input_file):
    df = pd.read_csv(input_file)
    # we want instances where there is only one occurrence of the main ponies in the character box
    pony_speaker_filter = df['pony'].str.lower().isin(MAIN_PONIES) & (df['pony'].str.split(' and ').apply(len) == 1)
    df = df.loc[pony_speaker_filter]
    # once we've found the valid sppech acts, we use the apply function to the text column to clean the text
    df['Clean Text'] = df['dialog'].apply(lambda x: remove_punctuation(x.lower()))
    return df

def get_word_counts(dialog, stopwords):
    character_word_counts = {pony.lower(): defaultdict(int) for pony in MAIN_PONIES}
    # creating a dictionary of word counts for each main pony, and storing them in a dictionary
    # now iterate through rows of the dataset and get the word counts for each pony and add them to the dicitonary
    for index, row in dialog.iterrows():
        pony = row['pony'].lower()
        dialog_text = row['Clean Text']
        for word in dialog_text.split():
            if word not in stopwords: # checking if the word is a stopword
                character_word_counts[pony][word] += 1
            
    return character_word_counts

def filter_word_counts(word_counts, k):
    # we want words that have a count more than 5
    filtered_word_counts = {character: {word: count for word, count in counts.items() if count >= k} for character, counts in word_counts.items()}

    return filtered_word_counts

def write_to_json(json_file_path, word_counts):
    directory = os.path.dirname(json_file_path)
    # extracting directory from the file path so that we can create the directory, the file gets created with open

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(json_file_path, 'w') as f:
        json.dump(word_counts, f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', help='Output path to file to store results', required=True)
    parser.add_argument('-d', '--input', help='Input file containing dialogue data', required=True)
    args = parser.parse_args()
    output_file = args.output
    input_file = args.input

    # load stopwords
    stopword_path = Path(__file__).parent / 'stopwords.txt'
    stopword_set = load_stopwords(stopword_path)

    pony_dialog_file_path = Path(__file__).parent / input_file
    clean_dialog_df = fix_dialog(pony_dialog_file_path)

    pony_word_counts = get_word_counts(clean_dialog_df, stopword_set)
    above_threshold = filter_word_counts(pony_word_counts, 5)

    write_to_json(output_file, above_threshold)

if __name__ == "__main__":
    main()