import express from 'express';
import cors from 'cors';
import { config } from 'dotenv';
import { OpenAI } from 'openai';

config();
const app = express();
const port = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// OpenAI API setup
const openai = new OpenAI({ apiKey: process.env.API_KEY });

// Route to handle chat requests
app.post('/chat', async (req, res) => {
  const userMessage = req.body.message;

  try {
    const aiResponse = await openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: userMessage }],
    });

    const botReply = aiResponse.choices[0].message.content;
    res.json({ reply: botReply });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error processing request' });
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
