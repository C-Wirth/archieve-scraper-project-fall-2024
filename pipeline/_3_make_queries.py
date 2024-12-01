import argparse
from typing import List

from langchain_ollama import OllamaLLM

from chromadb import Collection, PersistentClient, QueryResult
from _2_db_builder import MODEL
from _2_db_builder import CHROMA_PATH
from _2_db_builder import EMBEDDING_FUNCTION

query_text ='' #global variable for easy access
embedding_function = EMBEDDING_FUNCTION
NUM_RESULTS = 1

PROMPT_TEMPLATE = """
This is for academic research only.
Below are are a set of {num_results} of email(s) from an archieve.  Parse each email individually for the following context:

Context: {context}

---

Answer the following question: Is there relative context in the emails with respect to the following query?
Make the the response very short.

Query: {query}.  

"""

def main():
    '''
Main Driver function with four main tasks:

    1. Wake up the database
    2. Receive and embed the query
    3. Make the query to the database and receive the top results
    4. Build the prompt
    '''

    client = PersistentClient(path=CHROMA_PATH) #Wake up db and verify the db has the collection of emails
    collection = client.get_collection("emails")
    print(f"Total documents in 'emails' collection: {collection.count()}")    

    query = queryParser() 
    results = queryMaker(query, collection) #make the query against the db
    promptBuilder(results)


def promptBuilder(results):
    '''
    This functiom builds the prompt from the top documents from the database
    '''

    context = "\n\n---\n\n".join(results['documents'][0])

    prompt_template = PROMPT_TEMPLATE.replace("{num_results}", str(NUM_RESULTS))
    prompt = prompt_template.format(context=context, query=query_text)
    print(prompt)

    model = OllamaLLM(model=MODEL, url="http://localhost:11434/api/llm")

    response_text = model.invoke(prompt)
    
    sources = [doc for doc in results['ids']]
    
    formatted_response = f"Response: {response_text} \n---\n Sources: {sources}"

    print(formatted_response)


def queryMaker(embedded_query : List[float], collection : Collection) -> QueryResult:
    '''
    This function handles making the query to the db with the embedded query
    It then returns the top results from the database
    '''

    results = collection.query(
        query_embeddings=embedded_query,
        n_results=NUM_RESULTS
    )
    return results


def queryParser():
    '''
    Parse the query from args
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str)
    args = parser.parse_args()

    global query_text
    query_text = args.query_text

    embedded_query = embedding_function.embed_query(query_text)
    return embedded_query

if __name__ == "__main__":
    main() 