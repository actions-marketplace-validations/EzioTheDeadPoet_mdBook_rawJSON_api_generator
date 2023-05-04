import os
import sys
import requests  # Installed
import urllib.parse
import json
from pathlib import Path
from selenium import webdriver # Installed
from selenium.webdriver.chrome.options import Options # Installed
from bs4 import BeautifulSoup as Soup  # Installed

# Setup Selenium Webdriver
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

if len(sys.argv) < 2:
    print("missing arguments: mbBook_url output_file(optional)")
    exit(-1)

mdBook_url = sys.argv[1]

query = sys.argv[2]


class SearchResult(dict):
    def __init__(self, title, href, paragraph_preview):
        dict.__init__(self, name=title, href=href, paragraph_preview=paragraph_preview)

def get_html(url):
    driver.get(url)
    return driver.page_source


def get_processed_results(mdBook_url):
    html_item = Soup(get_html(mdBook_url), 'html.parser')
    results_ul = html_item.find("ul", id="searchresults")
    results = results_ul.find_all('li')
    processed_results = []
    for result in results:
        title = result.a.get_text()
        result_href = mdBook_url[0:mdBook_url.find("?")]+urllib.parse.quote(result.a['href'], '/#')
        paragraph_preview = result.span.get_text()
        process_result = SearchResult(title, result_href, paragraph_preview)
        processed_results.append(process_result)
    return json.dumps(processed_results, indent=2)


def is_header(element):
    if element.a is None:
        return False
    header_link = element.a
    return header_link.has_attr('class') and header_link['class'].count('header') > 0


print("START")

query = sys.argv[0].replace("generate_index_JSON.py", "json_index/queries/" + query)

print("The indexed data will be stored into:\n" + query)

p = Path(os.path.dirname(query))
p.mkdir(exist_ok=True)

with open(query, "w") as outfile:
    outfile.write(get_processed_results(mdBook_url))
    print("Indexing complete.\n")
