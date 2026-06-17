from langchain_core.messages import SystemMessage
from ecomm_tools import order_agent_tools
from dotenv import load_dotenv
from state import State
load_dotenv(override=True)

def orderAgent(old_state:State) :
    original_user_query = old_state['messages'][0].content
    worker_llm_w_tools = order_agent_tools.get_order_llm_with_tools()
   
    PROMPT = f''' 
    You are an Order Support Agent for an e-commerce platform.
    Here is the user's question - \n
    User Query:
    {original_user_query}
    
    And here's the conversation so far - \n
    {old_state['messages']}
    
    Instructions:

    * Use the fetch_order_details tool whenever order information is required.
    * Answer ONLY using information returned by the tool.
    * Do not invent tracking details, delivery dates, statuses, or actions by yourself.
    * If the order is not found, respond with a short humorous message.
    * Keep responses concise and customer-friendly.
    If a ToolMessage is already present in the conversation history,
    use that information to answer the user.

    Do not call fetch_order_details again once order information has been retrieved.
    If a ToolMessage is already present in the conversation history,
    DO NOT call any tool again.

    Use the ToolMessage content to answer the user directly.
    
    When order information is available:

    - First identify what the user is asking.
    - Answer ONLY that question.
    - DO NOT DUMP ALL order fields.
    - Summarize and only give the relevant information in plain ENGLISH in one or two sentences.
    
    Examples :
    query - where is my order
    response - your order has been delivered on 13th June 2026.
    
    query - why my payment got failed?
    response - your payment got failed due to this error code - ABC123. Please check details and try again

    '''
    orderResponse = worker_llm_w_tools.invoke(
        input=[SystemMessage(content=PROMPT)]
        )
    
    return {
        'messages' : [orderResponse]
    }
    
