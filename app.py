from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Function to extract direct link from a given Fuckingfast URL
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
                print(f"Script Content: {script.string[:200]}...")  # Debugging output
                match = re.search(r'https://fuckingfast\.co/dl[^"]+', script.string)
                if match:
                    return match.group(0).replace('\\', '')
        return None
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
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

if __name__ == '__main__':
    app.run(debug=True)
