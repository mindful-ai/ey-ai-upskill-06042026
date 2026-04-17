# main.py

from groq import Groq
from agent_tools import handle_tool_call

# ----------------------------
# LOAD API KEY
# ----------------------------
with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt", "r") as f:
    api_key = f.read().strip()

# ----------------------------
# INIT CLIENT
# ----------------------------
client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"


# ----------------------------
# CHAT FUNCTION
# ----------------------------
def chat():
    print("Welcome to the ChatBot! Type 'exit' or 'quit' to end the chat.\n")
    print("ChatBot: Hello! How can I assist you today?")

    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    while True:

        # ----------------------------
        # USER INPUT
        # ----------------------------
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

        # ----------------------------
        # REACT LOOP
        # ----------------------------
        react_messages = messages.copy()

        react_messages.append({
            "role": "system",
            "content": """
You are a ReAct-style AI assistant.

STRICT FORMAT:

Thought:
Action:
Action Input:
Observation:
Final Answer:

Rules:
- Use ONLY tools: [get_time, get_date, get_day, get_weather]
- For weather → provide city name
- ALWAYS stop after Final Answer
- DO NOT repeat actions after observation
"""
        })

        final_answer = None
        reasoning_steps = []

        for step in range(4):

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=react_messages,
                    temperature=0
                )

                reply = response.choices[0].message.content.strip()

                react_messages.append({"role": "assistant", "content": reply})
                reasoning_steps.append(reply)

                # ----------------------------
                # FINAL ANSWER FIRST
                # ----------------------------
                if "Final Answer:" in reply:
                    final_answer = reply.split("Final Answer:")[-1].strip()
                    break

                # ----------------------------
                # TOOL EXECUTION
                # ----------------------------
                observation = handle_tool_call(reply)

                if observation:
                    react_messages.append({
                        "role": "user",
                        "content": observation
                    })
                else:
                    break

            except Exception as e:
                print(f"Error during LLM call: {e}")
                break

        # ----------------------------
        # PRINT CLEAN OUTPUT
        # ----------------------------
        print("\n--- ReAct Reasoning ---")

        for i, step in enumerate(reasoning_steps, 1):
            print(f"\nStep {i}:\n{step}")

        if final_answer:
            print(f"\nChatBot: {final_answer}")
            messages.append({"role": "assistant", "content": final_answer})
        else:
            print("\nChatBot: Sorry, I couldn't complete the reasoning.")


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    chat()