import requests
from bs4 import BeautifulSoup
import time
import random

# Define a user-agent list to simulate requests from different browsers
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/53.0',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.3',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12'
]


def get_page_content(url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        return response.content

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    return None


def parse_html(content):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    except Exception as e:
        print(f"An error occurred while parsing HTML: {e}")
        return None


def extract_info(soup):
    try:
        # Example of extracting different types of data

        # Extract all paragraphs
        paragraphs = [p.text for p in soup.find_all('p')]
        print("Paragraphs:")
        for para in paragraphs:
            print(para[:100])  # Print first 100 characters

        # Extract all links
        links = [a['href'] for a in soup.find_all('a', href=True)]
        print("\nLinks:")
        for link in links:
            print(link)

        # Extract all table data
        tables = soup.find_all('table')
        for idx, table in enumerate(tables):
            print(f"\nTable {idx + 1}:")
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                cols = [ele.text.strip() for ele in cols]
                print('\t'.join(cols))

        # Extract all lists
        lists = soup.find_all(['ul', 'ol'])
        for idx, lst in enumerate(lists):
            print(f"\nList {idx + 1}:")
            items = lst.find_all('li')
            for item in items:
                print(item.text.strip())

    except Exception as e:
        print(f"An error occurred while extracting information: {e}")


def scrape_website(url):
    content = get_page_content(url)

    if content:
        soup = parse_html(content)
        if soup:
            extract_info(soup)


if __name__ == "__main__":
    url = "https://www.worldbank.org/en/projects-operations/procurement?srce=both"
    scrape_website(url)
