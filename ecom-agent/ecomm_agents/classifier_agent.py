#classifier agent
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from typing import Literal
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
load_dotenv(override=True)

#structured output for classifier llm
class classifier(BaseModel) : 
    category : Literal['order', 'refund', 'payment', 'human']

classifierLLM = ChatOpenAI(model='gpt-5-nano')
classifierLLM_with_SO = classifierLLM.with_structured_output(classifier)

class State(TypedDict) :
    messages : Annotated[list, add_messages]
    humanRequired : bool
    category : str

def classifierAgent(old_state : State) :
    PROMPT = f''' 
    You are a classifier agent for an ecommerce platform. 
    Your work is to analyze the incoming user queries and decide
    the category which they belong to. Your response should be the category the query belongs to.
    Here's the user query - {old_state['messages'][0].content}

    If it belongs to orders specifically - route it to order agent.
    If it belongs to refunds specifically - route it to refund agent.
    If it belongs to payment specifically - route it to payment agent.
    If it belongs to inquiring information or making claims about company's policies, - route it to refund agent.
    If the query belongs to anything other than the 3 categories defined above or if the query is a customer's complaint,
    regarding any order, route them to the compliant agent to raise a ticket.
    '''
    response = classifierLLM_with_SO.invoke(
        input=[SystemMessage(content=PROMPT)]
    )
    print(f'category : {response.category}')
    return {
        'category' : response.category
    }
    
    
def classify_route(old_state : State) :
    return 'order' if old_state['category']=='order' else 'refund' if old_state['category']=='refund' else 'payment' if old_state['category'] == 'payment' else 'human'