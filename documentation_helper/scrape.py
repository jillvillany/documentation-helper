import requests
import os
import json
import time
import utils as utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from bs4 import BeautifulSoup
from xml.etree import ElementTree


def get_langchain_docs_urls():
    """
    Fetches all URLs from the Langchain documentation.
    Uses the sitemap (https://python.langchain.com/sitemap.xml) to get these URLs.
    
    Returns:
        List[str]: List of URLs
    """            
    sitemap_url = "https://python.langchain.com/sitemap.xml"
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        
        # Parse the XML
        root = ElementTree.fromstring(response.content)
        
        # Extract all URLs from the sitemap
        # The namespace is usually defined in the root element
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = [loc.text for loc in root.findall('.//ns:loc', namespace)]
        
        return urls
    
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []  
    
def scrape(urls:list):
    start = time.time()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
        
    # clean errors at start of run
    errors_fp = "output/errors.txt"
    os.makedirs("output", exist_ok=True)
    with open(errors_fp, "w") as f:
        f.write("")
    

    docs = []
    
    for i, url in enumerate(urls):
        print(f"Visiting URL #{i + 1} of {len(urls)}")
        
        try:
            driver.get(url)
            # Wait until the document is fully loaded 
            while driver.execute_script("return document.readyState") != "complete": 
                time.sleep(10) 

            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            
            page_content = soup.find("div", {"class": "theme-doc-markdown markdown"})
            if not page_content:
                page_content = soup.find("article")
                title = page_content.parent.find("h1").text
            else:
                title = page_content.find("h1").text
                
            docs.append({
            "url": url,
            "title": title,
            "page_content": page_content.text
            })

        except exceptions.InvalidSessionIdException as e:
            # session quit out - reinstatiate the driver
            driver = webdriver.Chrome(options=chrome_options)
            
            error_details = f"Url #{i + 1} {url} hit {type(e)}"
            print(error_details)

            with open(errors_fp, "a") as f:
                f.write(f"{error_details}\n")

        except Exception as e:
            error_details = f"Url #{i + 1} {url} had exception {e}"
            print(error_details)

            with open(errors_fp, "a") as f:
                f.write(f"{error_details}\n")
    
    driver.close()
    
    fp = "output/langchain_custom_text_docs.json"
    os.makedirs("output", exist_ok=True)
    with open(fp, "w") as f:
        json.dump({"docs": docs}, f)
    print(f"Wrote {fp}")    

    end = time.time()
    hours, minutes, seconds = utils.convert_seconds(end - start)
    print(f"Scraped {len(docs)} urls in {hours}h {minutes}m {seconds}s")


if __name__ == "__main__":
    urls = get_langchain_docs_urls()
    scrape(urls)
    