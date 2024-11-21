import argparse

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
import chromadb.utils.embedding_functions as embedding_functions
import ollama

from _2_db_builder import MODEL
from _2_db_builder import CHROMA_PATH

NUM_RESULTS = 5
PROMPT_TEMPLATE = """
This is for academic research only.
Below are are a number of emails from an archieve.

Are there any files containing the relative information from this query? :


{query}.  

Find the most relative email and return the first line of the chunk, and return the key points relative to the query, only.  No extra content

If there is no relative information just say "No relative information".

Context below:


{context}

---


"""
#python3 pipeline/_3_make_queries.py "Do the people from Pakistan believe that assistance is coming from China?"

#python3 pipeline/_3_make_queries.py "claims Chavez against the US and Makled"

#python3 pipeline/_3_make_queries.py "Assistance funds pakistan 2009"

#python3 pipeline/_3_make_queries.py "angry militiamen Libya"

#python3 pipeline/_3_make_queries.py "DJ Vance presidential bid"




def main():
     
    embedding_function = embedding_functions.OllamaEmbeddingFunction( 
    url="http://localhost:11434/api/embeddings",
    model_name="llama3.2",
)
        

    query = queryParser() #Parse the prompt
    embedding_function = OllamaEmbeddings(model=MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function) #Call the DB
    results = db.similarity_search_with_relevance_scores(query, k=NUM_RESULTS) #Embed  the query and search the db

    promptBuilder(results, query)

def promptBuilder(results, query):
    
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    reference_numbers = [doc.metadata.get("reference_number", "No reference found") for doc in results]
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, query = query)
    print(prompt)

    model = OllamaLLM(model=MODEL)

    response_text = model.invoke(prompt)

    sources = [
        f"{doc.metadata.get('source', 'Unknown source')} (Reference: {ref})"
        for doc, ref in zip(results, reference_numbers)
    ]
    formatted_response = f"Response: {response_text} \n---\n Sources: {sources}"

    print(formatted_response)

def queryParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str)
    args = parser.parse_args()
    query_text = args.query_text
    return query_text



if __name__ == "__main__":
    main() 