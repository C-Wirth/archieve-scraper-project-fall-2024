import json
import random
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}

JSON_FILE_ITERATION = "00"  # What JSON file number inputted
INPUT_JSON_PATH = f'data/json_files/clinton_emails/clinton_json_links_{JSON_FILE_ITERATION}.json'
OUTPUT_DIRECTORY = 'data/email_repo'
EMAIL_NAMING = 'clinton_email_content.md'

FIRST_BEGIN_DELIMITER = "h2"
POST_DOWNLOAD_END_DELIMITER = "\n*********************END_OF_EMAIL*********************\n"

output_iteration = 0  # Tracking the file naming for emails


def main():
    import os
    print("At directory: " + os.getcwd())

    # Load the input JSON file containing the links
    with open(INPUT_JSON_PATH, 'r') as json_file:
        json_data = json.load(json_file)

    print("JSON loaded")

    # Create an HTML format string for parsing with BeautifulSoup
    html_format = ''.join([f'<a href="{entry["link"]}">{entry["name"]}</a><br/>' for entry in json_data['leaks']])
    soup = BeautifulSoup(html_format, 'html.parser')

    # Process all links and build the repo
    repo_builder(soup)

"""
Iterates over the parsed HTML and processes each link to retrieve and save the emails.
"""
def repo_builder(soup: BeautifulSoup):

    global output_iteration

    for line in soup:
        # Find the next link
        url = find_next_link(str(line))

        if url:
            # Make an HTTP request to the link and parse the email
            current_soup = make_request(url)
            if current_soup:
                email_content = file_parser(current_soup, url, output_iteration)

                if email_content:
                    save_email(email_content, output_iteration)
                    output_iteration += 1

"""
Writes the parsed email content to a file.
"""
def save_email(email: str,output_iteration: int):

    email+=f"repo_number[{output_iteration}]"
    
    file_path = f'{OUTPUT_DIRECTORY}/{output_iteration}_{EMAIL_NAMING}'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(email)

    print(f"Email content downloaded and saved as {output_iteration}_{EMAIL_NAMING}\n")

"""
Makes an HTTP request to the provided URL and returns the parsed HTML content.
"""
def make_request(current_url: str) -> BeautifulSoup:

    time.sleep(random.uniform(1, 3))  # Avoid overwhelming the server

    if not current_url:
        print("No URL provided")
        return None

    print(f"Making request for URL: {current_url}")
    response = requests.get(url=current_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Failed to retrieve {current_url}")
        return None

    return BeautifulSoup(response.content, 'html.parser')

"""
Extracts the next hyperlink from the given line of HTML.
"""
def find_next_link(line: str) -> str:

    if not line.startswith("<a href="):
        return None

    soup = BeautifulSoup(line, 'html.parser')
    a_tag = soup.find('a')

    if a_tag and a_tag.has_attr('href'):
        return a_tag['href']

    return None

"""
Parses the email content from the provided HTML soup.
"""
def file_parser(soup: BeautifulSoup, url: str, output_iteration: int) -> str:

    beginning_text = soup.find(FIRST_BEGIN_DELIMITER)

    if not beginning_text:
        print(f"Email content start delimiter not found in {url}")
        return ''

    # Initialize email content
    final_email_content = ''
    content_lines = []

    email_content = beginning_text.find_next_sibling()

    while email_content:
        # Convert the email content to string and add it to the lines
        email_line = str(email_content)
        content_lines.append(email_line)
        email_content = email_content.find_next_sibling()

    final_email_content = "repo number["+ str(output_iteration) + "]\n" +''.join(content_lines) #+ POST_DOWNLOAD_END_DELIMITER

    print(f"Email parsed successfully")
    return final_email_content


if __name__ == "__main__":
    main()
