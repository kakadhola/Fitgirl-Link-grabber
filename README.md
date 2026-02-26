# Fitgirl Link Grabber

An automated tool to extract direct download links from Fitgirl-Repacks "FuckingFast" landing pages. This tool simplifies the process of grabbing multiple download parts for use with download managers like `aria2c` or `wget`.

## Features
- **Landing Page Parsing:** Automatically extracts direct `dl` links from FuckingFast landing pages.
- **Batch Processing:** Processes multiple URLs in one go.
- **Clean Output:** Outputs only the direct links, ready to be piped into a text file for download managers.

## Installation

### Dependencies
Ensure you have Python 3 installed. You will also need the following libraries:
- `requests`
- `beautifulsoup4`
- `flask` (for the web interface)

You can install the dependencies using pip:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface
1. Run the application:
   ```bash
   python3 app.py
   ```
2. Open your browser and navigate to the local address (usually `http://127.0.0.1:5000`).
3. Paste your FuckingFast URLs and click "Process".

### CLI Automation
You can use a script to grab links and pipe them directly to a download manager:

1. **Grab Links:**
   ```bash
   python3 grab_links.py > links.txt
   ```

2. **Download with aria2c:**
   ```bash
   aria2c -i links.txt -d '/your/download/path' -j 5 -x 5
   ```

## License
MIT
