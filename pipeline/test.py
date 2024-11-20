from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaLLM
from langchain.evaluation import load_evaluator




# from langchain_community.llms import Ollama DEPRECATED
# from langchain.embeddings import OllamaEmbeddings DEPRECATED

# llm = OllamaLLM(model="llama3.2")
# embeddings = OllamaEmbeddings()

# v1 = embeddings.embed_query("Apple")
# # print(len(v1))

# v2 = embeddings.embed_query("Banana")
# # v3 = embeddings.embed_query("Microsoft")
# v4 = embeddings.embed_query("Appel")


# from sklearn.metrics.pairwise import cosine_similarity

# x = cosine_similarity([v1],[v4])


# evaluator = load_evaluator("embedding_distance")
# x = evaluator.evaluate_strings(prediction="Apple", reference="Orange")

# print(x)

# result = llm.invoke("My Name is Sully")
# print(result)