from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

# ── GEMINI SETUP ─────────────────────────────────────────────
GROQ_API = os.environ.get("GROQ_API", "")
# Initialize the Groq client
client = Groq(api_key=GROQ_API)  # Replace with your actual API key


def generate_groq(prompt):
    # Send a chat completion request
    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"{prompt}"  # Replace with your message
            }
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    # Print the response
    # print("Response:", chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

# generate_groq("Hi")