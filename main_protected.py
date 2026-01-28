import os
import sys
from groq import Groq
from dotenv import load_dotenv

def load_system_prompt(filename="system_prompt.txt"):
    """Reads the system prompt from a local text file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️ Error: '{filename}' not found. Please create it in this folder.")
        sys.exit(1)

def chat():
    # 1. Load variables from .env file
    load_dotenv()
    
    # 2. Initialize Groq Client
    # It will look for GROQ_API_KEY inside your .env file
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in .env file.")
        print("Please create a .env file with: GROQ_API_KEY=your_key_here")
        return

    client = Groq(api_key=api_key)
    
    # 3. Load System Prompt & Initialize History
    system_content = load_system_prompt()
    messages = [
        {"role": "system", "content": system_content}
    ]

    print("--- Groq Terminal Chat (Environment: Loaded) ---")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            # Using Llama 3.3 70B for high-quality responses
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                stream=True,
            )

            print("Groq: ", end="", flush=True)
            full_response = ""
            
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n") 

            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            print(f"\n❌ API Error: {e}")

if __name__ == "__main__":
    chat()