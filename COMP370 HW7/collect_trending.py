import argparse # for making CLI
import json # for writing to output file
from bs4 import BeautifulSoup # for webscraping
import requests # for making calls to website
from pathlib import Path # for writing and reading files

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
website_url = "https://montrealgazette.com/category/news/"

def get_page_data(link=website_url, file_name="montrealgazette_data"):
    # cacheing function when testing to reduce load on the Montreal Gazette servers
    path = Path(f"{file_name}.html")
    if not path.exists():
        data = requests.get(link, headers=headers)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data.text)

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-file", required=True, help="Intended output file to write results to")

    args = parser.parse_args()
    output_file = args.output_file

    data = get_page_data()
    soup = BeautifulSoup(data, 'html.parser')
    trending = soup.find('div', {'class': 'col-xs-12 top-trending'})
    trending_articles = trending.find_all('li')
    # print(len(trending_articles)) # this prints 5, so we know that we have the 5 trending articles on the front page

    trending_article_links = []

    for article in trending_articles:
        article_info = article.find('a')
        article_link = article_info['href']
        # when there is no class specified, but a tag has certain properties within it we can use accessing like how we would access columns of a dataframe
        new_link = f"https://montrealgazette.com/{article_link}"
        trending_article_links.append(new_link)


    out = []

    for i, article_link in enumerate(trending_article_links):
        article_response = get_page_data(article_link, f"article{i+1}")
        article_soup = BeautifulSoup(article_response, 'html.parser')
        # now that we have loaded our trending articles, it is time to scrape each of them and pull out the relevant information
        # we want: title, publication date, author, opening "blurb"
        details = {}
        # when using find, we specify the label and then class information to extract a certain type of tag
        details["title"] = article_soup.find('h1', {'class': 'article-title'}).text
        details["publication_date"] = article_soup.find('span', {'class': 'published-date__since'}).text
        details["author"] = article_soup.find('span', {'class': 'published-by__author'}).text
        details["opening_blurb"] = article_soup.find('p', {'class': 'article-subtitle'}).text
        out.append(details)

    with open(output_file,"w") as f:
        json.dump(out, f)
        # writing article details to specified output file

if __name__ == "__main__":
    main()