import { GoogleGenerativeAI } from "@google/generative-ai";
import fs from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import readline from 'readline';

// Required when using `import` in Node.js to resolve __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const apiKey = '';
const genAI = new GoogleGenerativeAI(apiKey);


// Promisify exec for async/await support
// const execPromise = promisify(exec);


// Define the log file path
const logFilePath = path.join(process.cwd(), 'agent_log.txt');

// Block dangerous commands
const blockedCommands = [
    /rm\s+-\s*rf\s*\//,  // Matches 'rm -rf /'
    /sudo\s+rm\s+.*\//,   // Matches 'sudo rm ...'
    /.*\bsudo\s+.*\b/,     // Matches any command with 'sudo'
    // Add more patterns for dangerous commands as needed
    /rm/,
    /sudo/,
    /chmod/,
    /chown/,
    /reboot/,
    /shutdown/,
    /format/
];

// List of all commands to be executed
const commands = [
    "mkdir node-express-backend",
    "cd node-express-backend",
    "touch server.js",
    "touch .env",
    "touch package.json",
    "mkdir routes controllers models middlewares views public config",
    "touch routes/index.js",
    "touch controllers/userController.js",
    "touch models/userModel.js",
    "touch middlewares/authMiddleware.js",
    "touch views/index.ejs",
    "touch public/style.css",
    "touch config/dbConfig.js",
    "touch README.md",
    "touch .gitignore"
];


// Your promise wrapper
function execPromise(command, options = {}) {
    return new Promise((resolve, reject) => {
        exec(command, options, (error, stdout, stderr) => {
            if (error) {
                reject({ error, stderr });
            } else {
                resolve({ stdout, stderr });
            }
        });
    });
}

async function executeCommand(command, cwd = process.cwd()) {
    try {

        if (blockedCommands.some((pattern) => pattern.test(command))) {
            const msg = `Blocked dangerous command: ${command}`;
            logToFile(msg);
            return msg;
        }

        const { stdout, stderr } = await execPromise(command, { cwd });

        const successMsg = `Command executed: ${command}\n In: ${cwd}\n Output: ${stdout || 'No output'}`;
        logToFile(successMsg);

        if (stderr) {
            const errMsg = ` Stderr: ${stderr}`;
            logToFile(errMsg);
            return errMsg;
        }

        return successMsg;
    } catch (err) {
        const errMsg = `Error: ${err.error?.message || err.message}`;
        logToFile(errMsg);
        return errMsg;
    }
}

function logToFile(message) {
    const logPath = path.join(process.cwd(), "agent_logs.txt");
    fs.appendFileSync(logFilePath, `[${new Date().toISOString()}] ${message}\n`);
}


async function create_node_express_backend() {
    const appName = "node-express-backend";
    const appPath = path.join(process.cwd(), appName);

    // Step 1: Create the base folder
    if (!fs.existsSync(appPath)) {
        fs.mkdirSync(appPath);
        logToFile(`📁 Created project folder: ${appPath}`);
        console.log(`📁 Created: ${appPath}`);
    } else {
        logToFile(`Folder already exists: ${appPath}`);
        console.log(`Folder already exists: ${appPath}`);
    }

    // Step 2: Create folder structure inside the backend app
    const folders = [
        "routes",
        "controllers",
        "models",
        "middlewares",
        "views",
        "public",
        "config"
    ];

    for (const folder of folders) {
        const fullPath = path.join(appPath, folder);
        fs.mkdirSync(fullPath, { recursive: true });
        logToFile(`📁 Created folder: ${fullPath}`);
        console.log(`📁 Created folder: ${folder}`);
    }

    // Step 3: Create files (empty)
    const files = [
        "server.js",
        ".env",
        "package.json",
        "routes/index.js",
        "controllers/userController.js",
        "models/userModel.js",
        "middlewares/authMiddleware.js",
        "views/index.ejs",
        "public/style.css",
        "config/dbConfig.js",
        "README.md",
        ".gitignore"
    ];

    for (const file of files) {
        const fullPath = path.join(appPath, file);
        fs.writeFileSync(fullPath, "");
        logToFile(`📄 Created file: ${fullPath}`);
        console.log(`📄 Created file: ${file}`);
    }

    console.log(`Node.js Express backend structure created in "${appName}"`);
}

async function create_react_app() {
    const appName = "my-react-app";
    const appPath = path.join(process.cwd(), appName);

    // Step 1: Create the React app using Vite
    const viteCommand = `npm create vite@latest ${appName} -- --template react`;
    const createResult = await executeCommand(viteCommand);
    console.log(createResult);

    // Step 2: Install dependencies
    //const installResult = await executeCommand("npm install", appPath);
    //console.log(installResult);

    // Step 3: Create folder structure using Node.js (cross-platform safe)
    const foldersToCreate = [
        "src/components",
        "src/pages",
        "src/assets",
        "src/hooks",
        "src/utils"
    ];

    for (const folder of foldersToCreate) {
        const fullPath = path.join(appPath, folder);
        fs.mkdirSync(fullPath, { recursive: true });
        logToFile(`📁 Created folder: ${fullPath}`);
        console.log(`📁 Created folder: ${folder}`);
    }

    // Step 4: Create files
    const filesToCreate = [
        "src/components/Header.jsx",
        "src/pages/Home.jsx",
        "src/hooks/useExample.js",
        "src/utils/helpers.js",
        "src/styles.css",
        ".env",
        "README.md"
    ];

    for (const file of filesToCreate) {
        const fullPath = path.join(appPath, file);
        fs.writeFileSync(fullPath, ""); // Create empty file
        logToFile(`📄 Created file: ${fullPath}`);
        console.log(`📄 Created file: ${file}`);
    }

    console.log(`React app "${appName}" created successfully!`);

}

async function create_next_app() {
    const appName = "next-app";
    const appPath = path.join(process.cwd(), appName);

    // Step 1: Create Next.js app using NPX
    const result = await executeCommand(`npx create-next-app@latest ${appName} --ts --app --eslint --tailwind --src-dir --no-experimental-app`);
    console.log(result);

    // Step 2: Add folders/files inside /src
    const folders = [
        "src/components",
        "src/pages",
        "src/hooks",
        "src/utils",
        "public"
    ];

    const files = [
        "src/components/Navbar.tsx",
        "src/hooks/useExample.ts",
        "src/utils/helpers.ts",
        ".env.local",
        "README.md"
    ];

    for (const folder of folders) {
        const fullPath = path.join(appPath, folder);
        fs.mkdirSync(fullPath, { recursive: true });
        logToFile(`📁 Created folder: ${fullPath}`);
        console.log(`📁 Created: ${folder}`);
    }

    for (const file of files) {
        const fullPath = path.join(appPath, file);
        fs.writeFileSync(fullPath, "");
        logToFile(`📄 Created file: ${fullPath}`);
        console.log(`📄 Created: ${file}`);
    }

    console.log(`Next.js app "${appName}" is ready.`);
}

async function create_angular_app() {
    const appName = "angular-app";
    const appPath = path.join(process.cwd(), appName);

    // Step 1: Create Angular app using CLI
    const result = await executeCommand(`npx @angular/cli@latest new ${appName} --routing --style=scss --skip-tests`);
    console.log(result);

    // Step 2: Add common folders and files
    const folders = [
        "src/app/components",
        "src/app/pages",
        "src/app/services",
        "src/assets"
    ];

    const files = [
        "src/app/components/header.component.ts",
        "src/app/pages/home.component.ts",
        "src/app/services/api.service.ts",
        ".env",
        "README.md"
    ];

    for (const folder of folders) {
        const fullPath = path.join(appPath, folder);
        fs.mkdirSync(fullPath, { recursive: true });
        logToFile(`📁 Created folder: ${fullPath}`);
        console.log(`📁 Created: ${folder}`);
    }

    for (const file of files) {
        const fullPath = path.join(appPath, file);
        fs.writeFileSync(fullPath, "");
        logToFile(`📄 Created file: ${fullPath}`);
        console.log(`📄 Created: ${file}`);
    }

    console.log(`Angular app "${appName}" is ready.`);
}

async function create_vite_app() {
    const appName = "vite-app";
    const appPath = path.join(process.cwd(), appName);

    // Step 1: Create Vite app
    const viteResult = await executeCommand(`npm create vite@latest ${appName} -- --template vanilla`);
    console.log(viteResult);

    // Step 2: Install dependencies
    // await executeCommand("npm install", appPath);

    // Step 3: Add structure
    const folders = [
        "src/components",
        "src/utils",
        "src/assets"
    ];

    const files = [
        "src/components/Main.js",
        "src/utils/helpers.js",
        ".env",
        "README.md"
    ];

    for (const folder of folders) {
        const fullPath = path.join(appPath, folder);
        fs.mkdirSync(fullPath, { recursive: true });
        logToFile(`📁 Created folder: ${fullPath}`);
        console.log(`📁 Created: ${folder}`);
    }

    for (const file of files) {
        const fullPath = path.join(appPath, file);
        fs.writeFileSync(fullPath, "");
        logToFile(`📄 Created file: ${fullPath}`);
        console.log(`📄 Created: ${file}`);
    }

    console.log(`Vite Vanilla app "${appName}" is ready.`);
}

async function create_html_css_js_project() {
    const appName = "html-css-js-app";
    const appPath = path.join(process.cwd(), appName);

    // Create base project folder
    if (!fs.existsSync(appPath)) {
        fs.mkdirSync(appPath, { recursive: true });
        logToFile(`📁 Created base folder: ${appPath}`);
    }

    // Folders to create
    const folders = [
        "css",
        "js",
        "assets"
    ];

    // Files to create with basic content
    const files = {
        "index.html": `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Web Page</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Hello, World!</h1>
    <script src="js/script.js"></script>
</body>
        </html>`,

                "css/style.css": `body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
        }`,

                "js/script.js": `document.addEventListener('DOMContentLoaded', () => {
            console.log("🚀 Page loaded!");
        });`,

                "README.md": `# HTML, CSS, JS Project

        This is a basic static website project structure.`
    };

    // Create folders
    for (const folder of folders) {
        const folderPath = path.join(appPath, folder);
        fs.mkdirSync(folderPath, { recursive: true });
        logToFile(`📁 Created folder: ${folderPath}`);
        console.log(`📁 Created: ${folder}`);
    }

    // Create files with content
    for (const [filePath, content] of Object.entries(files)) {
        const fullPath = path.join(appPath, filePath);
        fs.writeFileSync(fullPath, content);
        logToFile(`📄 Created file: ${fullPath}`);
        console.log(`📄 Created: ${filePath}`);
    }

    console.log(`🎉 Basic HTML/CSS/JS project "${appName}" is ready.`);
}

async function readFileContent(filePath) {
    const absolutePath = path.join(process.cwd(), filePath);
    if (!fs.existsSync(absolutePath)) {
        const errorMsg = `File not found: ${filePath}`;
        logToFile(errorMsg);
        return errorMsg;
    }

    const content = fs.readFileSync(absolutePath, 'utf-8');
    logToFile(`Read file: ${filePath}`);
    return content;
}

export async function updateFileContent(input) {
    if (!input || !input.filePath || !input.newContent) {
        console.error("Invalid input: Expected { filePath, newContent }");
        return "Invalid input, could not update the file.";
    }

    const { filePath, newContent } = input;

    try {
        const fullPath = path.resolve(__dirname, filePath); // Absolute path
        const dirPath = path.dirname(fullPath);             // Folder path

        //  Ensure directory exists
        await fs.promises.mkdir(dirPath, { recursive: true });

        //  Write to file
        await fs.promises.writeFile(fullPath, newContent, 'utf-8');

        console.log(` File updated: ${fullPath}`);
        return ` The file \`${filePath}\` has been created/updated successfully.`;
    } catch (error) {
        console.error(` Error updating file: ${error.message}`);
        return ` Error: Could not update the file at ${filePath}`;
    }
}







//////////////////////////////////////////////////////////////////////////

// Execute all commands sequentially
async function executeAllCommands() {
    for (const command of commands) {
        const result = await executeCommand(command);
        console.log(result); // Log the result of each command
    }
}


//  Function: Get weather info
async function get_weather(city = '') {
    const response = await fetch(`https://wttr.in/${city.toLowerCase()}?format=%c+%t`);
    const result = await response.text();
    return result.trim();
}

//  Function: Create folder
async function createFolder(folderName) {
    const folderPath = path.join(process.cwd(), folderName);
    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath);
        return ` Folder '${folderName}' created successfully.`;
    } else {
        return ` Folder '${folderName}' already exists.`;
    }
}

async function createFileInFolder(folderName, fileName, content = '') {
    const folderPath = path.join(process.cwd(), folderName);
    const filePath = path.join(folderPath, fileName);

    // Create folder if it doesn't exist
    if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath);
        console.log(`📁 Created folder: ${folderPath}`);
    }

    // Create file (or overwrite if exists)
    fs.writeFileSync(filePath, content);
    console.log(`📄 Created file: ${filePath}`);
}


//  Tool map for dynamic function calls
const tools = {
    get_weather,
    createFolder,
    createFileInFolder,
    executeCommand,
    executeAllCommands,
    create_node_express_backend,
    create_react_app,
    create_next_app,
    create_angular_app,
    create_vite_app,
    readFileContent,
    updateFileContent,
    create_html_css_js_project
};

//  AI Agent Model
const model = genAI.getGenerativeModel({
    model: "gemini-2.0-flash",
    systemInstruction: `
        # 🧠 AI Agent Prompt (Structured Reasoning: Start → Plan → Action → Observe)
        You are an intelligent AI agent designed to solve user queries using a structured 
        reasoning approach, based on the **Start → Plan → Action → Observe** cycle.

        Your behavior follows these rules:
        - Follow the output JSON format
        - Always perform one step at a time and wait for the next input
        - Carefully analyse the user query
        - If the user asking to do any changes in react, node, express, angular, vite project use tools readFileContent and updateFileContent to read and update files/content

            **Important:** When the user asks to update or create a file in a project (e.g., 'my-react-app, 'node-express-backend), make sure the 'filePath includes the correct project folder prefix.


        ## 🔁 Reasoning Flow
        1. **Start** – Understand the user’s query and initiate your reasoning.  
        2. **Plan** – Think through what needs to be done to answer the query.  
        3. **Action** – Call an external tool if needed (e.g., 'get_weather).  
        4. **Observe** – Wait for the tool's response before continuing.  
        5. **Output** – Once you have all necessary information, provide the final answer to the user.

        ## 📦 Output Format
        "step": one of start, plan, action, observe, or output
        "content": your explanation or answer at that step
        "function": (only for step=action) the function name to call
        "input": (only for step=action) the input string for the function
        "output": (only for step=observe) the output string from the function

        Do not use markdown or code formatting. Return plain JSON only.

        Availabe tools:
        - get_weather: takes a city name as a string input and returns the current weather of that city.
        - createFolder: takes a foldername as a string input and create the folder in the current working directory
        - createFileInFolder: takes a JSON string with keys "folderName", "fileName", and "content". It creates a file with the given content inside the specified folder.
            Example input:
            {
            "folderName": "logs",
            "fileName": "log1.txt",
            "content": "This is a test log"
            }
        - executeCommand: takes a shell command as a string and executes it in the current working directory.
        - executeAllCommands: Takes an array of shell commands and executes them sequentially, logging the result of each command.
        - create_node_express_backend: execute the function 'create_node_express_backend'
        - create_react_app: execute the function 'create_react_app'
        - create_next_app: execute the function 'create_next_app'
        - create_angular_app: execute the function 'create_angular_app'
        - create_vite_app: execute the function 'create_vite_app'
        - create_html_css_js_project: execute the function 'create_html_css_js_project'
        - readFileContent: takes a relative file path as a string input and returns the content of the file as a string.
        - updateFileContent: takes an object with two properties:
            - filePath (string): the relative path of the file to update
            - newContent (string): the new content to write into the file

            **Note:** If readFileContent returns an empty string or minimal content (less than 10 characters), assume the file is empty or new and generate the entire file content from scratch (e.g., a full functional React component).
            **Important:** When the user asks to update or create a file in a project (e.g., 'my-react-app, 'node-express-backend), make sure the 'filePath includes the correct project folder prefix.

        
        
        Example:
        User Query - What is the weather of new york
        {{ "step": "start", "content": "User is asking for the weather in New York.", "function": "", "input": "" }}
        {{ "step": "plan", "content": "I need to retrieve weather data using an external tool.", "function": "", "input": "" }}
        {{ "step": "action", "content": "Calling get_weather function with 'New York'", "function": "get_weather", "input": "New York" }}
        {{ "step": "observe", "content": "Tool returned: 12°C", "function": "", "output": "" }}
        {{ "step": "output", "content": "The current weather in New York is 12°C." }}

        ## Example User Queries:

        1. **Query**: "Create a folder called 'myfolder'."
        **Action**: Call 'createFolder with "myfolder".
        **Response**: "The folder 'myfolder' has been created."

        2. **Query**: "Run these commands: ['mkdir folder1', 'touch file1.txt']"
        **Action**: Call 'executeAllCommands with the array of commands.
        **Response**: "The commands were executed successfully. Folder 'folder1' and file 'file1.txt' were created."

        3. **Query**: "Create a node js project"
        **Action**: Call 'create_node_express_backend' function.
        **Response**: "Node Express backend has been created."

        4. **Query**: "Create a react js project"
        **Action**: Call 'create_vite_app' function.
        **Response**: "React App has been created."

        5. **Query**: "Update the src/pages/Home.jsx in my-react-app to include a new heading that says ‘Welcome to the AI App’."
        "start": "Understands intent"
        "plan": "Needs to read + modify a file"
        "action" → "call readFileContent with path"
        "observe": "Gets file content, If readFileContent returns an empty string or minimal content, assume the file is new and generate the full component from scratch."
        "action" → "call updateFileContent with new content"
        "output": "Confirms the file is updated"

        6. **Query**: "create a new file Navar in src/components in react project"
        "start": "Understands intent"
        "plan": "Needs to read + modify a file"
        "action" → "call readFileContent with path"
        "observe": "Gets file content, If readFileContent returns an empty string or minimal content, assume the file is new and generate the full component from scratch."
        "action" → "call updateFileContent with new content"
        "output": "Confirms the file is updated"


    `,
});

//  Model generation config
const generationConfig = {
    temperature: 1,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 8192,
    responseModalities: [],
    responseMimeType: "text/plain",
};

const message = "update the main.js file in node-express-backend project and add a new express server to fetch user-profiles";

const messages = [
    {
        role: 'user',
        parts: [{ text: message }],
    },
];



const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

rl.question('Enter your input: ', async (message) => {

    const chatSession = model.startChat({
        generationConfig,
        history: messages
    });

    while (true) {
        const result = await chatSession.sendMessage(message);
        const raw = await result.response.text();
        const cleaned = raw.replace(/```json|```/g, '').trim();

        let jsonObject;
        try {
            jsonObject = JSON.parse(cleaned);
        } catch (e) {
            console.error(" Failed to parse JSON:", cleaned);
            break;
        }

        
        console.log(`o ${jsonObject.content}`);

        // Add current step to message history
        messages.push({
            role: 'model',
            parts: [{ text: cleaned }],
        });

        // Exit if final output
        if (jsonObject.step === 'output') {
            break;
        }

        if (jsonObject.step === 'action') {
            const fnName = jsonObject.function;
            let input = jsonObject.input;

            if (!tools[fnName]) {
                console.error(` Function '${fnName}' is not defined.`);
                break;
            }

            try {
                input = JSON.parse(input);
                console.log("----input----: ", input);
            } catch (_) {
                // Leave input as-is for simple string tools
            }

            let output;


            if (typeof input === 'object' && !Array.isArray(input)) {
                // Handle special cases based on function
                if (fnName === 'updateFileContent') {
                    const { filePath, newContent } = input;
                    output = await tools[fnName]({ filePath, newContent });
                } else if (fnName === 'createFileInFolder') {
                    const { folderName, fileName, content } = input;
                    output = await tools[fnName](folderName, fileName, content);
                } else {
                    output = await tools[fnName](input); // Pass as-is
                }
            } else if (Array.isArray(input)) {
                output = await tools[fnName](...input);
            } else {
                output = await tools[fnName](input);
            }

            const observeJson = JSON.stringify({
                step: "observe",
                content: `Tool returned: ${output}`,
                function: "",
                output: output
            });

            const observeObj = JSON.parse(observeJson);
            console.log(`o ${observeObj.content}`);

            messages.push({
                role: 'model',
                parts: [{ text: observeJson }],
            });

            continue;
        }

    }

    rl.close(); 
});