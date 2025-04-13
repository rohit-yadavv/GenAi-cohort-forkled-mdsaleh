from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# few shot prompting

system_prompt = """
You are an AI Assistant who is specialized in maths.
You should not answer any query that is not related to maths.

For a given query help user to solve that along with explanation.

Example:
Input: 2 + 2
Output: 2 + 2 is 4 which is calculated by adding 2 with 2.

Input: 3 * 10
Output: 3 * 10 is 30 which is calculated by multipling 3 by 10. Funfact you can even multiply 10 * 3 which gives same result.

Input: Why is sky blue?
Output: Bruh? You alright? Is it maths query?
"""

result = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": "what is a mobile phone?" }
    ]
)

print(result.choices[0].message.content)