Author : Colby Wirth
Last Update : 30 November 2024

What you need to run the model:

Python - https://www.python.org/downloads/

Huggingface - https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.huggingface.HuggingFaceEmbeddings.html

Vector Embedding - https://huggingface.co/sentence-transformers/all-mpnet-base-v2

LLama 3.2 - https://python.langchain.com/docs/integrations/llms/ollama/

ChromaDb - https://docs.trychroma.com/

Beautiful Soup -https://pypi.org/project/beautifulsoup4/
(**ONLY** needed if you want to scrape the archieve in document 1)

How to run:

This is a pipeline.  The first two files have been run and the database.  You just need to install the libraies and make your queries through your CLI


What The pipeline does:

_1_WikiLeaksScraper.py:

    This file takes an inputted json file will a set of links to scrape for content.
    It will output a markdown file will all content from each scraped page.
    For the content of this assignment - I used a very small subset of links from the 'Clinton Emails' Wikileaks archieve. 
    The program is designed to parse those emails specifically.

_2_db_builder.py




