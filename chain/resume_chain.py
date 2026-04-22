
from utils.vector_store import create_vector_store
from langchain_core.prompts import ChatPromptTemplate

def resume_chain(pdf_path, query):
    vector_store = create_vector_store(pdf_path)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Retrieve relevant documents
    retrieval_docs = retriever.invoke(query)
    context = "\n".join(doc.page_content for doc in retrieval_docs)
    
    return context