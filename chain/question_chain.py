from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from utils.vector_store import create_vector_store
from config import api_key

# Store conversation history
chat_history = []

def run_interview(context, user_input):
    global chat_history
    
    llm = ChatOpenAI(model="gpt-4o")
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """You are an expert interviewer 
             Candidate Resume Info: {context}
             Use this context and ask questions based on resume 
             Rules:
             --Ask relevant questions based on resume
             --Adapt to interviewer response 
             --Ask follow-ups
             --Do not repeat same question
             --Be realistic
             --Ask production based scenario questions
             """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{user_input}")
        ]
    )
    
    # Create the chain
    question_chain = prompt | llm
    
    # Invoke with context and chat history
    response = question_chain.invoke({
        "context": context,
        "user_input": user_input,
        "chat_history": chat_history
    })
    
    # Store in chat history
    chat_history.append(HumanMessage(content=user_input))
    chat_history.append(AIMessage(content=response.content))
    
    return response.content

    