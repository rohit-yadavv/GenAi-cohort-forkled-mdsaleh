from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
from langchain_core.runnables import Runnable

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

# OpenAIEmbeddings.openai_api_key = os.getenv("OPENAI_API_KEY")
api_key= os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)

# docker compose -f docker.compose.yml up   before writing this line start docker desktop
# http://localhost:6333/dashboard

# vector_store = QdrantVectorStore.from_documents(
#     documents=[],
#     url="http://localhost:6333",
#     collection_name="learning_langchain",
#     embedding=embedder
# )

# vector_store.add_documents(documents=split_docs)
print("Injection Done")

retriver = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_langchain",
    embedding=embedder
)

# relevant_chunks = retriver.similarity_search(
#     query="what is Multi-Head Attention?"
# )

# print("Relevant Chunks: ", relevant_chunks)

SYSTEM_PROMPT = """
You are an helpfull AI Assistant who responds base on the available context
If the answer is not found in the context, reply with "I don't know based on the document.

Context:
{context}
"""


api_key = os.getenv("GEMINI_API_KEY")
LLM = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)

# Chat chain = SYSTEM_PROMPT + LLM
# rag_chain: Runnable = SYSTEM_PROMPT | LLM


while True:
    user_input = input("Ask Question: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    relevant_chunks = retriver.similarity_search(query=user_input) # similarity_search() -> returns List of Documents most similar to the query.
    context = "\n".join([doc.page_content for doc in relevant_chunks])
    # response = rag_chain.invoke({
    #     'context': context,
    #     'question': user_input
    # })
    PROMPT = SYSTEM_PROMPT.format(context=context)
    response = LLM.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    print("-----> ", response.choices[0].message.content)