from scopus import *
from os.path import exists
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#this is for algorithm test purposes only
from random import choices


if not exists('articles.json'):
    articles = get_scopus_articles()
    with open('articles.json', 'w') as f:
        json.dump(articles, f, ensure_ascii=False)


df = pd.read_json('articles.json')
df['Date'] = pd.to_datetime(df['Date']).dt.year


list_of_categories = ['technical', 'management', 'review', 'other']
df['Category'] = choices(list_of_categories, k=len(df))
pivot_table = df.pivot_table(index='Category', columns='Date', aggfunc='size', fill_value=0)

plt.figure(1)
sns.heatmap(pivot_table, annot=True)
plt.figure(2)
sns.histplot(data=df['Date'], discrete=True, kde=True)
plt.show()