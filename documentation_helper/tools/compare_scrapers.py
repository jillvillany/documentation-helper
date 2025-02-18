import os
import asyncio
import time
import json
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import exceptions


async def main():
    url = "https://python.langchain.com/docs/concepts/lcel/"
    os.makedirs("output", exist_ok=True)
    
    # scrape with crawl4ai
    async with AsyncWebCrawler() as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url=url)

        # # Print the extracted content
        # print(result.markdown)
        md = result.markdown
        md = md.replace("</docs", "").replace("/>", "").split("On this page")[-1]

    d = {"docs": [{"url": url, "content": md}]}
    with open("output/lcel_md.json", "w") as f:
        json.dump(d, f)
        
    # crawl with selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    # Wait until the document is fully loaded 
    while driver.execute_script("return document.readyState") != "complete": 
        time.sleep(10) 

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    text = soup.text
    text = text.split("On this page")[-1]
    
    d = {"docs": [{"url": url, "content": text}]}
    with open("output/lcel_text.json", "w") as f:
        json.dump(d, f)


# Run the async main function
asyncio.run(main())