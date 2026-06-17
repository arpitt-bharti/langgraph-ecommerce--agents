# check_refund_eligibility tool
from datetime import datetime
from langchain_core.tools import Tool
import importlib

from langchain_openai import ChatOpenAI
import sqlite_db
from sqlite_db import fetch_order_from_db
from rag_v1 import fetch_retriever
importlib.reload(sqlite_db)

def check_refund_eligibility(order_id) :
    '''use this to check if a order is eligible for refund or not'''
    
    print('inside check_refund_eligibility tool')
    order = fetch_order_from_db(order_id)
    order_date_str = order['order_date']  # Example: "2026-05-29"
    order_date = datetime.strptime(order_date_str, "%Y-%m-%d")
    current_date = datetime.now()
    days_passed = (current_date - order_date).days
    
    if order['refund_eligible'] and order['shipping_status'] != 'cancelled' :
        return 'item is eligible for a refund'
    else:
        reason = order['refund_reason'] if not order['refund_eligible'] else 'More than 10 days since order got placed' if days_passed>10 else order['shipping_status']
        return reason
    
    
#RAG for fetching policies 
def fetch_policy_rag(user_query : str):
    print('inside fetch policy using RAG tool')
    retriever = fetch_retriever()
    policy = retriever.invoke(user_query)
    return "\n\n".join([doc.page_content for doc in policy])


def getRefundTools():
    fetch_policy_rag_tool = Tool(
        name = 'fetch_policy_tool',
        func = fetch_policy_rag,
        description='Use this rag tool to fetch policy related context'
    )
            
    check_refund_eligibility_tool =  Tool(
        name='check_refund_eligibility',
        func=check_refund_eligibility,
        description='use this to check if a order is eligible for refund or not'
    )

    refund_tools = [check_refund_eligibility_tool, fetch_policy_rag_tool]
    return refund_tools


def get_refund_llm_tools() :
    refund_llm = ChatOpenAI(model='gpt-5-nano')
    refund_tools = getRefundTools()
    refund_llm_with_tools = refund_llm.bind_tools(refund_tools)
    return refund_llm_with_tools

