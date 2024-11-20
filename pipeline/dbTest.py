from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

import chromadb.utils.embedding_functions as embedding_functions

ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    url="http://localhost:11434/api/embeddings",
    model_name="llama3.2",
)

embeddings = ollama_ef(["This is my first text to embed",
                        "This is my second document"])

print(embeddings)



# CHROMA_PATH = "chroma"
# MODEL="llama3.2"

# embedding_function = OllamaEmbeddings(model=MODEL)
# db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function) #Call the DB