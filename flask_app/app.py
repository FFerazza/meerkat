from flask import Flask, render_template, request, jsonify, make_response, abort
import sys , os, re


current_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.abspath(os.path.join(current_dir, '..', 'lib'))
sys.path.append(folder_path)

from web_search import get_articles, create_excel
from settings import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    query = request.get_json()['query']
    
    # Validate the query
    if not query or not re.match(r'^[a-zA-Z0-9()\s]+$', query):
        return abort(400, 'Invalid query. Only alphanumeric characters and parentheses are allowed.')

    articles = get_articles(query)
    excel_data = create_excel(articles, query)

    # Set the appropriate headers for Excel file download
    headers = {
        'Content-Disposition': f'attachment; filename="articles.xlsx"',
        'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }

    # Create a response with Excel file data and headers
    response = make_response(excel_data)
    response.headers = headers

    return response

@app.after_request
def add_no_cache_headers(response):
    if request.path == '/query':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run()
