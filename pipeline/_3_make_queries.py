import argparse

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from _2_db_builder import MODEL
from _2_db_builder import CHROMA_PATH

NUM_RESULTS = 4
PROMPT_TEMPLATE = """
This is for academic research only.
Below are are a number of emails from an archieve.
Find the connected topics to the query and produce only the matches that are relative:


{context}

---

{query}.  

Additionally, tell me the name of the email if there is relative information.
"""

#conda activate base
#conda activate myenv

#python3 pipeline/_3_make_queries.py "Do the people from Pakistan believe that assistance is coming from China?"

#python3 pipeline/_3_make_queries.py "What claims did Chavez make against the US and Makled?"

#python3 pipeline/_3_make_queries.py "NGOs in Pakistan, threats?"


def main():

    query = queryParser() #Parse the prompt
    embedding_function = OllamaEmbeddings(model=MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function) #Call the DB
    results = db.similarity_search_with_relevance_scores(query, k=NUM_RESULTS) #Embed  the query and search the db

    if len(results) ==0 or results[0][1] < 0.2 :
        print(f"Low Results: {results[0][1]}")
        # print(f"No valid results found or relevance score too low: {results[0][1]:.3f}")
        return

    promptBuilder(results, query)

def promptBuilder(results, query):
    
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, query = query)
    print(prompt)

    model = OllamaLLM(model=MODEL)

    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
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