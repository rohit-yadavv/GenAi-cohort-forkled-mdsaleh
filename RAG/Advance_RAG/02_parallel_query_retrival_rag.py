from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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


api_key= os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)

# api_key= os.getenv("GEMINI_API_KEY")
# embedder = GoogleGenerativeAIEmbeddings(
#     model="textembedding-gecko@001",
#     # api_key=api_key
#     api_key="AIzaSyDGO89aiKLl6-Tvf_SB_nurGLcw5kD58OQ"
# )

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

api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)



def generate_different_user_prompt(user_input, num_variants=3):
    SYSTEM_PROMPT = f"""
    You are an helpfull AI Assistant that rewrites user input queries in different forms for the better document retrieval

    Original Query: "{user_input}"

    Rewrite this query in {num_variants} different ways:

    If the answer is not found in the context, reply with "I don't know based on the document.
    """

    different_qurey = []
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    different_qurey.append(response.choices[0].message.content)

    # Split the first string into lines so we did different_query[0], remove 1234567890, and skip empty lines so we did line.strip()
    cleaned_questions = [line.strip("1234567890.") for line in different_qurey[0].split('\n') if line.strip()]
    # print(cleaned_questions)
    return cleaned_questions

    # for query in cleaned_questions:
    #     print(query)
        
    # print(different_qurey)
    # print(cleaned_questions)


def get_similar_chunks_from_document(user_input):
    ai_prompts = generate_different_user_prompt(user_input)
    relevant_chunks_search = []
    for index, prompt in enumerate(ai_prompts):
        # print(prompt)
        relevant_chunks = retriver.similarity_search(
            query=prompt
        )
        # print(ai_prompts)
        relevant_chunks_search.append(relevant_chunks)
        # print(f"*********** {index} prompt chunk: ************ \n{relevant_chunks_search}")
    return relevant_chunks_search



# get_similar_chunks_from_document("application of positional encoding")

def parallel_query_retrieval():
    while True:
        user_input = input(">> ")
        if user_input.lower() in ["exit", "quit"]:
            break
        similar_chunks = get_similar_chunks_from_document(user_input)
        # print("\n\nSMILAR CHUNKS: ", similar_chunks)
        seen_contents = set()
        filter_unique_chunks = []
        for chunk in similar_chunks: # can be nested list
            for docs in chunk:
                content = docs.page_content
                # print(content)
                if content not in seen_contents:
                    seen_contents.add(content)
                    # print("seen_contents: ", list(seen_contents))
                    filter_unique_chunks.append(chunk) # Only adds the actual chunk (the full object with metadata, etc.) to the final list if it's the first time we see that content.

        # print("************ Filtered Unique Chunks ************")
        # # for u_chunk in filter_unique_chunks:
        #     # print(u_chunk)
        # print(filter_unique_chunks)
        # print("************************************************")

        SYSTEM_PROMPT = f"""
        You are an helpfull AI Assistant who responds base on the available context
        If the answer is not found in the context, reply with "I don't know based on the document.

        Context:
        {seen_contents}
        """

        # context = "\n".join([doc.page_content for doc in similar_chunks])
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        
        print("-----> ", response.choices[0].message.content)


parallel_query_retrieval()








# The enumerate() function adds a counter to an iterable (like a list, tuple, or string) so you can get both the index and the item in a loop.
# enumerate(iterable, start=0)
# iterable: The list or string you want to loop over.
# start: (optional) The starting index (default is 0).


# It adds the item to the set if it's not already there, but importantly:
# set.add() returns None.
# It modifies the set in-place, but doesn't return anything useful to capture or check. 