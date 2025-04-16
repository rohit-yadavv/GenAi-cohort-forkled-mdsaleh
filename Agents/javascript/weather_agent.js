import Groq from "groq-sdk";
import dotenv from "dotenv";
import readlineSync from "readline-sync";

dotenv.config();

const client = new Groq({
  apiKey: process.env.GROQ_API_KEY,
});

// tools
function getWeatherDetails(city = "") {
  if (city.toLowerCase() === "sirsi") return "10°C";
  if (city.toLowerCase() === "banaglore") return "30°C";
  if (city.toLowerCase() === "hubbli") return "40°C";
}

const tools = {
  "getWeatherDetails": getWeatherDetails,
};

const SYSTEM_PROMPT = `
    You are an AI Assistant with START, PLAN, ACTION, Obeservation and Output State.
    Wait for the user prompt and first PLAN using available tools.
    After Planning, Take the action with appropriate tools and wait for Observation based on Action.
    Once you get the observations, Return the AI response based on START propmt and observations

    Strictly follow the JSON ouput format as in examples

    Available Tools:
    - function getWeatherDetails(city: string): string
    getWeatherDetails is a function that accepts city name as string and retuns the weather details

    Example:
    START
    { "type": "user", "user": "What is the sum of weather of Patiala and Mohali?" }
    { "type": "plan", "plan": "I will call the getWeatherDetails for Patiala" }
    { "type": "action", "function": "getWeatherDetails", "input": "patiala" }
    { "type": "observation", "observation": "10°C" }
    { "type": "plan", "plan": "I will call getWeatherDetails for Mohali" }
    { "type": "action", "function": "getWeatherDetails", "input": "mohali" }
    { "type": "observation", "observation": "14°C" }
    { "type": "output", "output": "The sum of weather of Patiala and Mohali is 24°C" }
`;

// observation is function output

// const user = "hey what is the weather of sirsi"

// client.chat.completions
//   .create({
//     model: "llama-3.1-8b-instant",
//     messages: [
//       { role: "system", content: SYSTEM_PROMPT },
//       { role: "user", content: user },
//     ],
//   })
//   .then((e) => {
//     console.log(e.choices[0].message.content);
//   })
//   .catch((err) => {
//     console.log(err);
//   });

const messages = [{ role: "system", content: SYSTEM_PROMPT }];
async function hello() {
    while (true) {
      const query = readlineSync.question(">> ");
      const q = { role: "user", user: query };
      messages.push({ role: "user", content: JSON.stringify(q) });

      while (true) {
        const chat = await client.chat.completions.create({
          model: "llama-3.1-8b-instant",
          messages: messages,
          response_format: { type: "json_object" },
        });
        const result = chat.choices[0].message.content;
        messages.push({ role: "assistant", content: result });
        
        console.log("\n\n-------- START AI --------");
        console.log(result);
        console.log("-------- END AI --------\n\n");
        
        

        const call = JSON.parse(result);
        if (call.type === "ouput") {
          console.log(`🤖: ${call.output}`);
          break;
        } else if (call.type === "action") {
          const fn = tools[call.function];
          const observation = fn[call.input];
          const obs = { type: "observation", observation: observation };
          messages.push({ role: "assistant", content: JSON.stringify(obs) });
        }
      }
    }
}
hello()