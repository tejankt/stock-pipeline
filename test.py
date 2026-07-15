from langchain_postgres import PGVector
from langchain_ollama import OllamaEmbeddings

# Configuration
connection_string = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"
collection_name = "financial_reports"
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Initialize the vector store
vector_store = PGVector(
    embeddings=embeddings,
    collection_name=collection_name,
    connection=connection_string,
)
from langchain_core.documents import Document
docs = [
    Document(
        page_content="Apple reported a revenue increase of 8% this quarter, driven by strong iPhone sales in emerging markets.",
        metadata={"ticker": "AAPL", "report_type": "quarterly"}
    ),
    Document(
        page_content="NVIDIA continues to see massive demand for AI chips, resulting in a 200% year-over-year growth in data center revenue.",
        metadata={"ticker": "NVDA", "report_type": "quarterly"}
    ),
    Document(
        page_content="Tesla's operating margins were pressured by aggressive price cuts, despite record-breaking vehicle delivery numbers.",
        metadata={"ticker": "TSLA", "report_type": "quarterly"}
    )
]
vector_store.add_documents(docs)

# Perform a test similarity search
results = vector_store.similarity_search("financial performance", k=1)
print(f"Found {len(results)} relevant document(s):")
for doc in results:
    print(doc.page_content)