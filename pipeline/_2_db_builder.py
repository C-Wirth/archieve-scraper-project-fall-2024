from typing import List
import glob
from langchain.schema import Document
import shutil
import os
import chromadb

from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import load_dotenv
load_dotenv()

INPUT_REPO = "data/email_repo"
DATA_PATH = f"{INPUT_REPO}"
MODEL="llama3.2"
CHROMA_PATH = "chroma"

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

EMBEDDING_FUNCTION = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    show_progress = True,
)

def main():
    '''
    Main Driver function with 3 main tasks:
    1. load the documents and create chunks
    2. instantiate a new, empty db
    3. build out the db's collection with the chunks
    '''

    chunks = load_documents()
    client = chroma_builder()
    collection_builder(chunks, client)

def load_documents() -> List[Document]:
    '''
    This function handles reads all markdown files from the DATA_PATH
    A List of Documents is returned
    A Document is a datatype with w fields:
                i 'page_content' field from the md file
                ii 'metadata' with the file_path

    Each document will represent 1 chunk, so chunking is not required
    '''
    files = glob.glob(os.path.join(DATA_PATH, '*.md'))
    documents = []

    for i, file_path in enumerate(files, start=1): #build each Document
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": file_path}))
            print(f"Document {i} read from {file_path}")  # Log each document

    print("\nAll files read and documents created")
    
    return documents

def chroma_builder():
    '''
    This function instantiates an empty db - will delete the last persited one
    '''

    if os.path.exists(CHROMA_PATH):
        print("Previous db deprecated")
        shutil.rmtree(CHROMA_PATH)

    print("Empty Database successfully created")

    return chromadb.PersistentClient(path=CHROMA_PATH)

def collection_builder(chunks : list[Document], client: chromadb):
    '''
    This function adds all chunks to the database
    '''

    embedding_function = EMBEDDING_FUNCTION

    embeddings = embedding_function.embed_documents([chunk.page_content for chunk in chunks])  
    
    collection = client.create_collection("emails")

    for i, chunk in enumerate(chunks, start=0):

        collection.add(
            ids=[chunk.metadata["source"]],  # Ensure metadata source is used as id
            embeddings=[embeddings[i]],
            documents=[chunk.page_content],
            )
        print(f"Document {i} added")

if __name__ == "__main__":
    main() 