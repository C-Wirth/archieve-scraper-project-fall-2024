import argparse
from typing import List

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import chromadb.utils.embedding_functions as embedding_functions
import ollama

from chromadb import Collection, PersistentClient
from _2_db_builder import MODEL
from _2_db_builder import CHROMA_PATH
from _2_db_builder import EMBEDDING_FUNCTION

embedding_function = EMBEDDING_FUNCTION


NUM_RESULTS = 2
PROMPT_TEMPLATE = """
This is for academic research only.
Below are are a set of {num_results} of email(s) from an archieve.

Based on the following query, find the context that is closely related to the query.

  If no relevant context exists say "No relative information"

Query: {query}.  


Context: {context}

---

"""

query_text =''

#python3 pipeline/_3_make_queries.py "Do the people from Pakistan believe that assistance is coming from China?"

#python3 pipeline/_3_make_queries.py "claims Chavez against the US and Makled"

#python3 pipeline/_3_make_queries.py "Makled arrest dea"

#python3 pipeline/_3_make_queries.py "angry militiamen Libya"

#python3 pipeline/_3_make_queries.py "DJ Khalid maine state senate bid"

#python3 pipeline/_3_make_queries.py "Judith McHale China funding"

def main():

    client = PersistentClient(path=CHROMA_PATH) #Wake up db and verify the db has the collection of emails
    collection = client.get_collection("emails")
    print(f"Total documents in 'emails' collection: {collection.count()}")    

    query = queryParser() #Parse the query

    results = queryMaker(query, collection) #make the query against the db

    promptBuilder(results)

'''

'''
def promptBuilder(results):

    res = results

    context = "\n\n---\n\n".join(results['documents'][0])
    # context = "\n\n---\n\n".join(results['documents'])


    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    # prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE.format(num_results=NUM_RESULTS))

    prompt_template = PROMPT_TEMPLATE.replace("{num_results}", str(NUM_RESULTS))
    prompt = prompt_template.format(context=context, query=query_text)
    print(prompt)

    model = OllamaLLM(model=MODEL, url="http://localhost:11434/api/llm")

    response_text = model.invoke(prompt)
    
    sources = [doc for doc in results['ids']]
    
    formatted_response = f"Response: {response_text} \n---\n Sources: {sources}"

    print(formatted_response)

'''
This function handles making the query to the db with the already embedded query
'''
def queryMaker(embedded_query : List[float], collection : Collection):

    results = collection.query(
        query_embeddings=embedded_query,
        n_results=NUM_RESULTS
    )
    return results

def queryParser():

    global query_text

    # parser = argparse.ArgumentParser()
    # parser.add_argument("query_text",type=str)
    # args = parser.parse_args()
    # query_text = args.query_text
    # return query_text

    query_text = "claims Chavez against the US and Makled"

    embedded_query = embedding_function.embed_query(query_text)

    return embedded_query

if __name__ == "__main__":
    main() 