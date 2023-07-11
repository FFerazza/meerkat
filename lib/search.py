from scopus import *
from springer import *
from ieeexplore import *
from os.path import exists
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cosine_comparer import cosine_compare
import argparse


def gather_articles():
    scopus_articles = get_scopus_articles(search_string=search_string)
    springer_articles = get_springer_articles(search_string=search_string)
    ieeexplore_articles = get_ieee_articles(search_string=search_string)
    print(f"Found {len(scopus_articles)} articles in Scopus")
    print(f"Found {len(springer_articles)} articles in Springer")
    print(f"Found {len(ieeexplore_articles)} articles in IEEE")
    merged_articles = {**scopus_articles, **springer_articles, **ieeexplore_articles}
    df = pd.DataFrame.from_dict(merged_articles, orient="index")
    df = transform_and_validate(df)
    df["URL"] = df["URL"].apply(lambda x: f'=HYPERLINK("{x}", "{x}")') #let's make it clickable
    df.to_excel("articles.xlsx", sheet_name=f"{search_string}-articles", index=False)


def transform_and_validate(dataframe, is_web_search=False):
    if is_web_search:
            if dataframe.duplicated("Title").any():
                dataframe.drop_duplicates(subset="Title", inplace=True)
            cosine_compare(dataframe["Title"].tolist())
            dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.year
            return dataframe
    if dataframe.empty:
        print("ERROR:No data found")
        return
    if "Date" not in dataframe.columns:
        print("ERROR: No date column found")
        return
    if "Title" not in dataframe.columns:
        print("ERROR: No title column found")
        return
    if dataframe.duplicated("Title").any():
        print("Duplicate rows found, removing duplicates")
        dataframe.drop_duplicates(subset="Title", inplace=True)
    cosine_compare(dataframe["Title"].tolist())
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.year
    dataframe["Category"] = ""
    dataframe["Definition"] = ""
    print("***Dataframe validation complete***")
    print("Dataframe shape: ", dataframe.shape)
    print(dataframe.dtypes)
    return dataframe


def analyze_articles():
    if not exists("articles.xlsx"):
        print("No articles found, please run with -s <search_string>")
        return

    df = pd.read_excel("articles.xlsx")

    list_of_categories = ["technical", "management", "review", "other"]
    list_of_definitions = ["defined", "undefined", "referenced"]
    pivot_table = df.pivot_table(
        index="Definition", columns="Date", aggfunc="size", fill_value=0
    )

    plt.figure(1)
    sns.heatmap(pivot_table, annot=True, linewidth=0.5)
    plt.figure(2)
    plt.locator_params(axis="x", integer=True)
    sns.histplot(data=df["Date"], discrete=True, kde=True)
    plt.show()

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-s",
        "--search",
        help="Queries multiple academic literature sources and saves data to an excel file",
        required=False,
    )
    argparser.add_argument(
        "-y", "--starting-year", help="Year to start searching from", required=False
    )
    argparser.add_argument(
        "-d",
        "--hard-dupe-validation",
        help="When validating, use text mining to detect duplicates that might still occur, undetected by pandas",
        required=False,
        action="store_true",
    )
    argparser.add_argument(
        "-a",
        "--analyze",
        help="Analyzes the data in articles.xlsx",
        required=False,
        action="store_true",
    )
    search_string = argparser.parse_args().search
    analyze = argparser.parse_args().analyze
    hard_validation = True

    if search_string:
        gather_articles()
    elif analyze and exists("articles.xlsx"):
        analyze_articles()