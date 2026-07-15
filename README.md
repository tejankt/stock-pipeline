Real-Time Stock Data Engineering Pipeline 🚀
An end-to-end data pipeline that extracts real-time stock market data from a financial API, processes it using Pandas, loads it into a local PostgreSQL database running in Docker, and performs analytical queries using SQL inside interactive Jupyter Notebooks.

🛠️ Tech Stack
Language: Python 3.14

Libraries: Pandas, SQLAlchemy, Matplotlib, LangChain, Streamlit

Database: PostgreSQL (Dockerized)

Environment: VS Code & Jupyter Notebooks

⚙️ Architecture & Features
Extraction: Pulls live financial data stream (JSON).

Transformation: Cleaned and structured using Pandas.

Load: Automatically writes to a local Postgres database container.

Analytics: Built-in SQL script (analyze_all.py) and a Jupyter Notebook (playground.ipynb) to calculate moving averages, track capital flow, and visualize price trends using Matplotlib.

🤖 AI Database Agent
You can now interact with your stock database using plain English via a web-based chat interface.

How to run the AI Agent
Ensure your PostgreSQL container is running:

Bash
docker start stock-db
Launch the Web Interface:

Bash
python -m streamlit run app.py
Chat: Open http://localhost:8501 in your browser to ask questions like "What is the latest stock price for AAPL?".

Dependencies
Ensure you have installed the additional AI libraries:

Bash
pip install streamlit langchain langchain-community langchain-ollama