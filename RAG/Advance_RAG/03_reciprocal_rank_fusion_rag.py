from dotenv import load_dotenv
import os
from openai import OpenAI
from create_and_store_vector_embeddings import retriver

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)

# https://smith.langchain.com/hub

"""
    Step 0 - Create and store vector embeddings of pdf document
    Step 1 - User gives prompt
    Step 2 - Create System prompt, and generate multiple user prompts
    Step 3. Create vector embeddings of each query and perform similarity search with vector database.
    Step 4. Ranking Relevant Chunks
    Step 5. Use relevant chunks to generate response for original user query
"""

def generate_different_user_prompt(user_input, num_variants=3):
    SYSTEM_PROMPT = f"""
    You are a highly intelligent AI assistant designed to generate diverse and semantically relevant rephrased user prompts.
    Your goal is to improve document retrieval effectiveness by crafting multiple variants of a user's query.

    ### Objective
    Given a single user prompt, generate **3 to 5 unique and meaningful prompts** that either:
    - Rephrase the original query,
    - Explore subtopics or components of the query,
    - Provide alternative ways a user might express the same intent.

    ### Guidelines (Strictly Follow)
    1. Avoid duplicate or semantically identical prompts.
    2. Ensure each prompt is grammatically correct and focused on improving retrieval.
    3. Maintain semantic alignment with the user's original intent.
    4. Never make assumptions outside the scope of the user's query.
    5. Always return **at least 3** and **no more than 5** prompts.
    

    ### Workflow
    1. Carefully analyze the given user query.
    2. Break it down into logical parts if needed.
    3. Consider synonyms, question transformations, or clarifying angles.
    4. Generate diversified prompts.
    5. Stop and wait for the next instruction.

    Original Query: "{user_input}"

    Rewrite this query in {num_variants} different ways:

    ### Example Input
    **User Prompt**: What is Python programming?

    ### Example Output
    1. What is Python?
    2. Can you explain the basics of Python programming?
    3. How does Python work as a programming language?
    4. What are the key features of Python?
    5. Why is Python popular for development?
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

    return cleaned_questions


def get_similar_chunks_from_document(user_input):
    print("\n\n🔄 Generating query variations...\n")
    ai_prompts = generate_different_user_prompt(user_input)

    print("\n\n📄 Generated queries:\n")
    for prompt in ai_prompts:
        print(prompt)

    relevant_chunks_search = [] #  list of lists of chunks
    print("\n\n🔍 Retrieving relevant chunks for each query...\n")
    for prompt in ai_prompts:
        relevant_chunks = retriver.similarity_search(
            query=prompt
        )
        relevant_chunks_search.append(relevant_chunks)
    # print(relevant_chunks_search)

    return relevant_chunks_search


def reciprocal_rank_fusion_algo(rankings, k=60):
    scores = {}  #  stores the RRF score for each document.
    doc_lookup = {}  # maps a document ID to the actual Document so we can return the full object at the end.
    for ranking in rankings:
        for rank, doc in enumerate(ranking):
            doc_id = (doc.page_content, doc.metadata.get("page")) # Create a hashable ID (tuple of content and page for uniqueness)
            scores[doc_id] = scores.get(doc_id, 0)+1/(k+ rank + 1)
            doc_lookup[doc_id] = doc  # Keep a reference to retrieve full doc later
    
    # print("Scores: ", scores)
    # print("ID: ", doc_lookup[doc_id])
    # print("Doc lookup: ", doc_lookup)

    # Sort by RRF score (high to low)
    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(sorted_docs)

    # Deduplicate: keep only best-scoring doc per page
    seen_pages = set()
    final_docs = []
    for doc_id, _ in sorted_docs:
        # print("id: ", doc_id)
        page = doc_id[1] # sorted_docs is tuple so that tuple 1st index position which is page number
        if page not in seen_pages:
            final_docs.append(doc_lookup[doc_id])
            seen_pages.add(page)
    return final_docs

def reciprocal_rank_fusion():
    while True:
        user_input = input("💻 >> ")
        if user_input.lower() in ["exit", "quit"]:
            break

        similar_chunks = get_similar_chunks_from_document(user_input)
        print("\n\n🧹 Filtering unique chunks...\n")
        
        # reciprocal_rank_fusion_algo(similar_chunks)
        fused_docs = reciprocal_rank_fusion_algo(similar_chunks)
        
        for i, doc in enumerate(fused_docs[:5]):  # Print top 5 results with page numbers
            print(f"\n🔹 Rank {i+1} (Page {doc.metadata.get('page')}):\n{doc.page_content}\n")

        # Combine top docs as context text
        context_text = "\n\n".join([
            f"[Page {doc.metadata.get('page', 'Unknown')}]\n{doc.page_content}"
            for doc in fused_docs[:5]
        ])

        SYSTEM_PROMPT = f"""
        You are a helpful AI assistant. Answer the question **only using the context below**.
        If the context does not contain enough information, reply with:
        "I don't know based on the document."

        Include the **exact page number** if information is found.

        
        Question:
        {user_input}
        
        Context:
        {context_text}
        """

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )
        
        print("Answer -----> ", response.choices[0].message.content)
        


reciprocal_rank_fusion()