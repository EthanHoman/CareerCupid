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
    res.choices.forEach( out => console.log(out.message.content) );
});
