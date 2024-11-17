import argparse

from langchain_community.embeddings import OllamaEmbeddings #DEPRECATED VERSION
# from langchain_ollama import OllamaEmbeddings

# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma

from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

from langchain.evaluation import load_evaluator


CHROMA_PATH = "chroma"

NUM_RESULTS = 1

PROMPT_TEMPLATE = """
Given this context only, answer the question that follows:

{context}

---

Based on the context, answer the follwing question:{query}
"""


#python3 pipeline/3_make_queries.py "Is Hillary Clinton the Candidate?"
#conda activate base
#conda activate myenv


def main():

    query = queryParser()

    embedding_function = OllamaEmbeddings()

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    results = db.similarity_search_with_relevance_scores(query, k=NUM_RESULTS)

    if len(results) ==0 or results[0][1] < 0.7 :
        return

    promptBuilder(results, query)



def promptBuilder(results, query):
    
    context = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, question = query)
    # print(prompt)

    model = OllamaLLM(model="llama3.2")
    response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    # formatted_response = f"Response: {response_text}\nSources: {sources}"
    formatted_response = f"Response: {response_text}"
    print(formatted_response)


def queryParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text",type=str)
    args = parser.parse_args()
    query_text = args.query_text
    return query_text

if __name__ == "__main__":
    main() 
