import json

def create_todo_files():
    # The HTML, CSS, and JS content as plain strings
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="todo-container">
        <h1>Todo List</h1>
        <input type="text" id="todo-input" placeholder="Add a new todo">
        <button id="add-todo">Add</button>
        <ul id="todo-list"></ul>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
    
    css_content = """body {
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.todo-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    width: 300px;
}

h1 {
    text-align: center;
}

input[type="text"] {
    width: calc(100% - 22px);
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #28a745;
    border: none;
    border-radius: 4px;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background-color: #218838;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    background-color: #f9f9f9;
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 4px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

li button {
    background-color: #dc3545;
    border: none;
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

li button:hover {
    background-color: #c82333;
}"""

    js_content = """document.addEventListener('DOMContentLoaded', () => {
    const addTodoButton = document.getElementById('add-todo');
    const todoInput = document.getElementById('todo-input');
    const todoList = document.getElementById('todo-list');
    
    addTodoButton.addEventListener('click', () => {
        const todoText = todoInput.value.trim();
        if (todoText !== '') {
            addTodoItem(todoText);
            todoInput.value = '';
        }
    });
    
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodoButton.click();
        }
    });
    
    function addTodoItem(text) {
        const li = document.createElement('li');
        li.textContent = text;
    
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', () => {
            li.remove();
        });
    
        li.appendChild(deleteButton);
        todoList.appendChild(li);
    }
});"""

    # Create JSON data
    data = {
        "step": "action",
        "function": "write_file",
        "input": [
            {"file_path": "index.html", "content": html_content},
            {"file_path": "style.css", "content": css_content},
            {"file_path": "script.js", "content": js_content}
        ]
    }

    # Convert to JSON
    json_data = json.dumps(data)
    print(json_data)

# Call the function
create_todo_files()
