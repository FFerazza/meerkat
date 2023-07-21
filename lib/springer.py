from settings import SPRINGER_API_KEY
import requests
import json
import unicodedata
import hashlib


def convert_scopus_to_springer_query(search_string):
    groups = search_string.split(" AND ")
    query_parts = []
    for group in groups:
        keywords = group.strip("()").split(" OR ")
        title_query = " OR ".join([f"title:{keyword}" for keyword in keywords])
        query_parts.append(f"({title_query})")
    query = " AND ".join(query_parts)
    return query


def get_springer_articles(
    search_string: str,
    starting_year: int = None,
    pagination_url=None,
    is_web_search: bool = False,
) -> list[dict]:
    articles = {}
    if not pagination_url:
        if is_web_search:
            url = f'http://api.springernature.com/meta/v2/json?q={convert_scopus_to_springer_query(search_string)}&api_key={SPRINGER_API_KEY}'
        else:
            url = f'http://api.springernature.com/meta/v2/json?q=title:"{search_string}"&api_key={SPRINGER_API_KEY}'
    else:
        url = f"http://api.springernature.com{pagination_url}"
    connection = requests.get(url)
    results = json.loads(connection.text)
    for result in results["records"]:
        normalized_title = unicodedata.normalize("NFKD", result["title"]).lower()
        title_hash = hashlib.md5(normalized_title.encode()).hexdigest()
        print(f'Found article: {result["title"]} in Springer Nature')
        articles.update(
            {
                result.get("doi", title_hash): {
                    "Title": normalized_title,
                    "Date": result["publicationDate"],
                    "URL": result.get("url", {})[0]
                    .get("value", "")
                    .replace("http://link.springer.com", "https://link.springer.com"),
                }
            }
        )
    if results.get("nextPage", None):
        articles.update(
            get_springer_articles(
                search_string=search_string,
                pagination_url=results["nextPage"],
                articles=articles,
            )
        )
    return articles
