from settings import IEEEXPLORE_API_KEY
import requests
import json
import unicodedata
import hashlib

def get_ieee_articles(search_string, start_record=1, max_records=25):
    base_url = 'http://ieeexploreapi.ieee.org/api/v1/search/articles'
    
    result = {}
    while True:
        params = {
            'apikey': IEEEXPLORE_API_KEY,
            'format': 'json',
            'querytext': search_string,
            'start_record': start_record,
            'max_records': max_records
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        # error handling
        if response.status_code != 200:
            print(f"Request failed with status {response.status_code}")
            return None

        # creating the dictionary with necessary information
        articles = data['articles']
        for article in articles:
            if 'Books' in article.get('content_type', None):
                continue
            print(article.get('publication_year', 'No date available on IEEE'))
            title = article.get('title')
            normalized_title = unicodedata.normalize("NFKD", title).lower()
            title_hash = hashlib.md5(normalized_title.encode()).hexdigest()
            doi = article.get('doi', title_hash)
            pub_date = f"{article.get('publication_year', 'No date available on IEEE')}-01-01"
            result[doi] = {
                'Title': normalized_title,
                'URL': article.get('pdf_url', 'No URL available on IEEE'),
                'Date': pub_date
            }

        total_records = int(data.get('total_records', 0))
        if start_record + max_records > total_records:
            break
        else:
            start_record += max_records
    return result
