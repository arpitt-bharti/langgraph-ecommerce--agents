from state import State
from langchain_core.messages import SystemMessage
from ecomm_tools import order_agent_tools
from dotenv import load_dotenv
load_dotenv(override=True)


def paymentAgent(old_state : State) :
    original_user_query = old_state['messages'][0].content
    worker_llm_w_tools = order_agent_tools.getOrderTools()
    PROMPT = f''' 
    You are a Payment Support Agent for an e-commerce platform.

    User Query:
    {original_user_query}
    
    And here's the conversation so far - \n
    {old_state['messages']}

    Instructions:

    * Use the fetch_order_details tool whenever payment information is needed.
    * Answer only using information returned by the tool.
    * Explain payment status clearly and concisely.
    * Do not invent payment actions, refunds, retries, or support processes.
    * If the order is not found, clearly inform the customer.
    * Keep responses short and professional.
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

    Examples:

    User: Where is my order?
    Answer: Your order has been delivered on 2026-05-22.

    User: What is my payment status?
    Answer: Your payment was successful.

    User: Is my order delivered?
    Answer: Yes, your order was delivered on 2026-05-22.
    '''
    payment_response = worker_llm_w_tools.invoke(
        input=[SystemMessage(content=PROMPT)]
    )
    
    return {
        'messages' : [payment_response]
    }