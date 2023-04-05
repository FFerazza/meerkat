from settings import SPRINGER_API_KEY
import requests
import json
import unicodedata
import hashlib

def get_springer_articles(search_string='devsecops', starting_year: int= None, pagination_url=None, articles={}) -> list[dict]:
    articles = articles
    if not pagination_url:
        url = f"http://api.springernature.com/meta/v2/json?q=title:\"{search_string}\"&api_key={SPRINGER_API_KEY}"
    else:
        url=f'http://api.springernature.com{pagination_url}'
    connection = requests.get(url)
    results = json.loads(connection.text)
    for result in results['records']:
        normalized_title = unicodedata.normalize('NFKD',result['title']).encode()
        title_hash = hashlib.md5(normalized_title).hexdigest()
        print(f'Found article: {result["title"]} in Springer Nature')
        articles.update({result.get('doi',title_hash):{'Title': result['title'], 'Date': result['publicationDate'], 'Category': ''}})
    if results.get('nextPage', None):
        articles.update(get_springer_articles(search_string=search_string, pagination_url=results['nextPage'], articles=articles))
    return articles