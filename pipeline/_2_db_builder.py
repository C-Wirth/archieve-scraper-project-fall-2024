
import httpx
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

import chromadb.utils.embedding_functions as embedding_functions
from _1_WikiLeaksScraper import POST_DOWNLOAD_END_DELIMITER

import ollama

import chromadb

import shutil
import os

from dotenv import load_dotenv
load_dotenv()

INPUT_REPO = "data/email_repo"
DATA_PATH = f"{INPUT_REPO}"
MODEL="llama3.2"
CHROMA_PATH = "chroma"



text_splitter = RecursiveCharacterTextSplitter( #Splitter splits an email into chunks by paragraphs
    chunk_size=1000,
    separators= [
        POST_DOWNLOAD_END_DELIMITER
        # "\n",
        # "\n\n",
    ]
)

#python3 pipeline/_2_db_builder.py

# embedding_function = OllamaEmbeddings(model=MODEL,) 

#Try new embedding function
embedding_function = embedding_functions.OllamaEmbeddingFunction( 
    url="http://localhost:11434/api/embeddings",
    model_name="llama3.2",
)

llm = OllamaLLM(model=MODEL)

def main():

    email_repo = load_documents()
    all_chunks = buildChunks(email_repo)
    chroma_builder(all_chunks)

def chroma_builder(documents: list[Document]):

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    print("Empty Database successfully created")

    collection = client.create_collection("emails")

    for i, d in enumerate(documents):
        
        id = d.page_content.split("\n")[0]

        response = ollama.embeddings(model="mxbai-embed-large", prompt=d.page_content)
        embedding = response["embedding"]
        collection.add(
            # ids=[str(i)],
            ids=id,
            embeddings=[embedding],
            documents=[d.page_content],
            metadatas=[{"reference_number": id}],
        )
        print(f"Document {i} added")


def buildChunks(documents):

    chunks = []
    total_docs = len(documents)

    for i, doc in enumerate(documents, start=1):
        chunks.append(Document(page_content=doc.page_content.strip(), metadata=doc.metadata)) #Adding each chunk to the chunks structure
        print(f"Document {i}/{total_docs} added as a single chunk")  # Log each document

    print(f"Processing Completed: {total_docs} documents added as {len(chunks)} chunks\n") 
    return chunks

def load_documents(): #The document contains all content on a page and meta data
    
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")  # Load all markdown files in the directory
    documents = loader.load()  # loads the files into a list of documents
    return documents

if __name__ == "__main__":
    main() 