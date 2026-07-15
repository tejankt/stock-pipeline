import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama
from langchain_community.agent_toolkits import create_sql_agent

# Page configuration
st.set_page_config(page_title="AI Database Agent 📈", page_icon="🤖", layout="wide")
st.title("🤖 Chat with Your Stock Database")
st.markdown("Query your Postgres `pgvector` container using plain English.")

# Initialize the Database & LLM only once (Cached to avoid reloading on every message)
@st.cache_resource
def initialize_agent():
    DATABASE_URL = "postgresql://admin:supersecretpassword@localhost:5432/stock_data"
    db = SQLDatabase.from_uri(DATABASE_URL)
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
    
    agent = create_sql_agent(
        llm=llm, 
        db=db, 
        verbose=True,
        agent_type="tool-calling",
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    return agent

try:
    agent_executor = initialize_agent()
except Exception as e:
    st.error(f"Could not connect to database/Ollama: {e}")
    st.stop()

# Initialize conversational session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! Ask me anything about your stock prices database."}]

# Display past chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input(placeholder="e.g., How many records are inside raw_stock_prices?"):
    # Show user message instantly
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Call AI agent and display response with a loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Analyzing database schema and writing SQL..."):
            try:
                response = agent_executor.invoke({"input": prompt})
                output_text = response["output"]
                st.write(output_text)
                st.session_state.messages.append({"role": "assistant", "content": output_text})
            except Exception as e:
                error_msg = f"An error occurred while executing the query: {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})