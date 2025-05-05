from mem0 import Memory
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")
NEO4J_URL= os.getenv("NEO4J_URL")
NEO4J_USERNAME= os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD= os.getenv("NEO4J_PASSWORD")

# mem0 need a config
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "openai",
        "config": {
            "api_key": OPENAI_API_KEY,
            "model": "text-embedding-3-small"
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "gemini-2.0-flash"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QDRANT_HOST,
            "port": 6333
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URL,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD
        }
    }
}

# https://docs.mem0.ai/components/llms/models/gemini
# https://python.langchain.com/docs/how_to/graph_constructing/
# https://python.langchain.com/docs/tutorials/graph/
# https://github.com/mem0ai/mem0/blob/main/mem0/configs/prompts.py

mem_client = Memory.from_config(config)
openai_client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=GEMINI_API_KEY
)

def chat(message):
    mem_result = mem_client.search(query=message, user_id="p123")
    # print(f"\n\n ----- MEMORY ---- {mem_result} \n\n")

    # memories = ""
    # for memory in memories:
    #     memories += f"{str(memory.get("memory"))}: {str(memory.git("score"))}"

    memories = "\n".join(m["memory"] for m in mem_result.get("results"))

    print(f"\n\n ----- MEMORY ---- {memories} \n\n")

    SYSTEM_PROMPT = f"""
        You are a Memory-Aware Fact Extraction Agent, an advanced AI designed to
        systematically analyze input content, extract structured knowledge, and maintain an
        optimized memory store. Your primary function is information distillation
        and knowledge preservation with contextual awareness.

        Tone: Professional analytical, precision-focused, with clear uncertainty signaling
        
        Memory and Score:
        {memories}
    """

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message}
    ]

    result = openai_client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=messages
    )

    messages.append(
        {"role": "assistant", "content": result.choices[0].message.content}
    )

    mem_client.add(messages, user_id="p123")

    return result.choices[0].message.content

while True:
    message = input(">> ")
    print("BOT: ", chat(message=message))