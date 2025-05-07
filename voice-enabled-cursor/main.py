import speech_recognition as sr
from langgraph.checkpoint.mongodb import MongoDBSaver
from graph import create_chat_graph
import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI()

MONGODB_URI = "mongodb://localhost:27017"
config = {"configurable": {"thread_id": "8"}}

# https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
def main():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph = create_chat_graph(checkpointer=checkpointer)


        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 2

            while True:
                print("Say something!")
                audio = r.listen(source)

                print("Processing audio")
                speech_to_text = r.recognize_google(audio)
                
                print("You Said: " + speech_to_text)
                for event in graph.stream({"messages": [{"role": "user", "content": speech_to_text}]}, config=config, stream_mode="values"):
                    if "messages" in event:
                        event["messages"][-1].pretty_print()


# https://platform.openai.com/docs/guides/text-to-speech#streaming-realtime-audio
async def speak(text: str):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)

# main()


if __name__ == "__main__":
    asyncio.run(speak("This is the sample voice hi saleh"))




# A symlink (symbolic link) is like a shortcut or pointer to another file.
# It lets you access a file (like .env) from a different location without copying it.
# Useful for sharing a single config file across folders, e.g., app/.env → ../.env
# when you make changes in that it also change in that file which is linked