import { config } from 'dotenv'
import { OpenAI } from 'openai'

config()
const openai = new OpenAI( { apiKey: process.env.API_KEY } );

openai.chat.completions.create({ 
    model: "gpt-4o",
    messages: [
        { role: "user", content: "Hello ChatGPT" }
    ]
}).then(res => {
    console.log(res)
    res.choices.forEach( out => console.log(out.message.content) );
});








/*const form = document.getElementById('chatForm');
const chatBox = document.getElementById('chatBox');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const userInput = document.getElementById('userInput').value;

  // Display user's message
  const userMessage = document.createElement('p');
  userMessage.textContent = `User: ${userInput}`;
  chatBox.appendChild(userMessage);

  // Send message to the back-end
  const response = await fetch('http://localhost:3000/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message: userInput }),
  });

  const data = await response.json();

  // Display AI's response
  const aiMessage = document.createElement('p');
  aiMessage.textContent = `AI: ${data.reply}`;
  chatBox.appendChild(aiMessage);

  // Clear input
  document.getElementById('userInput').value = '';
});*/

