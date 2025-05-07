from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.schema import SystemMessage
import os

load_dotenv()



class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool()
def run_command(command: str):
    """
        Takes a command line prompt and executes it on the user's machine and returns the output of the command.
        Example: run_command(cmd="ls") where ls is the command to list the files.
    """
    return os.system(command=command)


llm = init_chat_model(model="gpt-4o-mini", model_provider="openai") 
llm_with_tool = llm.bind_tools(tools=[run_command])

# SYSTEM_PROMPT = ""

def chatbot(state: State):
    # messages = llm.invoke(state["messages"])
    system_prompt = SystemMessage(content="""
        You are an AI Coding Assistant who takes an input from user and based on tools you choose the correct tool and execute the commands.
        
        You can even execute commands and help user with the output of the command. 

        Always make sure to keep your generated codes and files in chat_gpt/ folder. you can create one if not already there.

    """)
    messages = llm_with_tool.invoke([system_prompt] + state["messages"])
    assert len(messages.tool_calls) <= 1
    return {"messages": [messages]}


tool_node = ToolNode(tools=[run_command]) 

graph_builder = StateGraph(State)
# as of now we have 2 nodes before run_command tool chatbot node and tool node
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
# start then jaao chatbot pe and conditional edge agr tool call hai to tools pe jaao and udhar loop hota rahega toh tools se chabot pe jaao nhi to end ho jao chatbot se
graph_builder.add_edge("chatbot", END)


# we not using here simple graph instead of we using graph with checkpointer
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)