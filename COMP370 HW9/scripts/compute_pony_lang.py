import argparse
import json
import math
from pathlib import Path

OUTPUT_JSON_PATH = 'distinctive_pony_words.json'

def load_data(json_path):
    filepath = Path(json_path)
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def compute_tfidf(tf, idf):
    return tf * idf

def compute_idf(word, word_counts_by_pony):
    num_ponies_with_word = 0 
    # the following loop determines how many ponies spoke that word
    for counts in word_counts_by_pony.values():
        if word in counts:
            num_ponies_with_word += 1
    total_ponies = len(word_counts_by_pony)

    if num_ponies_with_word == 0:
        return 0
    else:
        return math.log(total_ponies / num_ponies_with_word)

def compute_top_words(word_counts_by_pony, num_words):
    top_words = {}

    for pony, word_counts in word_counts_by_pony.items():
        tfidf_list = []

        for word, tf in word_counts.items():
            idf = compute_idf(word, word_counts_by_pony)
            tfidf = compute_tfidf(tf, idf)
            tfidf_list.append((word, tfidf))
            # appending tuple so we can access the tfidf score to sort later on

        tfidf_list.sort(key=lambda x: x[1], reverse=True)
        # we want descending order of the tfidf scores, which is the second element of the tuple
        top_words[pony] = [word for word, _ in tfidf_list[:num_words]]
        # doesn't matter what the tfidf score is once we've sorted

    return top_words

def save_to_json(data, output_json_path):
    filepath = Path(output_json_path)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--input_json', required=True, help='Path to word_counts_by_pony.json')
    parser.add_argument('-n', '--num_words', required=True, help='Number of top words to compute')

    args = parser.parse_args()
    input_json = args.input_json
    n = args.num_words

    word_counts_by_pony = load_data(input_json)

    top_words = compute_top_words(word_counts_by_pony, n)

    print(json.dumps(top_words))
    # convert to string then print to output

    save_to_json(top_words, OUTPUT_JSON_PATH)

if __name__ == '__main__':
    main()
