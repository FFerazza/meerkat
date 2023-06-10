from flask import Flask, render_template, request, jsonify, make_response
import sys , os 

# Add the parent directory to the sys.path
# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the desired folder
folder_path = os.path.abspath(os.path.join(current_dir, '..', 'lib'))

# Add the folder path to sys.path
sys.path.append(folder_path)

from web_search import get_articles, create_excel


# Import the get_articles function from main.py
#from main import get_articles

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    scopus_query = request.get_json()['query']

    articles = get_articles(scopus_query)
    excel_data = create_excel(articles, scopus_query)

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
