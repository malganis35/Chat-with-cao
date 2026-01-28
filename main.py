import os
import sys
from groq import Groq

# Replace with your actual API key for testing
API_KEY_PASSWORD = "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" 

def load_system_prompt(filename="system_prompt.txt"):
    """Reads the system prompt from a local text file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️ Error: '{filename}' not found. Please create it in this folder.")
        sys.exit(1)

def chat():
    # 1. Initialize Groq Client
    # Ensure you have export GROQ_API_KEY='your_key_here' in your terminal
    api_key = API_KEY_PASSWORD # os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("❌ Error: GROQ_API_KEY environment variable is not set.")
        return

    client = Groq(api_key=api_key)
    
    # 2. Load System Prompt & Initialize History
    system_content = load_system_prompt()
    messages = [
        {"role": "system", "content": system_content}
    ]

    print("--- Groq Terminal Chat ---")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        # 3. Get User Input
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

        # 4. Add User Message to History
        messages.append({"role": "user", "content": user_input})

        # 5. Query Groq
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
                stream=True, # Streaming for a better terminal feel
            )

            print("Groq: ", end="", flush=True)
            full_response = ""
            
            for chunk in completion:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_response += content
            
            print("\n") # New line after finished response

            # 6. Add Assistant Response to History
            messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            print(f"\n❌ API Error: {e}")

if __name__ == "__main__":
    chat()