from chain.question_chain import run_interview
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
import json
from config import api_key

llm = ChatOpenAI(model="gpt-4o")
evaluation_prompt = ChatPromptTemplate.from_messages([
    ("system", """
        You are an expert interview evaluator
        Evaluate the candidate's response objectively.
        Be concise and realistic.
        Review the answers up to the mark
     """),
     ("human", """
        Question:{question},
        Candidate Answer:{answer}
        Evaluate the answers and provide the score in valid JSON format
        Return
        - score(number 1-10),
        - strengths (short bullet-style points)
        - weaknesses (short bullet-style points to improve)
        - improved_answer (better version of the answer)
        
        Rules:
        --Score strictly(do not inflate)
        --Keep Feedback clear and actionable
        --Do not return anything outside JSON
      """)
])
def evaluate_results(question,answer):
    """
    Evaluate user answer and return the output in structured JSON format
    """
    evaluation_chain = evaluation_prompt | llm
    response = evaluation_chain.invoke({
        "question": question,
        "answer": answer
    })
    
    # Extract content from AIMessage object
    response_text = response.content
    
    # Try to extract JSON from response (in case it's wrapped in markdown or text)
    try:
        # First try direct JSON parsing
        result = json.loads(response_text)
    except json.JSONDecodeError:
        try:
            # Try to extract JSON from markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text
            result = json.loads(json_str)
        except (json.JSONDecodeError, IndexError):
            # Fallback if model return invalid JSON
            result = {}
    
    # Ensure all required keys are present with correct names
    default_result = {
        "score": 5,
        "strengths": "Could not parse response properly",
        "weaknesses": "Model output formatting issue",
        "improved_answer": "Unable to generate improved answer"
    }
    
    # Normalize and merge with defaults
    if isinstance(result, dict):
        # Merge with defaults to ensure all keys exist
        final_result = {**default_result, **result}
    else:
        final_result = default_result
    
    return final_result






