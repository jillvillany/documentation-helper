# LangChain Documentation Helper

Use RAG to answer questions about langchain functionality

## Quickstart

- conda create -n documentation_helper python=3.11.10 -y
- conda activate documentation_helper
- poetry install
- playwright install   # for using crawl4ai


## For custom scraping
`python scrape.py`

Scraped using the URLs in the sitemap.xml and crawl4ai following this tutorial: https://www.youtube.com/watch?v=JWfNLF_g_V0&t=919s

## For scraping langchain website and downloading its file structure with wget
`wget -r -A html -P langchain-docs https://python.langchain.com/docs`
- `-r` recursive
- `-A` accept file extensions
- `-P` directory to save files to

## Takeaways
- Tried using the crawl4ai package that converts it to a markdown but langchain docs have so much formatting and links it breaks up the flow of the context and made it harder to get a meaningful result
- using selenium webdriver with beautiful soup to get the text/ running some additional parsing proved better