import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os.path import exists
from sklearn.metrics import cohen_kappa_score

def analyze_articles():
    if not exists("articles.xlsx"):
        print("No articles.xlsx found, please run with -s <search_string> first")
        return

    dataframe = pd.read_excel("articles.xlsx")
    
    generate_graphs(dataframe, graph_type="countplot", graph_title="Category Countplot", graph_index=None, graph_columns="Category")
    generate_graphs(dataframe, graph_type="countplot", graph_title="Definition Countplot", graph_index=None, graph_columns="Definition")
    generate_graphs(dataframe, graph_type="heatmap", graph_title="Category Heatmap", graph_index="Category", graph_columns="Date")
    generate_graphs(dataframe, graph_type="heatmap", graph_title="Definition Heatmap", graph_index="Definition", graph_columns="Date")
    generate_graphs(dataframe, graph_type="heatmap", graph_title="Category Definition Heatmap", graph_index="Category", graph_columns="Definition")
    generate_graphs(dataframe, graph_type="histogram", graph_title="Date Histogram", graph_index=None, graph_columns="Date")

    
def generate_graphs(dataframe, graph_type=None, graph_title=None, graph_index=None, graph_columns=None):
    if graph_type == "countplot":
        sns.countplot(data=dataframe, x=graph_columns)
    elif graph_type == "heatmap":
        pivot_table = dataframe.pivot_table(
        index=graph_index, columns=graph_columns, aggfunc="size", fill_value=0
        )
        sns.heatmap(pivot_table, annot=True, linewidth=0.5)
    elif graph_type == "histogram":
        sns.histplot(data=dataframe[graph_columns], discrete=True, kde=False)
    plt.title(graph_title)
    plt.show()

if __name__ == '__main__':
    analyze_articles()