import requests
import json
import unicodedata
import hashlib
from settings import SCOPUS_API_KEY


def get_scopus_articles(
    search_string: str,
    pagination_url: str = None,
    articles: dict = {},
    is_web_search: bool = False,
):
    """Function that returns a dictionary of articles from Scopus

    Args:
        search_string (str, optional): _description_. Defaults to scopus_search_string.
        max_pages (int, optional): _description_. Defaults to max_pages.
        fields (str, optional): _description_. Defaults to "&field=title,coverDate,identifier".
        page (int, optional): _description_. Defaults to 0.
    """

    scopus_url = "https://api.elsevier.com/content/search/scopus?query="
    if is_web_search:
        scopus_search_string = f"""TITLE-KEY{search_string}"""
    else:
        scopus_search_string = f"""TITLE-ABS-KEY("{search_string}")"""
    scopus_fields = "&count=20"
    api_key = f"&apiKey={SCOPUS_API_KEY}"
    research_url = "%s%s%s%s" % (
        scopus_url,
        scopus_search_string,
        scopus_fields,
        api_key,
    )
    articles = {}

    if pagination_url:
        research_url = pagination_url
    else:
        research_url = research_url

    connection = requests.get(research_url)
    results = json.loads(connection.text)
    for item in results["search-results"]["entry"]:
        if item.get('error'):
            print(f'No results found for {search_string}')
            return articles
        normalized_title = unicodedata.normalize("NFKD", item["dc:title"]).lower()
        title_hash = hashlib.md5(normalized_title.encode()).hexdigest()
        print(f'Found article: {item["dc:title"]} in Scopus')
        articles.update(
            {
                item.get("prism:doi", title_hash): {
                    "Title": normalized_title,
                    "URL": [l["@href"] for l in item['link'] if l['@ref']=="scopus"][0],
                    "Date": item["prism:coverDate"],
                }
            }
        )
    if [
        item["@href"]
        for item in results["search-results"]["link"]
        if item["@ref"] == "next"
    ]:
        pagination_next = [
            e["@href"] for e in results["search-results"]["link"] if e["@ref"] == "next"
        ][0]
        articles.update(
            get_scopus_articles(
                search_string=search_string,
                pagination_url=pagination_next,
                articles=articles,
            )
        )
    return articles
