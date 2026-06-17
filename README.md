# E-Commerce Multi-Agent Support System

An Agentic AI e-commerce customer support assistant built with LangGraph, LangChain, SQLite, and RAG.

It routes customer queries to specialized agents for orders, refunds, payments, and complaints.  
The system uses SQLite for structured data like orders and tickets, and RAG for policy-based answers like refund and return rules.

## Live Demo

🚀 Hugging Face Space:
https://huggingface.co/spaces/arpitt007/ecom-agent

## Features

- **Order Support Agent**: fetches order details from SQLite
- **Refund Support Agent**: checks refund eligibility and uses RAG for policy context
- **Payment Support Agent**: answers payment-related questions from order data
- **Complaint Support Agent**: creates support tickets and retrieves ticket details
- **Ticket deduplication**: prevents duplicate tickets for the same order/issue
- **RAG integration**: policy documents are retrieved only when needed
- **Modular architecture**: agents and tools are split into separate Python files

## Architecture

User Query  
→ Classifier Agent  
→ Specialized Agent  
→ Tool(s)  
→ SQLite / RAG  
→ Final Answer

### Agents

- `classifier_agent`
- `order_agent`
- `refund_agent`
- `payment_agent`
- `complaint_agent`

### Tools

- `fetch_order_details`
- `check_refund_eligibility`
- `fetch_policy_tool`
- `create_ticket_tool`
- `get_ticket_tool`

### Data Sources

- `orders.db` for order, payment, and refund state
- `tickets.db` for complaint tickets
- policy documents for RAG retrieval

## What the project can answer

### Order questions
- Where is my order ORD1001?
- Has ORD1018 been delivered?
- What is the tracking number for ORD1008?
- When will my order arrive?

### Payment questions
- Why did payment for ORD1004 fail?
- Was my payment successful?
- Which payment method was used?

### Refund questions
- Is ORD1005 eligible for a refund?
- Why was my refund rejected?
- What is your refund policy?
- What are the refund eligibility rules?
- Why is ORD1018 not refundable?

### Complaint questions
- I received the wrong item for ORD1019
- My package arrived empty
- I got a damaged product
- What is the status of ticket TICKET1234?

## Try these sample prompts

- Where is my order ORD1008?
- Why did payment for ORD1004 fail?
- Is ORD1018 eligible for a refund?
- Why is ORD1018 not refundable?
- What is your refund policy?
- I received the wrong item in order ORD1019
- My package arrived empty for ORD1020
- What is the status of ticket TICKET<your_ticket_id>?

## Tech Stack

- Python
- LangGraph
- LangChain
- OpenAI GPT models
- SQLite
- RAG with a vector retriever
- Pydantic
- Gradio

## Why this project is useful

This project demonstrates:

- multi-agent orchestration
- structured tool calling
- SQL-backed state
- retrieval-augmented generation
- complaint escalation workflows
- ticket persistence and duplicate prevention

## Future improvements

- conversation memory
- better ticket lifecycle management
- ticket priority and assignment
- FastAPI backend
- evaluation suite
- improved UI
- deployment to Hugging Face Spaces

## How to run

1. Install dependencies
2. Set up your `.env`
3. Seed the SQLite databases
4. Run `main.py`

## Notes

- Orders are stored in SQLite instead of mock JSON at runtime
- Refund policy answers use RAG for policy context
- Complaint flow creates and retrieves support tickets
