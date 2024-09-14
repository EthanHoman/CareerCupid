import { config } from 'dotenv'
config()
import { OpenAI } from 'openai'

const API_KEY = API_KEY=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
const openai = new OpenAI( { apiKey: API_KEY } );

openai.chat.completions.create({ 
    model: "gpt-4o",
    messages: [
        { role: "user", content: "Hello ChatGPT" }
    ]
}).then(res => {
    console.log(res)
    res.choices.forEach( out => console.log(out.message) );
});
