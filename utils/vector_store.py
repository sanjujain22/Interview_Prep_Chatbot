from langchain_community.document_loaders import PyPDFLoader
from langchain_core.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

def create_vector_store(pdf_path):
    loader =PyPDFLoader(pdf_path)
    docs=loader.load()
    embeddings=OpenAIEmbeddings()
    return FAISS.from_docuemnts(docs,embeddings)
