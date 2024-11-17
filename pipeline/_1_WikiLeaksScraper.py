import json
import random
import time
import requests
from bs4 import BeautifulSoup

HEADERS={'User-Agent': 'Mozilla/5.0'}

ITERATION = "00"
CURRENT_ITERATION = f'data/json_files/clinton_emails/clinton_json_links_{ITERATION}.json'
INPUT_JSON_PATH = f'data/json_files/clinton_emails/clinton_json_links_{ITERATION}.json'
OUTPUT_DIRECTORY = 'data/email_repo'
EMAIL_NAMING = 'clinton_email_content.md'

FIRST_BEGIN_DELIMITER = "h2"
END_DELIMITER = "###"
final_email_content=''

i = 0 #increment on each file in the repo
TESTING_END_POINT = None  #Set = a number < 100 for testing.  Else set = None

# POST_DOWNLOAD_BEGIN_DELIMITER = "\n*********************NEW_EMAIL*********************\n"
POST_DOWNLOAD_END_DELIMITER = "\n*********************END_OF_EMAIL*********************\n"

'''
Main driver function
'''
def main():

    import os
    print("At directory: " + os.getcwd())

    with open(CURRENT_ITERATION, 'r') as json1: #import the file with the links to crawl
        json1 = json.load(json1)

    print("json loaded")
    
    html_format = ''.join([f'<a href="{entry["link"]}">{entry["name"]}</a><br/>' for entry in json1['leaks']]) 

    soup = BeautifulSoup(html_format, 'html.parser')#the soup to parse

    for line in soup : #iterate through each line in the soup

        # url = find_next_link #get the link
        url = find_next_link(str(line))

        if TESTING_END_POINT is not None and i == TESTING_END_POINT: #This is used for small batches of emails in testing
            break

        if url:
            current_soup = makeRequest(url) #make the https 
            fileParser(current_soup, url) #parse the current file and add it to the final archievd file

    with open(f'{OUTPUT_DIRECTORY}/{ITERATION}_{EMAIL_NAMING}', 'w', encoding='utf-8') as file:

        file.write(final_email_content)

print(f"Email content downloaded and saved as {ITERATION}_{EMAIL_NAMING}")

'''
This function hanldes the logic for making https requests

parameters: current_url -inputted line
'''
def makeRequest(current_url: str)-> str:

    time.sleep(random.uniform(1, 3))
    
    if not current_url:
        print("No url")
        return
    global i
    i+=1
    print(f"About to make request {i}")
    response = requests.get(url=current_url, headers=HEADERS)
    print(response)

    if response.status_code != 200:
        raise ValueError(f"Request not made for: {current_url}")
    
    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

'''
This function hanldes the logic for finding the next line in the file with a ink

parameters: line -inputted line
'''
def find_next_link(line: str)-> str:

    if not line.startswith("<a href="):
        return None

    print("about to find a link")

    soup = BeautifulSoup(line, 'html.parser') #use BS library to parse lines
    
    a_tag = soup.find('a') #find starting point

    if a_tag and a_tag.has_attr('href'): #verify we have a link
        return a_tag['href']
    
    return None

'''
this function parses a file and adds to the repo
'''
def fileParser(soup: BeautifulSoup, url: str):

    global final_email_content
    
    beginning_text = soup.find(FIRST_BEGIN_DELIMITER)

    if not beginning_text:
        raise ValueError(f"Beginning text not found at: {url}")
    
    email_content = beginning_text.find_next_sibling()
        
    content_lines = []

    # final_email_content += ''.join(POST_DOWNLOAD_BEGIN_DELIMITER) #Indicate beginning of new email

    while email_content:
        
        email_line = str(email_content)        
        content_lines.append(email_line)
        email_content = email_content.find_next_sibling()

        # final_email_content = ''.join(content_lines)
        final_email_content += ''.join(content_lines)

    final_email_content += ''.join(POST_DOWNLOAD_END_DELIMITER) #Indicate end of new email
    
    print("Email content downloaded and added to the current document")

def json_splitter():
    print("json called")

    with open(INPUT_JSON_PATH, 'r') as file:
        data = json.load(file)
    leaks = data['leaks']

    # Split the "leaks" array into chunks of 100 entries each
    chunks = [leaks[i:i + 100] for i in range(0, len(leaks), 100)]
    
    for index, chunk in enumerate(chunks): # Save each chunk to a new file

        print(f'beginning{index} iteration')

        cur_data = {
            "country": data["country"],
            "leakgroup": data["leakgroup"],
            "leaks": chunk
        }

        with open(f'clinton_json_links_{index + 1}.json', 'w') as outfile:
            json.dump(cur_data, outfile, indent=4)

    print("Files created successfully!")

if __name__ == "__main__":
    # json_splitter() #split all 1000 files
    main() 