from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from sqlite_db import fetch_order_from_db

def get_order(order_id) :
    '''Use this to fetch order details from the mock DB'''
    
    print('Get order tool called !')
    orderDetails = fetch_order_from_db(order_id)
    # print(f'found order details - {orderDetails}')
    return orderDetails

def getOrderTools():
    orderTool = Tool(
        name='fetch_order_details',
        func=get_order,
        description='Use this to fetch order details from the mock DB'
    )
    order_related_tools = [orderTool]
    return order_related_tools

def get_order_llm_with_tools():
    worker_llm = ChatOpenAI(model='gpt-5-nano')
    order_tools = getOrderTools()
    worker_llm_w_tools = worker_llm.bind_tools(order_tools)
    return worker_llm_w_tools
