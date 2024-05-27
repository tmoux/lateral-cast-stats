#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup

def parse_transcript(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the transcript div
    transcript_div = soup.find('div', class_ = 'transcript')

    def process_div(div):
        return div.get_text().replace('\n', ' ')

    # find all quotes in div
    quote_divs = transcript_div.find_all('div', class_ = 'quote')
    transcript_lines = list(map(process_div, quote_divs))

    # Remove empty lines
    # transcript_lines = [line.strip() for line in transcript_lines if line.strip()]
    return transcript_lines

# Function to fetch HTML content of a webpage
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

BASE_URL = "https://lateralcast.com/episodes/"

for i in range(1, 85 + 1):
    print(i)
    url = f"{BASE_URL}{i}"
    html_content = fetch_html(url)
    if html_content:
        outfile = f"transcripts/{i}.txt"
        transcript_lines = parse_transcript(html_content)
        with open(outfile, 'w', encoding='utf-8') as output_file:
            # Write each line to the file
            for line in transcript_lines:
                output_file.write(line + '\n')