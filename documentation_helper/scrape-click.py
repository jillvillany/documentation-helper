## WARNING: NOT COMPLETE!!
# scrape the latest langchain documentation
import os
import json
import time
import utils as utils
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions
from bs4 import BeautifulSoup


def scrape():
    start = time.time()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    visited_urls = []
    queue = ['https://python.langchain.com/docs/introduction/']
    
    # clean errors at start of run
    errors_fp = "output/errors.txt"
    os.makedirs("output", exist_ok=True)
    with open(errors_fp, "w") as f:
        f.write("")
    
    site_data = {}
    
    url_num = 0
    while queue:
        url_num += 1
        print(f"Visiting URL #{url_num}, URLs in queue = {len(queue)}")
        
        url = queue.pop(0)
        
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
                
            site_data[url] = {
            "url": url,
            "title": title,
            "page_content": page_content.text
            }

            link_tags = page_content.find_all("a")
            for tag in link_tags:
                href = tag.get("href")
                if href \
                and "#" not in href \
                and (href.startswith("/docs") or href.startswith("https://python.langchain.com")) \
                and href not in visited_urls + queue:
                    
                    linked_url = href
                    if linked_url.startswith("/docs"):
                        linked_url = "https://python.langchain.com" + href
                        
                    queue.append(linked_url)
        
        except exceptions.InvalidSessionIdException as e:
            # session quit out - reinstatiate the driver and add url back to the queue
            driver = webdriver.Chrome(options=chrome_options)
            queue.append(url)
            
            error_details = f"Url #{url_num} {url} hit {type(e)} adding url back to queue"
            print(error_details)

            with open(errors_fp, "a") as f:
                f.write(f"{error_details}\n")

        except Exception as e:
            error_details = f"Url #{url_num} {url} had exception {e}"
            print(error_details)

            with open(errors_fp, "a") as f:
                f.write(f"{error_details}\n")

        visited_urls.append(url)
    
    driver.close()
    
    fp = "output/site_data.json"
    os.makedirs("output", exist_ok=True)
    with open(fp, "w") as f:
        json.dump(site_data, f)
    print(f"Wrote {fp}")    

    end = time.time()
    hours, minutes, seconds = utils.convert_seconds(end - start)
    print(f"Scraped {len(visited_urls)} urls in {hours}h {minutes}m {seconds}s")

if __name__ == "__main__":
    scrape()