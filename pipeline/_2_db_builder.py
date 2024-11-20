from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from _1_WikiLeaksScraper import POST_DOWNLOAD_END_DELIMITER

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

embeddings = OllamaEmbeddings(model=MODEL,)

llm = OllamaLLM(model=MODEL)

def main():
    
    email_repo = load_documents()

    all_chunks = buildChunks(email_repo)

    # print(all_chunks[1].page_content)
    # print(all_chunks[1].metadata)

    chroma_builder(all_chunks)

def chroma_builder(all_chunks: list[Document]):

    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        all_chunks,
        embeddings,
        persist_directory=CHROMA_PATH
    )
    print("Database successfully created")

"""
Split documents into chunks by POST_DOWNLOAD_END_DELIMITER.
"""    
def buildChunks(documents):

    chunks = []
    total_docs = len(documents)

    for i, doc in enumerate(documents, start=1):
        # Split the document content by the delimiter
        doc_parts = doc.page_content.split(POST_DOWNLOAD_END_DELIMITER)
        
        # Create a new Document object for each chunk with the same metadata
        doc_chunks = [
            Document(page_content=chunk.strip(), metadata=doc.metadata)
            for chunk in doc_parts if chunk.strip()  # Exclude empty chunks
        ]
        chunks.extend(doc_chunks)

        print(f"Document {i}/{total_docs} split into {len(doc_chunks)} chunks.")  # Successful split log

    print(f"Splitting Completed: {total_docs} documents into {len(chunks)} chunks.")  # All done
    return chunks


def load_documents(): #The document contains all content on a page and meta data
    
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")  # Load all markdown files in the directory
    documents = loader.load()  # loads the files into a list of documents
    return documents

if __name__ == "__main__":
    main() 