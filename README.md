# MCP-based Intelligent Tool Integration System

A final year internship project built at HCL Technologies.

## What it does
An AI-powered assistant that uses the **Model Context Protocol (MCP)** 
to intelligently route user queries to the right tool.

## Tools Available
- 🌤️ **Weather** — Live weather for any city
- 💱 **Currency Converter** — Live exchange rates
- 📰 **News Search** — Latest headlines on any topic
- 😊 **Sentiment Analysis** — Positive/Negative text analysis
- 💰 **Expense Tracker** — Add and track expenses

## Tech Stack
- Python 3.13
- MCP SDK
- Groq AI (LLaMA 3)
- HuggingFace Transformers
- Streamlit
- SQLite

## How to Run

1. Clone the repo
2. Create virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Add your API keys to `.env`
5. Run: `streamlit run frontend/app.py`

## Author
Samdeesh Singh | Roll No. 102203005 | Thapar Institute of Engineering & Technology