import json
import os
import argparse
from .. newsapi import fetch_latest_news

def main():
    parser = argparse.ArgumentParser(description="CLI to query news articles using data from an input file. Writes to files in output dir")
    parser.add_argument("-k", "--api-key", required=True, help="Key used to make calls to the API")
    parser.add_argument("-b", "--lookback", required=False, help="Number of days to look back when querying news articles. If unspecified, defaults to 10")
    parser.add_argument("-i", "--input-file", required=True, help="File to read data from")
    parser.add_argument("-o", "--output-dir", required=True, help="Output is directed to this folder")

    # parse arguments to extract information
    args = parser.parse_args()
    lookback_days = int(args.lookback)
    # read json data from file
    with open(args.input_file, "r") as file:
        data = json.load(file)

    for name, keywords in data.items():
        try:
            news_arts = fetch_latest_news(api_key=args.api_key, news_keywords=keywords, lookback_days=lookback_days)
            # buildling file path that we can write to later on
            output_path = os.path.join(args.output_dir, f"{name}.json")
            with open(output_path, "w") as output_file:
                json.dump(news_arts, output_file)
        except Exception as err:
            print(f"Exception: {str(err)}")

if __name__ == "__main__":
    main()