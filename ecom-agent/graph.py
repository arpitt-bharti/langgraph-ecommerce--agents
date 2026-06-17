from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from state import State
from ecomm_agents import classifier_agent, order_agent, complaint_agent,payment_agent,refund_agent
from ecomm_tools import complaint_agent_tools,order_agent_tools,refund_agent_tools

def build_graph():
    
    order_related_tools = order_agent_tools.getOrderTools()
    refund_tools = refund_agent_tools.getRefundTools()
    human_tools = complaint_agent_tools.getHuman_Agent_tools()
    classify_route = classifier_agent.classify_route
    
    graph_builder = StateGraph(State)
    graph_builder.add_node('classifier', classifier_agent.classifierAgent)
    graph_builder.add_node('orderAgent', order_agent.orderAgent)
    graph_builder.add_node('fetchOrderTool', ToolNode(tools=order_related_tools))
    graph_builder.add_node('refundTools', ToolNode(tools=refund_tools))
    graph_builder.add_node('paymentTool', ToolNode(tools=order_related_tools))
    graph_builder.add_node('human_tools', ToolNode(tools=human_tools))
    graph_builder.add_node('refundAgent', refund_agent.refund_agent)
    graph_builder.add_node('paymentAgent', payment_agent.paymentAgent)
    graph_builder.add_node('complaintAgent', complaint_agent.complaintAgent)

    graph_builder.add_edge(START, 'classifier')
    graph_builder.add_conditional_edges('classifier', classify_route,{'order' : 'orderAgent', 'refund' : 'refundAgent', 'payment' : 'paymentAgent', 'human':'complaintAgent'})
    graph_builder.add_conditional_edges('orderAgent', tools_condition, {'tools':'fetchOrderTool','__end__' : END})
    graph_builder.add_conditional_edges('refundAgent', tools_condition, {'tools':'refundTools','__end__' : END})
    graph_builder.add_conditional_edges('paymentAgent', tools_condition, {'tools':'paymentTool','__end__' : END})
    graph_builder.add_conditional_edges('complaintAgent', tools_condition, {'tools':'human_tools' ,'__end__' : END})
    graph_builder.add_edge('fetchOrderTool', 'orderAgent')
    graph_builder.add_edge('refundTools', 'refundAgent')
    graph_builder.add_edge('paymentTool', 'paymentAgent')
    graph_builder.add_edge('human_tools', 'complaintAgent')

    graph = graph_builder.compile()
    return graph
