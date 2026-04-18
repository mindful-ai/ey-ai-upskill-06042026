from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
import sqlite3

# ============================================================
# DB SETUP
# ============================================================

def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT,
        authenticated INTEGER
    )
    """)

    conn.commit()
    conn.close()


def seed_data():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    users = [
        ("ML001", "Raj", 1),
        ("ML002", "Ram", 0),
        ("ML003", "Sham", 1)
    ]

    cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", users)

    conn.commit()
    conn.close()


# ============================================================
# TOOLS (STRUCTURED)
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add a user to the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (id, name, authenticated) VALUES (?, ?, ?)",
            (user_id, name, 1)
        )
        conn.commit()
        return f"User {name} added with ID {user_id}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()


@tool
def list_users() -> str:
    """List all users"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, authenticated FROM users")
    rows = cursor.fetchall()
    conn.close()

    return "\n".join([str(r) for r in rows]) or "No users found"


# ============================================================
# MAIN
# ============================================================

f = open(r"E:\Lenovo Ideapad 330\company-material\ai-upskill\key-vault\groq\groq-api-key.txt")
groq_api_key = f.read()
f.close()

if __name__ == "__main__":

    setup_db()
    seed_data()

    # Groq via OpenAI-compatible API
    llm = ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=groq_api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

    tools = [add_user, list_users]

    # ---------------- Demo: change prompt to show how system prompt can be used to steer agent behavior ----------------

    # THIS is the correct API  
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="You are a user management assistant. Always use tools."  # [Demo]
        system_prompt=prompt
    )

    # Invoke
    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "Add a user named Purushotham with id ML501"}
        ]
    })

    print(response["messages"][-1].content)

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": "Give me a list of all authenticated users"}
        ]
    })

    print(response["messages"][-1].content)