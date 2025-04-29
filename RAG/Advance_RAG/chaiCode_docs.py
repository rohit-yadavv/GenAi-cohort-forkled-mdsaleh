from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from collections import defaultdict
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

# Load the base page
url = "https://chaidocs.vercel.app/youtube/getting-started"
loader = WebBaseLoader(web_path=url)
soup = loader.scrape()
# print(soup)

base_url = "https://chaidocs.vercel.app"
links = set()

# Grab all sidebar links
for a_tag in soup.select("details ul li a[href]"):
    href = a_tag["href"]
    # print(href)
    if href.startswith("/"):
        full_url = base_url + href   # e.g: https://chaidocs.vercel.app/youtube/chai-aur-html/welcome/
        links.add(full_url)

all_urls = [url] + list(links)
# print(all_urls)




# Print loaded URLs
# print("Final URL list:")
# for u in all_urls:
#     print(u)

# Load all pages
# loader = WebBaseLoader(web_paths=all_urls)
# docs = loader.load()
# print("Total docs loaded:", len(docs))

# 📄 scrape(): Returns raw HTML (BeautifulSoup object) to manually extract links or data
# 📚 load(): Returns LangChain Document objects with clean text & metadata (for RAG)

topic_urls = defaultdict(list) # defaultdict(list) is like a normal dictionary (dict), but it automatically creates an empty list for any new key the first time it’s used.

for link in all_urls:
    url_parts = link.split("/")  # ['https:', '', 'chaidocs.vercel.app', 'youtube', 'chai-aur-html', 'welcome']
    if "chai-aur" in url_parts[4]:
        topic = url_parts[4] # chai-aur-html, chai-aur-git, etc.
        topic_urls[topic].append(link) # add this (link) URL to the list of URLs under that topic in our dictionary.

# print(topic_urls)


api_key= os.getenv("OPENAI_API_KEY")
embedder = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key
)

for topic, url in topic_urls.items():
    print(f"Processing Topic {topic}")
    print(url)

    # load documents
    loader = WebBaseLoader(web_paths=url)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = text_splitter.split_documents(documents=docs)

    print("DOCS", len(docs))
    print("SPLIT", len(split_docs))

    # vector_store = QdrantVectorStore.from_documents(
    #     documents=[],
    #     url="http://localhost:6333",
    #     collection_name=topic,
    #     embedding=embedder
    # )

    # vector_store.add_documents(documents=split_docs)
    # print("Injection Done")

    

    
api_key = os.getenv("GEMINI_API_KEY")
LLM = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)

def classify_topic(user_input):
    topics = list(topic_urls.keys())

    SYSTEM_PROMPT = f"""
        You are a smart topic classifier.

        Based on the user's query and the list of available topics below, select the **most relevant topic** that best matches the intent.

        Topics:
        {topics}

        User Query:
        "{user_input}"

        Return **only** the topic name from the list above. Do not include any explanations or extra text.
        """
    
    response = LLM.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    # print("-----> ", response.choices[0].message.content)
    return response.choices[0].message.content


# classify_topic("hello world code for c++ and javacript?")

SYSTEM_PROMPT = """
    You are a helpful AI Assistant who responds based on the available context and also give the source from where you get the information
    If the answer is not found in the context, reply with "I don't know based on the document."

    Context:
    {context}
"""

while True:
    user_input = input("👤 Ask Question: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    topic = classify_topic(user_input)
    print(f">> Routed to topic: {topic}")

    retriver = QdrantVectorStore.from_existing_collection(
        url="http://localhost:6333",
        collection_name=topic,
        embedding=embedder
    )

    relevant_chunks = retriver.similarity_search(query=user_input)
    print(relevant_chunks)
    context = "\n".join([f"{doc.page_content}\n\n Source: {doc.metadata["source"]}" for doc in relevant_chunks])
    formatted_prompt = SYSTEM_PROMPT.format(context=context)

    response = LLM.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": formatted_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    print("----->", response.choices[0].message.content)
