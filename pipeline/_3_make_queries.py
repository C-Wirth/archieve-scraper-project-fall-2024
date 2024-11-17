import argparse

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from _2_db_builder import MODEL
from _2_db_builder import CHROMA_PATH

NUM_RESULTS = 5
PROMPT_TEMPLATE = """
I am going to ask you provide some context, only answer with regards to the context:

{context}

---

Based on this context, answer the follwing question: {query}
"""

#conda activate base
#conda activate myenv

#python3 pipeline/_3_make_queries.py "Does Judith McHale believe that we should sent aid to Pakistan?  Why or why not?"


def main():

    query = queryParser()

    embedding_function = OllamaEmbeddings(model=MODEL)

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query, k=NUM_RESULTS)

    if len(results) ==0 or results[0][1] < 0.2 :
        print(f"No valid results found or relevance score too low: {results[0][1]:.3f}")
        return

    promptBuilder(results, query)

def promptBuilder(results, query):
    
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, query = query)
    print(prompt)

    model = OllamaLLM(model=MODEL)
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    # formatted_response = f"Response: {response_text}"
    print(formatted_response)

def queryParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str)
    args = parser.parse_args()
    query_text = args.query_text
    return query_text

if __name__ == "__main__":
    main() 
