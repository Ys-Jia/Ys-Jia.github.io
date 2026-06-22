import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Function to download a file from a URL and save it locally
def download_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
            print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download: {url}")

# Function to download specific resource types (e.g., CSS and JavaScript)
def download_specific_resources(base_url, page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create a directory in the current script directory to save resources
        script_dir = os.path.dirname(os.path.abspath(__file__))
        page_dir = os.path.basename(page_url)
        save_directory = os.path.join(script_dir, page_dir)
        os.makedirs(save_directory, exist_ok=True)

        # Define a regular expression pattern for acceptable file extensions
        accepted_extensions = r'\.(css|js)$'

        # Download linked resources (CSS and JavaScript files)
        for tag in soup.find_all(['link', 'script']):
            src = tag.get('src') or tag.get('href')
            if src and re.search(accepted_extensions, src):
                resource_url = urljoin(base_url, src)
                file_name = os.path.join(save_directory, os.path.basename(resource_url))
                download_file(resource_url, file_name)

# Input website URL
website_url = input("Enter website URL: ")

# Download specific resources (CSS and JavaScript) from the website
download_specific_resources(website_url, website_url)