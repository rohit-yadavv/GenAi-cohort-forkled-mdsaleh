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



""" 
    Step 0 - Create and store vector embeddings of pdf document
    Step 1 - User gives prompt
    Step 2 - Create System prompt, and generate multiple user prompts
    Step 3. Chaining of prompts and responses
    Step 4. Use relevant subquery responses to generate response for original user query
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

    relevant_chunks_search = []
    print("\n\n🔍 Retrieving relevant chunks for each query...\n")
    for prompt in ai_prompts:
        relevant_chunks = retriver.similarity_search(
            query=prompt
        )
        relevant_chunks_search.append(relevant_chunks)
    # print(relevant_chunks_search)
    return relevant_chunks_search
