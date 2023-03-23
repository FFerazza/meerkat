import requests
import json
from settings import *

scopus_search_string="""TITLE-ABS-KEY("devops security") OR TITLE-ABS-KEY("devsecops") OR TITLE-ABS-KEY("secdevops")"""
scopus_fields = "&field=title,coverDate,identifier&count=20&start="
scopus_url="https://api.elsevier.com/content/search/scopus?query="
research_url=  "%s%s%s"  % (scopus_url, scopus_search_string, scopus_fields)

def get_scopus_articles(search_string: str=research_url,fields: str = "&field=title,coverDate,identifier", page: int = 0):
    """ Function that returns a dictionary of articles from Scopus

    Args:
        search_string (str, optional): _description_. Defaults to scopus_search_string.
        max_pages (int, optional): _description_. Defaults to max_pages.
        fields (str, optional): _description_. Defaults to "&field=title,coverDate,identifier".
        page (int, optional): _description_. Defaults to 0.
    """
    connection = requests.get(research_url+str(page*20), {"apiKey": API_KEY})    
    return json.loads(connection.text)



response= get_scopus_articles()
articles = {}
for item in response['search-results']['entry']:
    print(item['dc:identifier'].strip('SCOPUS_ID:'))
    print(item['dc:title'])
    print(item['prism:coverDate'])
    print('')
    articles[item['dc:identifier'].strip('SCOPUS_ID:')] = { "title": item['dc:title'], "date": item['prism:coverDate'] } 
pagination = int(response['search-results']['opensearch:totalResults'])/25
for page in range(1, int(pagination)+1):
    new_articles = get_scopus_articles(page=page)
    articles[item['dc:identifier'].strip('SCOPUS_ID:')] = { "title": item['dc:title'], "date": item['prism:coverDate'] }   
print('lol')