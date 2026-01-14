"""Quick test to verify OpenAI API key works"""
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

print("Testing OpenAI API key...")
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'Say "Hello! AI is working!" in exactly those words.'}],
        max_tokens=20
    )
    print(f"✓ SUCCESS! ChatGPT says: {response.choices[0].message.content}")
    print("\n✓ Your AI Assistant is ready to use!")
    print("✓ Run: python main.py")
except Exception as e:
    print(f"✗ Error: {e}")
