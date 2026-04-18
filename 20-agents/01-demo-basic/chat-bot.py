# Use Groq
from groq import Groq
from agent_tools import agent_router

# Read the key from the file
f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt", "r")
api_key = f.read().strip()
f.close()

# Intialize the Groq client
client = Groq(api_key=api_key)

# Select a model
MODEL = "llama-3.1-8b-instant"

# Create a function to generate responses from the model
def chat():
    print("Welcome to the ChatBot! Type 'exit' to end the chat.\n")
    print("ChatBot: Hello! How can I assist you today?")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:

        # Get user input
        user_input = input("You: ")

        # Exit condition
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        # Response from the model
        messages.append({"role": "user", "content": user_input})

        '''
        # ---- AGENT ROUTER LOGIC: Bypassing the model
        agent_response = agent_router(user_input)
        if agent_response:
            print(f"ChatBot (Agent): {agent_response}")
            continue  # Skip calling the model if we have an agent response
        # ----------------------------
        '''

        # ---- AGENT ROUTER LOGIC 
        agent_response = agent_router(user_input)

        if agent_response:
            print(f"[Agent Output]: {agent_response}")
            messages.append({"role": "system", "content": agent_response})
            
        # -------------------------

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.3,
                max_tokens=512
            )

            ai_reply = response.choices[0].message.content
            messages.append({"role": "assistant", "content": ai_reply})

            # Print the response
            print(f"ChatBot: {ai_reply}")

        except Exception as e:
            print(f"An error occurred: {e}")

# Launch the model
if __name__ == "__main__":
    chat()