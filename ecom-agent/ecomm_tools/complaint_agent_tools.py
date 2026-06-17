#TICKET CREATION TOOL 
import sqlite3
import uuid
from langchain_core.tools import StructuredTool, Tool
from langchain_openai import ChatOpenAI
from sqlite_db import fetch_order_from_db

#Args schema for the tool
from pydantic import BaseModel, Field

class CreateTicketInput(BaseModel):
    order_id: str = Field(description="The unique order ID string.")
    description: str = Field(
        description="A concise summary of the complaint."
    )

def create_ticket(order_id : str, description : str) : 
    '''use this to create a new ticket for the user query'''
    
    print('Starting ticket tool  !')
    order = fetch_order_from_db(order_id)
    if not order:
        return 'Order not found, so no ticket can be created !'
    else:
        ticket_conn = sqlite3.connect('tickets.db')
        tick_cursor = ticket_conn.cursor()
        ticket_id = 'TICKET'+str(uuid.uuid4())

        existing_ticket = tick_cursor.execute(
            ''' 
            select * from tickets where order_id = ?
            ''',(order_id,)
        )
        old_ticket = existing_ticket.fetchone()
        if old_ticket :
            return f'ticket already exists - {old_ticket}'
        
        tick_cursor.execute(
            ''' 
            insert into tickets (
                ticket_id,
                order_id,       
                description,     
                status,          
                created_date 
            )
            VALUES (
                ?,?,?,?,?
            )
            ''',
            (
                ticket_id,
                order_id,
                description,
                'Under review',
                '15th June,2026'
            )
        )
        ticket_conn.commit()
        ticket_conn.close()
    print(f'ticket id created - {ticket_id}')
    return f"Success! Created ticket with ID: {ticket_id}"


def get_ticket_details(ticket_id : str) : 
    '''use this tool to find details of customer's tickets'''
    
    print('inside fetch tickets details tool')
    ticket_conn = sqlite3.connect('tickets.db')
    tick_cursor = ticket_conn.cursor()
    
    ticket = tick_cursor.execute(
        ''' 
        select * from tickets where ticket_id = ?
        ''' , (ticket_id,)
    )
    ticket = ticket.fetchone()
    print(f'status - {ticket}')
    if not ticket:
        return 'No ticket found with the given ticket id'
    else:
        return ticket

def getHuman_Agent_tools():
    get_tick_details_tool = Tool(
        name='get_ticket_tool',
        func=get_ticket_details,
        description='use this to fetch ticket details'
    )

    create_tick_tool = StructuredTool.from_function(
        name='create_ticket_tool',
        func = create_ticket,
        description='use this to create a new ticket for the user complaint',
        args_schema = CreateTicketInput
    )

    human_tools = [create_tick_tool, get_tick_details_tool]
    return human_tools

def get_complaint_llm_tools():
    human_llm = ChatOpenAI(model='gpt-5-nano')
    human_tools = getHuman_Agent_tools()
    human_llm_with_tools = human_llm.bind_tools(human_tools)
    return human_llm_with_tools