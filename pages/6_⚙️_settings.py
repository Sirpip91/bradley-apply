import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Settings")

st.title("⚙️ Settings")

# Path to .env file
env_path = Path(".env")

# Function to load key from .env
def load_api_key():
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith("OPENAI_API_KEY="):
                return line.strip().split("=", 1)[1]
    return ""

# Function to save key to .env (overwrite or add)
def save_api_key(key):
    lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()

    key_line = f"OPENAI_API_KEY={key}\n"
    key_written = False
    for i, line in enumerate(lines):
        if line.startswith("OPENAI_API_KEY="):
            lines[i] = key_line
            key_written = True
            break

    if not key_written:
        lines.append(key_line)

    with open(env_path, "w") as f:
        f.writelines(lines)

# Load existing key but do NOT show it in the input field (security)
stored_key = load_api_key()

st.markdown("""
### How to get your OpenAI API key
1. Go to [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).
2. Create a new secret key if you don't have one.
3. Copy the key to your clipboard.
4. Paste it into the input below and click **Save**.
5. Head to cover letter generator to start using the AI powered generator.
""")

api_key_input = st.text_input("Enter your OpenAI API key", type="password", placeholder="sk-...")

if st.button("Save API Key"):
    if api_key_input.strip() == "":
        st.error("Please enter a valid API key.")
    else:
        save_api_key(api_key_input.strip())
        st.success("API key saved to `.env` file securely! PLEASE REFRESH PAGE TO SEE CHANGES")

if stored_key:
    st.info("You have an API key saved. For security, the value is hidden.")
else:
    st.warning("No API key found. Please enter your key to use OpenAI features.")
