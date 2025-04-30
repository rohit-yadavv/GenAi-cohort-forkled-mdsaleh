import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=api_key
)

# def run_command(command):
#     os.system(command=command)

# Create a new directory or folder
def make_directory(directory_name):
    try:
        os.makedirs(directory_name)
        return f"Directroy created {directory_name}"
    except FileExistsError:
        return "Directroy already exists"
    except Exception as e:
        return f"Error {e}"

# Creates new file with file content
def make_file(data):
    file_name = data["file_name"]
    file_content = data["file_content"]

    if not file_name:
        return "File name is required to create file"
    if not file_content:
        return "File content is required to create file"

    try:
        with open(file_name, "w") as file:
            file.write(file_content)
    except FileExistsError:
        return f"File already exists {file_name}"
    except Exception as e:
        return f"Error: {e}"


# Deletes a directory
def delete_directory(directory_name):
    try:
        os.rmdir(directory_name)
        return f"Directory deleted: {directory_name}"
    except FileNotFoundError:
        return f"Directory not exists: {directory_name}"
    except Exception as e:
        return f"Error: {e}"


# Change current working directory
def change_directory(directory_name):
    try:
        os.chdir(directory_name)
        return f"Directory changed: {directory_name}"
    except FileNotFoundError:
        return f"Directory not exists: {directory_name}"
    except Exception as e:
        return f"Error: {e}"


def create_vite_app(data):
    project_name = data["project_name"] or "."
    vite_template = data["vite_template_name"] or "react"
    try:
        os.system(
            f"npm create vite@latest {project_name} -- --template {vite_template}"
        )
        return f"Project setup completed using vite {vite_template} template command: {project_name}"
    except Exception as e:
        return f"Error: {e}"


def run_command(command):
    try:
        os.system(command)
        return f"Command successfully executed: {command}"
    except Exception as e:
        return f"ERror: {e}"
    
available_tools = {
    "make_directory": make_directory,
    "make_file": make_file,
    "delete_directory": delete_directory,
    "change_directory": change_directory,
    "create_vite_app": create_vite_app,
    "run_command": run_command,
}

SYSTEM_PROMPT = """
You are a helpful AI Assistant and your task is to help build web application based on user query and available tools.
You wait for the user to provide his query or requirements and once the user provide the query, then based on the user query, first you start planning -> use the available tools to perform action -> after action, you observe the output -> and last you provide the actual output and end the process or steps.

Your typical workflow will look like this:
user query -> plan -> action -> observe -> output 

Strict JSON Format: 
{
    "step": "plan" | "action" | "observe" | "output",
    "content": "string"
    "function": "name of the function, if the step is action"
    "input": "input parameter for function (if the step is action)"    
}  


Rules:
- You wait for the user to enter his query.
- You always have to follow Strict Output JSON Format
- You carefully analyze user query, after analyzing, your first step is planning based analyzations and available tools
- You always perform one step at a time
- If the step is action, you always observe the output, that you got after performing the action step
- If the user ask you other than coding then do not do anything and reply with output step with relevant answer
- If the directory or file already exists, then you you delete it first and create a new one and work one same directory or file
- You work on current working directory and not create another directory until the user said to create a directory and - if you create new directory then change the current working directory to that new directory by using available tool
- If you are changing directory and that directory is not exists, then create it and then do change directory into it
- If you are creating a website in reactjs, so you have to find the project name on the basis of user query
- If you find anything wrong related to security in the command, given by user then do not run it and output the with some message 
- If you received query to make component or write styling,so you always create folder in a src/components/component_name/component_name.jsx and if you have to write styling for this component write in same folder(src/components/component_name) by creating a component_name.css and based classes you have created in css file updated the components className attribute and use that components in relevant components like App  

Available Tools: 
- make_directory(directory_name: string): Takes directory name as input and create a directory within the current working directory
- make_file({{file_name: string, file_content: string}}): Takes two input as dictionary with property, file_name as string and file_content which is also a type of string and creates the file. 
- delete_directory((directory_name: string): Take directory name as input and delete it from current working directory
- change_directory(directory_name: string): Takes directory name as input and change the working directory 
- create_vite_app({{project_name: string, vite_template_name: string}}): Takes two input as dictionary with property project_name and vite_template_name and creates the folder structure
- run_command(command: string): Takes a valid command as input and execute it in the terminal

Example:
User: Create a react js website 
{ "step": "plan", "content": "The user is interested in creating a website in react js, i should use vite to create folder structure" }
{ "step": "plan", "content": "From the available tools, i should call create_vite_app" }
{ "step": "action", "function": "run_command", "input": {project_name, 'react' or if user is asking to react typescript application then 'react-ts'} }
{ "step": "observe", "content": "React project setup created: project_name" }
{ "step": "plan", "content": "From the available tools, i should again call change_directory to change the working directory to vite project that we have created and call run_command to install dependencies" }
{ "step": "action", "function": "change_directory", "input": "project_name" }
{ "step": "observe", "content": "Directory changed: project_name" }
{ "step": "action", "function": "run_command", "input": "npm install" }
{ "step": "observe", "content": "Dependencies installed" }
{ "step": "output", "content": "Now, you can run the project: npm run dev" }


User: Create a portfolio website using html, css and js
{ "step": "plan", "content": "The user is interested in making a portfolio website by using html, css and javaScript" }
{ "step": "plan", "content": "From the available tools, i should call make_directory to create a folder name portfolio" }
{ "step": "action", "function": "make_directory", "input": "portfolio" }
{ "step": "observe", "content": "Directory created: portfolio" }
{ "step": "plan", "content": "From the available tools, i should call make_file to create files: index.html, style.css and script.js" }
{ "step": "action", "function": "make_file", "input": {index.html, file_content} }
{ "step": "action", "function": "make_file", "input": {style.css, file_content} }
{ "step": "action", "function": "make_file", "input": {script.js, file_content} }
{ "step": "observe", "content": "Files created with file content: index.html, style.css and script.js" }
{ "step": "output", "content": "Your portfolio website is ready" }

"""

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

#*   json.dumps() ---> Convert Python object to JSON string.   This is useful when you want to store or transmit data in JSON format.

#*  json.loads() ---> Convert JSON string to Python object.   Useful for reading JSON strings (e.g., from a file or API response) into Python dictionaries.


while True:
    query = input("You: ")
    if not query.strip():
        break

    messages.append({"role": "user", "content": query})

    while True:
        res = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=messages,
            response_format={"type": "json_object"},
        )

        parsed_output = json.loads(res.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
        step = parsed_output.get("step")

        if step == "output":
            print(f"{parsed_output.get("content")}")
            break
        elif step == "plan":
            print(f"{parsed_output["content"]}")
            continue
        elif step == "action":
            inp = parsed_output.get("input")
            func = parsed_output.get("function")

            if func in available_tools:
                output = available_tools[func](inp)
                messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps({"step": "observe", "content": output}),
                    }
                )
                continue
            else:
                messages.append(
                    {
                        "role": "assistant",
                        "content": json.dumps(
                            {
                                "step": "observe",
                                "content": f"Tool not exists: {func}",
                            }
                        ),
                    }
                )
                continue



















# while True:
#     user_input = input(">> ")
#     messages.append({"role": "user", "content": user_input})


#     while True:
#         time.sleep(5)
#         resposne = client.chat.completions.create(
#             model="gemini-2.0-flash",
#             messages=messages,
#             response_format={"type": "json_object"}
#         )

#         try:
#             parsed_output = json.loads(resposne.choices[0].message.content)
#         except Exception as e:
#             print("Error: ", e)
        
#         # print(parsed_output)
#         step = parsed_output["step"]

#         if step == "plan":
#             print(f"{parsed_output["content"]}")
#             messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
#             continue

#         if step == "action":
#             func_name = parsed_output["function"]
#             func_input = parsed_output["input"]

#             if func_name in available_tools:
#                 result = available_tools[func_name](func_input) # function execution from available tools. func_input is a argument for a function
#                 obs = {"step": "observe", "content": result}
#                 messages.append({"role": "assistant", "content": json.dumps(obs)})
#                 continue
#             else:
#                 obs = {"step": "observe", "content": "Tool name does not exists"}
#                 messages.append({"role": "assistant", "content": json.dumps(obs)})
#                 continue

#         if step == "output":
#             print(f"{parsed_output["content"]}")
#             break