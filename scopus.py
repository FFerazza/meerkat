import requests
import json
import unicodedata
from settings import *

scopus_search_string="""TITLE-ABS-KEY("devops security") OR TITLE-ABS-KEY("devsecops") OR TITLE-ABS-KEY("secdevops")"""
scopus_fields = "&field=title,coverDate,identifier&count=20&start="
scopus_url="https://api.elsevier.com/content/search/scopus?query="
research_url=  "%s%s%s"  % (scopus_url, scopus_search_string, scopus_fields)
articles = []

def get_scopus_page(search_string: str=research_url,fields: str = "&field=title,coverDate,identifier", page: int = 0) -> dict:
    """ Function that returns a dictionary of articles from Scopus

    Args:
        search_string (str, optional): _description_. Defaults to scopus_search_string.
        max_pages (int, optional): _description_. Defaults to max_pages.
        fields (str, optional): _description_. Defaults to "&field=title,coverDate,identifier".
        page (int, optional): _description_. Defaults to 0.
    """
    connection = requests.get(research_url+str(page*20), {"apiKey": SCOPUS_API_KEY})    
    return json.loads(connection.text)

def loop_articles_from_page(page: dict):
    for item in page['search-results']['entry']:
        print(item['dc:identifier'].strip('SCOPUS_ID:'))
        print(item['dc:title'])
        print(item['prism:coverDate'])
        print('')
        articles.append({"Scopus_id":item['dc:identifier'].strip('SCOPUS_ID:'),  "Title": unicodedata.normalize('NFKD',item['dc:title']), "Date": item['prism:coverDate'], "Category": ""})

def get_scopus_articles():
    """ Function that returns a dictionary of articles from Scopus

    Args:
        search_string (str, optional): _description_. Defaults to scopus_search_string.
        max_pages (int, optional): _description_. Defaults to max_pages.
        fields (str, optional): _description_. Defaults to "&field=title,coverDate,identifier".
        page (int, optional): _description_. Defaults to 0.
    """
    page = get_scopus_page()
    loop_articles_from_page(page)
    pagination = int(page['search-results']['opensearch:totalResults'])/20
    for page in range(1, int(pagination)+1):
        page = get_scopus_page(page=page)
        loop_articles_from_page(page)
    return articles

