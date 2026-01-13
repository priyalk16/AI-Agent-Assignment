# AutoStream Social to Lead Agent

This repository contains a conversational AI agent built for **AutoStream**, a fictional SaaS product that provides automated video editing tools for content creators.  
The agent demonstrates how social media conversations can be converted into qualified business leads using intent detection, retrieval augmented generation (RAG), and controlled tool execution.

---

## 🚀 How to Run the Project Locally

### Prerequisites
- Python 3.9+
- Git

### Steps
```bash
git clone <your-github-repo-url>
cd autostream-agent
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py


### Architechture Explanation 

This project uses LangGraph to implement a stateful, agentic workflow for lead generation. LangGraph was chosen because it provides explicit control over conversation state, decision making, and execution flow, which is critical for real world business agents.

The agent maintains a shared state across multiple conversation turns, allowing it to remember user intent, previously shown information, and collected lead details such as name, email, and creator platform. Intent detection is used to classify user messages into greetings, product inquiries, or high intent actions.

Product related questions are answered using a Retrieval Augmented Generation (RAG) approach, where responses are grounded in a local knowledge base stored as JSON. This ensures accurate and consistent answers without hallucination.

When a user shows high intent after viewing pricing information, the agent transitions into a lead qualification flow. A mock lead capture tool is executed only after all required details are collected, ensuring safe and deterministic tool invocation


###WhatsApp Integration 

To integrate this agent with WhatsApp, a webhook based architecture would be used. Incoming WhatsApp messages would be received through the WhatsApp Business API or Twilio WhatsApp Sandbox and forwarded to the agent backend. Each user’s phone number would map to a unique session state. The agent’s response would then be sent back to the user using the WhatsApp Send Message API. This approach allows the same agent logic to operate across chat-based platforms.