import argparse
import json
import random
# we need random since we want to randomly select some posts to write into the tsv files

def extract_data(input_json_file, output_file, num_output):
    with open(input_json_file, "r", encoding='utf-8') as f:
        return json.load(f)
    
def write_to_file(input_json_file, output_file, num_output, data):
        subset = None
        if num_output >= len(data):
            subset = data
        else:
            subset = random.sample(data, k=num_output)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('Name\ttitle\tcoding\n')
            for post in subset:
                name = post['data']['author']
                title = post['data']['title']
                file.write(f"{name}\t{title}\t\s\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output_file", help="Output file that we write randomly selected posts to", required=True)
    parser.add_argument("json_file", help="Input JSON file")
    parser.add_argument("num_output", help="Number of posts to output. If greater than number of posts available, uses all")

    args = parser.parse_args()
    input_json_file, output_file, num_output = args.json_file, args.output_file, int(args.num_output)

    posts = extract_data(input_json_file, output_file, num_output)['data']['children']
    # we access the data section of the json and then get the posts which are nested within the children key

    write_to_file(input_json_file, output_file, num_output, posts)    

if __name__ == "__main__":
    main()