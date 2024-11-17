# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

import shutil
import os

from dotenv import load_dotenv

INPUT_REPO = "data/email_repo"
DATA_PATH = f"{INPUT_REPO}"

text_splitter = RecursiveCharacterTextSplitter( #Splitter splits an email into chunks by paragraphs
    chunk_size=500,
    separators= [
        "\n\n",
        "\n"
    ]
)

load_dotenv()

embeddings = OllamaEmbeddings()
llm = OllamaLLM()
CHROMA_PATH = "chroma"

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
    
def buildChunks(documents):

    chunks = []
    total_docs = len(documents)

    for i, md_doc in enumerate(documents, start=1):
        
        doc_chunks = text_splitter.split_documents([md_doc])
        chunks.extend(doc_chunks)
        
        print(f"Document {i}/{total_docs} split into {len(doc_chunks)} chunks.") #a successful split has occured

    print(f"Splitting Completed: {len(documents)} documents into {len(chunks)} chunks.") #all done

    return chunks

def load_documents(): #The document contains all content on a page and meta data
    
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md")  # Load all markdown files in the directory
    documents = loader.load()  # loads the files into a list of documents
    return documents

if __name__ == "__main__":
    main() 