from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

result = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "user", "content": "What is greator? 9.8 or 9.11" } # Zero Shot Prompting
    ]
)

print(result.choices[0].message.content)