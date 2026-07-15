from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.tools.retriever import create_retriever_tool
from langchain.agents import create_agent

# 1. Setup Model
llm = ChatOllama(model="qwen2.5:7b", temperature=0)

# 2. Setup SQL Database
db = SQLDatabase.from_uri("postgresql://admin:supersecretpassword@localhost:5432/stock_data")

# 3. Setup Tools
# SQL Tools
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
sql_tools = toolkit.get_tools()

# Vector/RAG Tool
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = PGVector(
    connection_string="postgresql://admin:supersecretpassword@localhost:5432/stock_data",
    embedding_function=embeddings,
    collection_name="financial_reports"
)
retriever = vector_store.as_retriever()
rag_tool = create_retriever_tool(
    retriever, 
    "financial_reports_search", 
    "Use this tool to search through PDF reports and financial news for qualitative insights."
)

# 4. Combine Tools
all_tools = sql_tools + [rag_tool]

# 5. Create Agent (using langgraph prebuilt)
agent_executor = create_agent(llm, all_tools)

# Temporary test to see if the agent responds
try:
    response = agent_executor.invoke({"messages": [("human", "What is the price of AAPL?")]})
    print("Agent Test Success!")
    print(response)
except Exception as e:
    print(f"Agent execution failed: {e}")