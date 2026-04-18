from langchain_openai import ChatOpenAI
from langchain.tools import tool
import sqlite3
import json

# ============================================================
# DATABASE SETUP
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
# TOOLS (All tools should have docstrings explaining their purpose and inputs/outputs)
# Langchain expects tool functions to be decorated with @tool and to have clear type annotations.
# ============================================================

@tool
def add_user(name: str, user_id: str) -> str:
    """Add a new user to the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (user_id, name, 1)
        )
        conn.commit()
        return f"SUCCESS: Added {name}"
    except Exception as e:
        return f"ERROR: {str(e)}"
    finally:
        conn.close()


@tool
def list_users() -> str:
    """Return all users in the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)


@tool
def get_user_by_id(user_id: str) -> str:
    """Retrieve a user by their ID"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return json.dumps(row)


@tool
def update_user_auth(user_id: str, authenticated: int) -> str:
    """Update authentication status of a user (0 or 1)"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET authenticated=? WHERE id=?",
        (authenticated, user_id)
    )
    conn.commit()
    conn.close()
    return "SUCCESS: Updated authentication"


@tool
def delete_user(user_id: str) -> str:
    """Delete a user from the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
    return "SUCCESS: User deleted"


@tool
def count_users() -> str:
    """Return total number of users in the database"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return str(count)


@tool
def search_user_by_name(name: str) -> str:
    """Search users by name (partial match supported)"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    conn.close()
    return json.dumps(rows)

# ============================================================
# LLM
# ============================================================

def get_llm(api_key):
    return ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_key=api_key,
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0
    )

# ============================================================
# PLANNER
# ============================================================

def planner(llm, user_input):
    # -------- Logic for planner to generate a plan (action + action inputs) based on user input and available tools
    response = llm.invoke(prompt)
    return json.loads(response.content)

# ============================================================
# EXECUTOR
# ============================================================

TOOLS = {
    "add_user": add_user,
    "list_users": list_users,
    "get_user_by_id": get_user_by_id,
    "update_user_auth": update_user_auth,
    "delete_user": delete_user,
    "count_users": count_users,
    "search_user_by_name": search_user_by_name,
}

def executor(plan):
    # -------- Logic for executor

    return "ERROR: Unknown action"

# ============================================================
# VALIDATOR
# ============================================================

def validator(llm, user_input, result):
    # ------- Logic for valdator
    return llm.invoke(prompt).content.strip()

# ============================================================
# ORCHESTRATOR
# ============================================================

def run_agent(llm, user_input, retries=2):

    for _ in range(retries):
        # ---------- Demo: Logic for orchestrating the planner, executor and validator
        if status == "VALID":
            return result

    return "FAILED"

# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    setup_db()
    seed_data()

    with open(r"E:\\Lenovo Ideapad 330\\company-material\\ai-upskill\\key-vault\\groq\\groq-api-key.txt") as f:
        api_key = f.read().strip()

    llm = get_llm(api_key)

    print("\n=== ADD USER ===")
    print(run_agent(llm, "Add user named Alice with id ML200"))

    print("\n=== SEARCH USER ===")
    print(run_agent(llm, "Find user with name Raj"))

    print("\n=== COUNT USERS ===")
    print(run_agent(llm, "How many users exist?"))

    print("\n=== UPDATE USER ===")
    print(run_agent(llm, "Set authentication of ML002 to 1"))

    print("\n=== DELETE USER ===")
    print(run_agent(llm, "Delete user ML003"))

    print("\n=== LIST USERS ===")
    print(run_agent(llm, "List all users"))