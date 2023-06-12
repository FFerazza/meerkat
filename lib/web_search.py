from scopus import get_scopus_articles
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cosine_comparer import cosine_compare
import tempfile
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def get_articles(scopus_query):
    """Function that returns a dictionary of articles from Scopus

    Args:
        search_string (str, optional): _description_. Defaults to scopus_search_string.
        max_pages (int, optional): _description_. Defaults to max_pages.
        fields (str, optional): _description_. Defaults to "&field=title,coverDate,identifier".
        page (int, optional): _description_. Defaults to 0.
    """
    articles = get_scopus_articles(scopus_query, is_web_search=True)
    df = pd.DataFrame.from_dict(articles, orient="index")
    df = transform_and_validate(df)
    df["URL"] = df["URL"].apply(lambda x: f'=HYPERLINK("{x}", "{x}")') #let's make it clickable
    df.to_excel("articles.xlsx", sheet_name=f"{scopus_query}-articles", index=False)
    return df

def transform_and_validate(dataframe):
    """Function that transforms and validates the dataframe"""
    if dataframe.duplicated("Title").any():
        dataframe.drop_duplicates(subset="Title", inplace=True)
    cosine_compare(dataframe["Title"].tolist())
    dataframe["Date"] = pd.to_datetime(dataframe["Date"]).dt.year
    return dataframe

def create_excel(df, sheet_name):
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
        excel_file = temp_file.name
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        sheet = workbook[sheet_name]
        for column_cells in sheet.columns:
            max_length = 0
            for cell in column_cells:
                if cell.value:
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
            adjusted_width = (max_length + 2) * 0.9
            col_letter = get_column_letter(cell.column)
            sheet.column_dimensions[col_letter].width = adjusted_width
        writer.save()
        with open(excel_file, 'rb') as file:
            excel_data = file.read()

    return excel_data