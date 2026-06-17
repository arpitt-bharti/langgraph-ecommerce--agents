from langchain_core.messages import SystemMessage
from state import State
from dotenv import load_dotenv
from ecomm_tools import complaint_agent_tools
load_dotenv(override=True)


def complaintAgent(old_state : State):
    
    orig_query = old_state['messages'][0].content
    complaint_llm_with_tools = complaint_agent_tools.get_complaint_llm_tools()
    PROMPT = f''' 
    You are a complaint handling agent for a e-commerece business. This is the user's original query :-
    \n {orig_query}
    
    and this is the conversation so far \n 
    {old_state['messages']}
    
    Just like a real complaint handling agent, analyze the query if you can answer the user query directly from
    your intelligence and resolve it. 
    If the user's query is about knowing the details of a ticket id he might have raised, use the get_tick_details_tool
    tool to fetch the ticket details. If you get the details of the ticket back from the tool, analyze it and provide
    the user answer from the fetched ticket details in one line or two.
    
    If the tool returns that there was no ticket found, respond to the user that no such ticket exists with the 
    provided ticket id. Also ask the user to provide the issue so that you can help or create a new ticket.
    
    For anything other than answering a query related to information of a ticket,
    firstly use the create_ticket tool to check if a ticket already exists for the given order id from user. 
    if the tool responds with a existing ticket id, respond to the user saying a ticket already exists for the given 
    order id and provide the ticket details as well. 
    if there is no existing ticket, then use the create_ticket tool to create a support ticket.
    the tool takes order_id and description of issue as parameters and returns back the ticket id
    When the ticket has been created by the tool once, let customer know that a ticket has been created and will be reviewed by out 
    escalation team. Also provide the user with the ticket id for his query.  
    ONCE YOU GOT BACK THE TICKET_ID FROM THE TOOL, DO NOT RUN IT AGAIN.  
    '''
    
    complaint_response = complaint_llm_with_tools.invoke(
        input=[SystemMessage(content=PROMPT)]
    )
    
    return {
        'messages' : [complaint_response]
    }
    

