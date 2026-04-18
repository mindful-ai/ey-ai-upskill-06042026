# Use Groq
from groq import Groq
from agent_tools import handle_tool_call
import re

# Read the key from the file
with open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt", "r") as f:
    api_key = f.read().strip()

# Initialize the Groq client
client = Groq(api_key=api_key)

# Select a model
MODEL = "llama-3.1-8b-instant"


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
        # REACT LOOP (Single LLM)
        # ----------------------------
        react_messages = messages.copy()

        react_messages.append({
            "role": "system",
            "content": """
You are a ReAct-style AI assistant.

Follow STRICTLY:

Thought: reasoning
Action: one of [get_time, get_date, get_day, get_weather]
Action Input: input or NONE
Observation: tool result
Final Answer: final answer to user

Rules:
- Use tools when needed
- For weather, pass city name as input
- If no tool needed → directly give Final Answer
"""
        })

        final_answer = None

        for _ in range(2):  # max reasoning steps

            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=react_messages,
                    temperature=0
                )

                reply = response.choices[0].message.content

                print("\n[LLM Reasoning]\n", reply)

                react_messages.append({"role": "assistant", "content": reply})

                # ----------------------------
                # TOOL EXECUTION
                # ----------------------------
                observation = handle_tool_call(reply)

                if observation:
                    react_messages.append({"role": "user", "content": observation})
                    continue

                # ----------------------------
                # FINAL ANSWER
                # ----------------------------

                '''
                if "Final Answer" in reply:
                    final_answer = reply.split("Final Answer:")[-1].strip()
                    break
                '''

                #print("[test]", reply.split())

                # This should happen outside the loop

                # match = re.search(r"\sFinal Answer\s*:\s*(.*)", reply, re.IGNORECASE)

                # if match:
                #     final_answer = match.group(1).strip()
                #     print("\n[Final Answer Found]", final_answer)
                #     break

            except Exception as e:
                print(f"Error during LLM call: {e}")
                break
        else:
            match = re.search(r"Final Answer\s*:\s*(.*)", reply, re.IGNORECASE)

            if match:
                final_answer = match.group(1).strip()
                print("\n[Final Answer Found]", final_answer)
                
        # ----------------------------
        # OUTPUT HANDLING
        # ----------------------------
        if final_answer:
            print(f"\nChatBot: {final_answer}")
            messages.append({"role": "assistant", "content": final_answer})
        else:
            print("\nChatBot: Sorry, I couldn't complete the reasoning.")

        #print("Messages so far:", react_messages)

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    chat()


'''
✅ Stop loop as soon as Final Answer is found
✅ Print clean, structured reasoning (once)
✅ Avoid repeated tool calls
'''