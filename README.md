# E-Commerce Customer Support Agent (LangGraph)

## Overview

This project is an Agentic AI-powered customer support system for an e-commerce platform.

The system routes customer queries to specialized support agents and uses tool calling with SQLite-backed data storage to provide accurate responses.

Unlike traditional chatbots, the agent can perform actions such as checking order status, verifying refund eligibility, creating support tickets, and retrieving ticket details.

---

## Features

### Order Support Agent

Handles order-related queries such as:

* Where is my order?
* Has my order been delivered?
* What is my tracking information?

Uses tool calling to fetch order information directly from SQLite.

---

### Refund Support Agent

Handles refund-related requests:

* Is my order eligible for a refund?
* Why was my refund rejected?
* What is my refund status?

Applies business rules and eligibility checks before responding.

---

### Payment Support Agent

Handles payment-related queries:

* Why did my payment fail?
* Was my payment successful?
* Which payment method was used?

Uses order data stored in SQLite.

---

### Complaint Support Agent

Handles customer complaints that cannot be resolved automatically.

Examples:

* Wrong item delivered
* Empty package received
* Damaged product
* Missing items

The agent can:

* Create support tickets
* Prevent duplicate ticket creation
* Retrieve ticket details
* Track ticket status

---

## Architecture

User Query
↓
Classifier Agent
↓
├── Order Agent
├── Refund Agent
├── Payment Agent
└── Complaint Agent
↓
Tools
↓
SQLite Databases

---

## Databases

### orders.db

Stores:

* Order Details
* Payment Information
* Shipping Information
* Refund Information

### tickets.db

Stores:

* Ticket ID
* Order ID
* Complaint Description
* Ticket Status
* Created Date

---

## Tech Stack

* Python
* LangGraph
* LangChain
* OpenAI GPT Models
* SQLite
* Pydantic
* Structured Tool Calling

---

## Example Queries

### Order Tracking

Where is my order ORD1001?

### Refund Eligibility

Is ORD1005 eligible for a refund?

### Payment Support

Why did payment for ORD1004 fail?

### Complaint Handling

I received the wrong item for ORD1019.

### Ticket Tracking

What is the status of ticket TICKET123?

---

## Key Learning Outcomes

* Agent Routing using LangGraph
* Tool Calling
* Structured Outputs
* Multi-Agent Architectures
* SQLite Integration
* Stateful Workflows
* Ticket Lifecycle Management
* Customer Support Automation

---

## Future Improvements

* Conversation Memory
* FastAPI Backend
* Human-in-the-loop Approval Flows
* Ticket Priority Management
* Agent Evaluation Framework
* PostgreSQL Migration
