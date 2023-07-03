from scopus import get_scopus_articles
from springer import get_springer_articles
from search import transform_and_validate
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from cosine_comparer import cosine_compare
import tempfile
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

def get_articles(query):
    """Function that returns a dictionary of articles from Scopus

    Args:
        search_string (str, optional): _description_. Defaults to scopus_search_string.
        max_pages (int, optional): _description_. Defaults to max_pages.
        fields (str, optional): _description_. Defaults to "&field=title,coverDate,identifier".
        page (int, optional): _description_. Defaults to 0.
    """
    scopus_articles = get_scopus_articles(search_string=query, is_web_search=True)
    springer_articles = get_springer_articles(search_string=query, is_web_search=True)
    articles = {**scopus_articles, **springer_articles}
    if articles == {}:
        return pd.DataFrame()
    df = pd.DataFrame.from_dict(articles, orient="index")
    df = transform_and_validate(df, is_web_search=True)
    df["URL"] = df["URL"].apply(lambda x: f'=HYPERLINK("{x}", "{x}")') #let's make it clickable
    return df

def create_excel(df, sheet_name):
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
        excel_file = temp_file.name
        writer = pd.ExcelWriter(excel_file, engine='openpyxl')
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        sheet = workbook[sheet_name]
        for column_cells in sheet.columns:
            max_length = 0
            if column_cells[0].value == "Title":
                for cell in column_cells:
                    if cell.value:
                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                adjusted_width = (max_length + 1) * 0.9
                col_letter = get_column_letter(cell.column)
                sheet.column_dimensions[col_letter].width = adjusted_width
            else: 
                sheet.column_dimensions[column_cells[0].column_letter].width = 22
        writer.save()
        with open(excel_file, 'rb') as file:
            excel_data = file.read()

    return excel_data