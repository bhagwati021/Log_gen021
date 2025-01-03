import requests
from bs4 import BeautifulSoup
import time
import json
import re

# Retry mechanism and data scraping function
def featch_data_with_retries(url,retries=3,delay=2):
    """
    Fetches data from a url with retries in case of failure
    """
    for attempt in range(retries):
        try:
            response=requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exception.RequestException as e:
            print(f"Attempt {attempt + 1} Failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay * {attempt+1})    # exponential backoff resolution
            else:
                raise



# Function to extract data using Beautiful soup and regular expression
def extract_data_from_html(html_content):
    """"
    Extracting relavent data (links containing 'python')from the html content
    """
    if not html_content:
        raise ValueError("HTML content is invalid or empty!!!")
    
    soup=BeautifulSoup(html_content,'html.parser')
    titles=[]

    # Regular Expression to find all the links with the specific text 'python'
    for link in soup.find_all('a',href=True):
        title=link.get_text()
        if re.match(r'.*python.*',title,re.IGNORECASE):   #Looking for links containing python
            titles.append(title)

    return titles


# Function to save data to a json file
def save_data_to_json(data,filename="scraped_data.json"):
    """
    save the extrcted data to a json file
    """
    try:
        with open(filename,'w') as file:
            json.dump(data,file,indent=4)
        print(f"Data has been saved to {filename}")
    except Exception as e:
        print(f"Error saving data to the file: {e}")


# URL TO Scrape
url='https://www.python.org/downloads/'

# Fetch,Extract and Save the data 
html_content = featch_data_with_retries(url)
extracted_data = extract_data_from_html(html_content)
save_data_to_json(extracted_data)