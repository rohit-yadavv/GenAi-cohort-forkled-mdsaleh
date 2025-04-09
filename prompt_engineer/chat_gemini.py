from dotenv import load_dotenv
from google import genai
from google.genai import types

# https://github.com/googleapis/python-genai

load_dotenv()

client = genai.Client("api_key")

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)

# zero shot prompting
# system prompt -> it is very important because jo output hai oh system prompt me depend hoti hai initally
# few shot prompting -> very important
# Chain of Thaught


# self-consistency prompting -> The model generates multiple responses and selects the most consistent or common answer.  this type mostly used when we do research work
# persona-based prompting -> he model is instructed to respond as if it were a particular character or professional
# You are Hitesh sir [Background]
# Tone:
# Hanji!
# Hinglish
# give Examples:

# role-play prompting -> You are an Al coding assistant who is expert in teaching how to code.    The model assumes a specific role and interacts accordingly.
# CoT + Persona + Role

# these both are real coding part and advance part
# Contextual prompting
# Multimodal prompting


"""
Prompting
Zero-shot Prompting: The model is given a direct question or task without prior examples.
Few-shot Prompting: The model is provided with a few examples before asking it to generate a response.
Chain-of-Thought (CoT) Prompting: The model is encouraged to break down reasoning step by step before arriving at an answer.
Self-Consistency Prompting: The model generates multiple responses and selects the most consistent or common answer.
Instruction Prompting: The model is explicitly instructed to follow a particular format or guideline.
Direct Answer Prompting: The model is asked to give a concise and direct response without explanation.
Persona-based Prompting: The model is instructed to respond as if it were a particular character or professional.
Role-Playing Prompting: The model assumes a specific role and interacts accordingly.
Contextual Prompting: The prompt includes background information to improve response quality.
Multimodal Prompting: The model is given a combination of text, images, or other modalities to generate a response.


"""