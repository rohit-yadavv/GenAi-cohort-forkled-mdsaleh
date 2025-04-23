from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore

load_dotenv()


pdf_path = Path(__file__).parent / "1706.03762v7.pdf"
# print(pdf_path)

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load() # the load() gives a list of document. so it is a list datatype
# print(docs[0])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

split_docs = text_splitter.split_documents(documents=docs)

print("DOCS", len(docs))
print("SPLIT", len(split_docs))


api_key= os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)



# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain_PQR",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
# print("Injection Done")

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain_PQR",
    embedding=embedder
)

# relevant_chunks = retriver.similarity_search(
#     query="what is Multi-Head Attention?"
# )

# print("Relevant Chunks: ", relevant_chunks)