Author : Colby Wirth
Last Update : 30 November 2024

What you need to run the model:

Python - https://www.python.org/downloads/

Huggingface - https://api.python.langchain.com/en/latest/embeddings/langchain_community.embeddings.huggingface.HuggingFaceEmbeddings.html

Vector Embedding - https://huggingface.co/sentence-transformers/all-mpnet-base-v2

LLama 3.2 - https://python.langchain.com/docs/integrations/llms/ollama/

ChromaDb - https://docs.trychroma.com/

Beautiful Soup -https://pypi.org/project/beautifulsoup4/
(**ONLY** needed if you want to scrape the archieve as performed in _1_WikiLeaksScraper.py)

How to run:

This is a pipeline.  The first two files have ALREADY BEEN run and the database has been built.  You just need to install the libraies to make your queries through your CLI.  See program 3 below to run the program


What The pipeline does:

program 1:
_1_WikiLeaksScraper.py:

    This file takes an inputted json file will a set of links to scrape for content.
    It will output a markdown file will all content from each scraped page.
    For the content of this assignment - I used a very small subset of links from the 'Clinton Emails' Wikileaks archieve. 
    The program is designed to parse those emails specifically.

program 2:
_2_db_builder.py

    This builds the chroma db and persists it locally.  the emails are embedded with the hugging face vector embedding function

program3;
_3_make_queries.py

    THIS IS YOUR PROGRAM TO MAKE QUERIES WITH.  You must pass a query from your command line.

    1. Start the Ollama application (it must be running in the background for you to be able interface with the LLM)

    2. command to run the program: 
        python3 pipeline/_3_make_queries.py <query here>
        
        example command :
        python3 pipeline/_3_make_queries.py "NGO pakistan"