import os
import sys
import requests  # Installed
import urllib.parse
import json
from pathlib import Path
from selenium import webdriver  # Installed
from selenium.webdriver.chrome.options import Options  # Installed
from bs4 import BeautifulSoup as Soup  # Installed

# Setup Selenium Webdriver
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

mdBook_url = sys.argv[1]  # URL to mdBook website
post_queries_json = sys.argv[2]  # raw URL to queries.json Ideally on a POST branch
reprocess_cache = False
if len(sys.argv) > 3:
    reprocess_cache = sys.argv[3]  # to define if triggered by site deployment


class Query(dict):
    def __init__(self, query, cached):
        dict.__init__(self, query=query, cached=cached)
        self.cached = cached
        self.query = query


class SearchResult(dict):
    def __init__(self, title, href, paragraph_preview):
        dict.__init__(self, title=title, href=href, paragraph_preview=paragraph_preview)


def url_string(string):
    return urllib.parse.quote(string, '/#')


def get_html(url):
    driver.get(url)
    return driver.page_source


def get_processed_results(query_url):
    html_item = Soup(get_html(query_url), 'html.parser')
    results_ul = html_item.find("ul", id="searchresults")
    results = results_ul.find_all('li')
    processed_results = []
    for result in results:
        title = result.a.get_text()
        result_href = query_url[0:query_url.find("?")] + url_string(result.a['href'])
        paragraph_preview = result.span.get_text()
        process_result = SearchResult(title, result_href, paragraph_preview)
        processed_results.append(process_result)
    return json.dumps(processed_results, indent=2)


def generate_query_json(query):
    query = sys.argv[0].replace("generate_index_JSON.py", "out/queries/" + query)
    p = Path(os.path.dirname(query))
    p.mkdir(exist_ok=True)
    with open(query, "w") as outfile:
        query_url = mdBook_url + "?search=" + url_string(query)
        outfile.write(get_processed_results(query_url))


def process_queries_json():
    queries = requests.get(post_queries_json).json()
    for query in queries:
        query_obj = Query(**query)
        if not query_obj.cached or reprocess_cache:
            generate_query_json(query_obj.query)
    return json.dumps(queries, indent=2)


def start():
    queries = sys.argv[0].replace("generate_index_JSON.py", "out/queries.json")
    p = Path(os.path.dirname(queries))
    p.mkdir(exist_ok=True)
    with open(queries, "w") as outfile:
        outfile.write(process_queries_json())


start()
