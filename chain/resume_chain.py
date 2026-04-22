from langchain_core.runnables import (RunnablePassthrough,RunnablePipe,RunnableLambda)
from langchain_openai import ChatOpenAI
from utils.vector_store import create_vector_store
from langchain_core.prompts import ChatPromptTemplate

def resume_chain(pdf_path,query):
    vector_store = create_vector_store(pdf_path)
    retriever = vector_store.as_retreiver(search_kwargs={"k":3})
    llm = ChatOpenAI(model="gpt-4o")
    retrieval_docs = retriever.get_relevant_documents(query)
    context = "\n".join(doc.page_content for doc in retrieval_docs)
    return context