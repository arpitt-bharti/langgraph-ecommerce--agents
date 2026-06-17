
import gradio as gr
from langchain_core.messages import HumanMessage
from graph import build_graph

graph = build_graph()

def answer(user_query, history):
    state = {
        "messages": [HumanMessage(content=user_query)]
    }
    result = graph.invoke(state)
    return result["messages"][-1].content

examples = [
    ["Where is my order ORD1008?"],
    ["When will ORD1001 arrive?"],
    ["Why did payment for ORD1004 fail?"],
    ["Is ORD1018 eligible for a refund?"],
    ["Why is ORD1018 not refundable?"],
    ["What is your refund policy?"],
    ["I received the wrong item in order ORD1019"],
    ["My package arrived empty for ORD1020"],
]
    
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.HTML("""
    <div style="text-align:center; padding:20px;">
        <h1>🛒 E-Commerce Multi-Agent Assistant</h1>
        <p>
            Powered by <b>LangGraph</b> • <b>GPT</b> • <b>SQLite</b> • <b>RAG</b>
        </p>
    </div>
    """)

    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### 📦 Orders
            - Track deliveries
            - View shipping status
            - Get tracking details
            """)

        with gr.Column():
            gr.Markdown("""
            ### 💰 Refunds
            - Check eligibility
            - Explain refund decisions
            - Retrieve refund policies
            """)

        with gr.Column():
            gr.Markdown("""
            ### 💳 Payments
            - Payment status
            - Failed payments
            - Payment methods
            """)

        with gr.Column():
            gr.Markdown("""
            ### 🎫 Complaints
            - Create support tickets
            - Check ticket status
            - Escalate issues
            """)

    gr.Markdown("---")

    gr.Markdown("## 🚀 Try These Example Queries")

    
    chatbot = gr.ChatInterface(
        fn=answer,
        examples=[
        "Where is my order ORD1008?",
        "When will ORD1001 arrive?",
        "Why did payment for ORD1004 fail?",
        "Is ORD1018 eligible for a refund?",
        "Why is ORD1018 not refundable?",
        "What is your refund policy?",
        "I received the wrong item in order ORD1019",
        "My package arrived empty for ORD1020",
        ],
        title="",
        description="Ask questions about orders, refunds, payments, complaints, and tickets."
    )

    gr.HTML("""
    <div style="padding:15px;border:1px solid #ddd;border-radius:10px;margin-bottom:20px;">
    <h3>🏗️ Technical Architecture</h3>

    <p>
    <b>Agents:</b> Classifier • Order • Refund • Payment • Complaint
    </p>

    <p>
    <b>Data Sources:</b> SQLite Orders DB • SQLite Tickets DB • RAG Policy Store
    </p>

    <p>
    <b>Tech Stack:</b> LangGraph • LangChain • OpenAI • SQLite • Gradio
    </p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
