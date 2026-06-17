
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv(override=True)
EMBEDDING_MODEL = OpenAIEmbeddings(model='text-embedding-3-small')

def create_knowledge_base(path:Path) : 
    folder_path = path
    kb=''
    for file_path in folder_path.glob("*.txt"):
        with open(file_path,'r',encoding='utf-8') as file :
            print('starting.....')
            kb += f'\n---DOCUMENT --- : {file_path.name}---\n'
            kb += file.read()
    return kb

def chunk_docs(knowledge_base : str) :
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks = splitter.create_documents([knowledge_base])
    print(len(chunks))
    return chunks

def embedAndStore(chunks) :
    PERSIST_DIRECTORY = r'C:\AppyProjects\CustomGenAIProjects\ecomm-agents\ecom-agent\chroma_db'
    vectorStore=Chroma.from_documents(
        documents=chunks,
        embedding=EMBEDDING_MODEL,
        persist_directory=PERSIST_DIRECTORY
    )
    return vectorStore

def ingest_data(path):
    kb= create_knowledge_base(path)
    chunks = chunk_docs(kb)
    vectorStore = embedAndStore(chunks)
    print('ingestion complete !')
    return vectorStore


def fetch_retriever():
    PERSIST_DIRECTORY = r'C:\AppyProjects\CustomGenAIProjects\ecomm-agents\ecom-agent\chroma_db'
    vs = Chroma(persist_directory=PERSIST_DIRECTORY,
                embedding_function=EMBEDDING_MODEL)
    return vs.as_retriever(kwargs={'k':3})


if __name__ == '__main__' :
    vs = ingest_data(Path(r'C:\AppyProjects\CustomGenAIProjects\ecomm-agents\ecom-agent\knowledge_base'))