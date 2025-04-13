import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
import threading
import requests
from groq import Groq

load_dotenv()
Groq.api_key = os.getenv("GROQ_API_KEY")
client = Groq()
# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key= os.getenv("OPENROUTER_API_KEY")
# )

def query_db(sql):
    pass

# def run_command(command):
#     result = os.system(command=command)
#     return result


running_processes = {}

dangerous_keywords = [
    "rm", "sudo", "shutdown", "reboot", "mkfs", ">:",
    "init 0", "init 6", "halt", "poweroff", "dd", ":(){ :|: & };:", "forkbomb",
    "killall", "kill -9", "mv /", "chmod 000", "chown root", ">/dev/sda",
    ">/dev/sda1", ">/dev/sdb", ">/dev/null", "echo > /etc/passwd",
    "echo > /etc/shadow", "rm -rf", "mkfs.ext4", "mkfs.btrfs", "crontab -r",
    "yes > /dev/null", "rm -r /*", ">:*", ":(){ :|: & };:", "wget http://malicious",
    "curl http://malicious", "scp", "telnet", "nc", "netcat", "nmap", "iptables",
    "ufw disable", "service stop", "systemctl stop", "systemctl disable", "unlink"
]

def run_command(command: str):
    try:
        # Safety check
        for keyword in dangerous_keywords:
            if keyword in command:
                return f"❌ Dangerous command detected: '{keyword}' is not allowed."

        commands = command.split("&&")
        cwd = os.getcwd()  # current working directory

        output_collection = []

        for cmd in commands:
            cmd = cmd.strip()
            if cmd.startswith("cd "):
                # Change directory
                path = cmd[3:].strip()
                new_path = os.path.abspath(os.path.join(cwd, path))
                if os.path.exists(new_path):
                    cwd = new_path
                else:
                    return f"❌ Directory not found: {new_path}"
            else:
                # Execute command in the correct cwd
                process = subprocess.Popen(
                    cmd,
                    shell=True,
                    cwd=cwd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output, error = process.communicate()
                if process.returncode == 0:
                    output_collection.append(output.strip())
                else:
                    output_collection.append(f"❌ Error: {error.strip()}")

        return "\n".join(output_collection).strip()

    except Exception as e:
        return f"❌ Exception: {str(e)}"

def get_system_info(*args, **kwargs):
    try:
        # For posix systems like Linux and MacOS, os.uname() is available.
        system_info = os.uname().sysname if hasattr(os, 'uname') else os.name
        if system_info == "posix":
            if os.path.exists("/System/Library"):
                return "MacOS"
            else:
                return "Linux"
        elif system_info == "nt":
            return "Windows"
        else:
            return "Unknown"
    except Exception as e:
        return str(e)

def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return str(e)


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"File written successfully to {path}"


def append_to_file(file_path: str, content: str) -> str:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'a') as f:
            f.write(content)
        return f"Content appended successfully to '{file_path}'."
    except Exception as e:
        return str(e)

def list_directory(path: str) -> str:
    try:
        if not os.path.exists(path):
            return f"Directory '{path}' does not exist."
        entries = os.listdir(path)
        return "\n".join(entries)
    except Exception as e:
        return str(e)

def fix_errors(error_log: str) -> str:
    """
    A simple heuristic-based error fixer.
    It inspects the error log and returns suggested fixes.
    You can expand these patterns to better fit your needs.
    """
    suggestions = []
    
    if "ModuleNotFoundError" in error_log:
        suggestions.append("It seems a module is missing. Try installing the required package using pip or npm.")
    if "SyntaxError" in error_log:
        suggestions.append("There's a syntax error in your code. Check for missing colons, brackets, or typos.")
    if "Cannot find module" in error_log:
        suggestions.append("A module cannot be found. Ensure that all dependencies are installed and paths are correct.")
    if "port is already in use" in error_log:
        suggestions.append("The port is occupied. Try stopping the process using that port or change the port number.")
    if not suggestions:
        suggestions.append("No specific error fix found. Please review the error log manually.")

    return "\n".join(suggestions)

# Updating the available tools dictionary with new methods
available_tools = {
    "run_command": {
        "fn": run_command,
        "description": "Executes one or more shell commands and returns the output."
    },
    "get_system_info": {
        "fn": get_system_info,
        "description": "Returns the operating system type (Windows, MacOS, Linux, or Unknown)."
    },
    "read_file": {
        "fn": read_file,
        "description": "Reads and returns the content of a specified file."
    },
    "write_file": {
        "fn": write_file,
        "description": "Writes or overwrites content into a specified file path.",
        "input": {
            "path": "The path to the file that will be written or overwritten.",
            "content": "The text content to be written into the file."
        }
    },

    "append_to_file": {
        "fn": append_to_file,
        "description": "Appends content to an existing file."
    },
    "list_directory": {
        "fn": list_directory,
        "description": "Lists all files and folders in the specified directory."
    },
    "fix_errors": {
        "fn": fix_errors,
        "description": "Analyzes error logs or stack traces and suggests possible fixes."
    }
}



system_prompt = f"""
    You are a highly skilled AI Coding Agent operating exclusively via the terminal.
    You act like a mini-version of Cursor, assisting users in building and evolving real-world applications directly through the terminal.
    You function using a structured process: start → plan → action → observe.
    You specialize in full-stack development (MERN, FastAPI, JavaScript, Python, etc.) and operate fully via command-line interaction — no GUI.

    You understand existing project context, generate or modify code, fix errors, install dependencies, and run commands.
    

    For the given user query and available tools, plan the step by step execution, based on the planning,
    You operate using available tools (listed below) and can run shell commands, modify files, read project structure, and debug issues — just like a powerful coding terminal agent.
    You are intelligent, cautious, and goal-oriented.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    

    Rules:
    - Always follow the Output JSON Format.
    - Always respond with a single JSON object like: 
        '{{ "step": "plan", "content": "..." }} or '
        '{{ "step": "action", "function": "tool_name", "input": {{ "..." }} }} or '
        '{{ "step": "output", "content": "..." }}. '
        "Never return multiple JSON objects. Do not explain. "
        "Only return one JSON object per message."
    - Operate in one step at a time: start, plan, action, observe, or output.
    - Skip unnecessary steps smartly (e.g., avoid redundant installs).
    - Always cd into the required directory before running commands.
    - Always wait for the observation after `action` before continuing.
    - Auto-confirm prompts: enter y or password Coder_agent@2025 when asked.
    - Detect and handle background processes like npm run dev, vite, etc.
    - Never run dangerous commands (e.g., rm -rf /, disk wipes).
    - Act like a developer-first AI — use clean code, best practices, and proper error handling.
    - Detect, explain, and fix common errors or stack traces automatically.
    - Handle file edits: read, write, append, or refactor code if needed.
    - Perform basic code intelligence: generate components, modify logic, or create files/folders as required.
    - Prioritize developer productivity — fast iterations, automation, and feedback-driven fixes.

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    {json.dumps({k: v['description'] for k, v in available_tools.items()}, indent=4)}


    Example:
    User Query: "Create a Vite + React TypeScript app and run it"
    Output: {{ "step": "start", "content": "User wants a Vite + React TypeScript project setup. Let's plan the required steps." }}
    Output: {{ "step": "plan", "content": "Plan:\n1. Get system info to check Node availability\n2. Install Vite + React with TypeScript\n3. Start dev server\n4. Return URL"}}
    Output: {{ "step": "action", "function": "get_system_info", "input": ""}}
    Output: {{ "step": "observe", "content": "System: Linux. Proceeding to create the project." }}
    Output: {{ "step": "action", "function": "run_command", "input": "npm create vite@latest my-app" }}
    Output: {{ "step": "observe", "content": "Vite project created. Next: install dependencies."}}
    Output: {{ "step": "action", "function": "run_command", "input": "cd my-app && npm install" }}
    Output: {{
    "step": "action",
    "function": "write_file",
    "input": {{
        "path": "my-app/src/App.tsx",
        "content": "export default function App() {{\n  return <h1>Hello, Vite + React + TypeScript!</h1>;\n}}"
    }}
    }}
    Output: {{ "step": "action", "function": "run_command", "input": "npm run dev"}}

"""
# 

messages = [
    { "role": "system", "content": system_prompt }
]

while True:
    user_query = input('> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            messages=messages,
            response_format={"type": "json_object"},
            stream=False,
            model="qwen-2.5-coder-32b",
        )

        # parsed_output = json.loads(response.choices[0].message.content)
        try:
            
            content = response.choices[0].message.content
            # content = response['choices'][0]['message']['content']
            if content is None:
                print("❌ No content received from the assistant.")
                continue
            parsed_output = json.loads(content)
        except Exception as e:
            print(f"❌ Error parsing response: {e}")
            print(f"👉 Full response: {response}")
            continue

        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        if parsed_output.get("step") == "plan" or parsed_output.get("step") == "observe":
            print(f"🧠: {parsed_output.get('content')}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            print(f"🧠: running {tool_name}: {tool_input}")

            if available_tools.get(tool_name, False) != False:
                # output = available_tools[tool_name].get("fn")
                tool_fn = available_tools[tool_name].get("fn")
                # output = tool_fn(**tool_input)
                # 🔧 Fix: handle both dict and str inputs
                if isinstance(tool_input, dict):
                    output = tool_fn(**tool_input)
                else:
                    output = tool_fn(tool_input)
                print(f"🧠: output {tool_name}: {output}")
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "content":  output}) })
                continue

        if parsed_output.get("step") == "get_system":
            tool_name = parsed_output.get("function")
            print(f"🧠: tool_name {tool_name}")

            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")()
                print(f"🧠: output {output}")
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                continue
        
        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break