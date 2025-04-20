from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os


pdf_path = Path(__file__).parent / "1706.03762v7.pdf"
# print(pdf_path)

loader = PyPDFLoader(file_path=pdf_path) #  creates a loader for PDF file
docs = loader.load() # loads PDF file and returns a list of Document objects — one for each chunk (usually per page or section, depending on the loader).  the load() gives a list of document. so it is a list datatype
# print(docs[0])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
) # Splits long documents into smaller chunks (important for LLM token limits).
# Breaks PDF into manageable chunks (e.g., 1000 characters with 200 overlap), so each chunk can be embedded and retrieved later.

split_docs = text_splitter.split_documents(documents=docs) # This line takes the list of Document objects you got from the PDF (docs) and splits them into smaller chunks using the text_splitter. 'text_splitter' is helping to split the documents

print("DOCS", len(docs))
print("SPLIT", len(split_docs))

# OpenAIEmbeddings.openai_api_key = os.getenv("OPENAI_API_KEY")
api_key= os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
) # Converts each chunk of text into a vector (list of numbers) using an OpenAI embedding model.

# docker compose -f docker.compose.yml up   before writing this line start docker desktop
# http://localhost:6333/dashboard

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embedder
# ) # Creates a collection with name "learning_langchain" in qdrant

# vector_store.add_documents(documents=split_docs) # Stores embeddings in a Qdrant vector database and helps retrieve similar documents later.
print("Injection Done")

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
) # This connects to already existing Qdrant collection and lets you search it later (like a mini-Google for your PDF!).

relevant_chunks = retriver.similarity_search(
    query="what is Multi-Head Attention?"
) # Finds and returns the most relevant chunks (documents) from the vector store based on similarity to the user query.

print("Relevant Chunks: ", relevant_chunks)



SYSTEM_PROMPT = f"""
You are an helpfull AI Assistant who responds base on the available context

Context:
{relevant_chunks}
"""



# https://cookbook.openai.com/examples/responses_api/responses_api_tool_orchestration
# Topics for blogs
# Parallel Query Retrial (fan out), 
# Reciprocate Rank Fusion,
# Step Back Prompting (algo),
# CoT - Chain of Thought, HyDE - Hypothetical Document Embeddings