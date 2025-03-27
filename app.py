from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

COUNTER_FILE = "counter.txt"  # File to store visitor count

# Function to read the visitor count from a file
def read_visitor_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")  # Initialize the counter file if not exists
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

# Function to increment and save the visitor count
def increment_visitor_count():
    count = read_visitor_count() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))
    return count

# Function to extract direct link from a given URL
def get_direct_download_link(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')

        for script in script_tags:
            if script.string:
                match = re.search(r'https://fuckingfast\.co/dl[^"]+', script.string)
                if match:
                    return match.group(0).replace('\\', '')
        return None
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

@app.route('/')
def index():
    visitor_count = increment_visitor_count()  # Increment visitor count
    return render_template('index.html', visitor_count=visitor_count)

@app.route('/process', methods=['POST'])
def process():
    try:
        data = request.json
        urls = data.get('urls', [])
        results = []

        for url in urls:
            direct_link = get_direct_download_link(url)
            if direct_link:
                results.append(direct_link)
            else:
                results.append(f"No direct link found for {url}")

        return jsonify(results=results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
