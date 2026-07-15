# Real-Time Stock Data Engineering Pipeline 🚀

An end-to-end data pipeline that extracts real-time stock market data from a financial API, processes it using **Pandas**, loads it into a local **PostgreSQL database running in Docker**, and performs analytical queries using **SQL** inside interactive **Jupyter Notebooks**.

## 🛠️ Tech Stack
* **Language:** Python 3.14
* **Libraries:** Pandas, SQLAlchemy, Matplotlib, LangChain, Streamlit
* **Database:** PostgreSQL (Dockerized)
* **Environment:** VS Code & Jupyter Notebooks

## ⚙️ Architecture & Features
1. **Extraction:** Pulls live financial data stream (JSON).
2. **Transformation:** Cleaned and structured using Pandas.
3. **Load:** Automatically writes to a local Postgres database container.
4. **Analytics:** Built-in SQL script (`analyze_all.py`) and a Jupyter Notebook (`playground.ipynb`) to calculate moving averages, track capital flow, and visualize price trends using Matplotlib.
# 🧠 Hybrid RAG Architecture
This project implements a powerful Hybrid Agent that combines structured data analysis with unstructured document intelligence.

How it works:
Structured Data (SQL): The agent utilizes SQLDatabaseToolkit to interact directly with your PostgreSQL database, allowing it to perform precise calculations, filtering, and aggregation on stock market data.

Unstructured Data (RAG): We have integrated a Retrieval-Augmented Generation (RAG) pipeline using PGVector and OllamaEmbeddings. This allows the agent to ingest and search through financial reports, news articles, and PDFs to provide context-aware answers.

Intelligent Orchestration: Using langgraph's create_react_agent, the system acts as an orchestrator. When you ask a question, the agent dynamically decides whether to query the database for exact facts or perform a semantic search through stored reports to provide a comprehensive response.

Why this matters:
By combining these two approaches, the agent overcomes the limitations of traditional chatbots. It can answer both quantitative questions ("What was the closing price of AAPL?") and qualitative questions ("What are the risks mentioned in recent quarterly reports?") in a single, unified interface.

## 🤖 AI Database Agent
You can now interact with your stock database using plain English via a web-based chat interface.

### How to run the AI Agent
1. **Ensure your PostgreSQL container is running:**
   ```bash
   docker start stock-db

### Launch the Web Interface:
```Bash
python -m streamlit run app.py
Chat: Open http://localhost:8501 in your browser to ask questions like "What is the latest stock price for AAPL?".

### Dependencies
Ensure you have installed the additional AI libraries:
```Bash
pip install streamlit langchain langchain-community langchain-ollama