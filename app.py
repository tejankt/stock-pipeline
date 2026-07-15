import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.vectorstores import PGVector
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.tools.retriever import create_retriever_tool
from langchain.agents import create_agent

# Page configuration
st.set_page_config(page_title="AI Hybrid Agent 📈", page_icon="🤖", layout="wide")
st.title("🤖 Chat with Your Stock Database & Reports")

@st.cache_resource
def initialize_agent():
    # 1. Setup Model
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)

    # 2. Setup SQL Database
    DATABASE_URL = "postgresql://admin:supersecretpassword@localhost:5432/stock_data"
    db = SQLDatabase.from_uri(DATABASE_URL)
    
    # 3. Setup SQL Tools
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tools = toolkit.get_tools()
    
    # 4. Setup Vector/RAG Tool
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = PGVector(
        connection_string=DATABASE_URL,
        embedding_function=embeddings,
        collection_name="financial_reports"
    )
    rag_tool = create_retriever_tool(
        vector_store.as_retriever(), 
        "financial_reports_search", 
        "Search financial reports and news."
    )
    
    # 5. Combine and Create Hybrid Agent
    all_tools = sql_tools + [rag_tool]
    agent_executor = create_agent (llm, all_tools)
    
    return agent_executor 

# Initialize the agent
try:
    agent_executor = initialize_agent()
except Exception as e:
    st.error(f"Could not connect: {e}")
    st.stop()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! Ask me anything about your stock prices database."}
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor.invoke({"messages": [("human", prompt)]})
            output_text = response["messages"][-1].content
            st.write(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})