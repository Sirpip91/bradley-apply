import streamlit as st
import json
import os
from datetime import datetime

INFO_FILE = "data/common_info.json"

def load_info():
    if os.path.exists(INFO_FILE):
        with open(INFO_FILE, "r") as f:
            return json.load(f)
    return {}

def save_info(info):
    with open(INFO_FILE, "w") as f:
        json.dump(info, f, indent=2)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%b %d, %Y").date()
    except:
        try:
            return datetime.strptime(date_str, "%b %Y").date()
        except:
            return datetime.today().date()

st.title("🗃️ Required Information")
st.markdown("Enter the information, then press save at the bottom. You can come back anytime to edit or copy for your applications.")

info = load_info()

def get_val(key):
    return info.get(key, "")

# Single column layout with vertical inputs
st.header("👤 Personal Information 👤")
first_name = st.text_input("First Name", get_val("first_name"))
last_name = st.text_input("Last Name", get_val("last_name"))
email = st.text_input("Email", get_val("email"))
link = st.text_input("Link (will be used on cover letter)", get_val("link"))

st.markdown("---")

if st.button("💾 Save Information"):
    new_info = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "link": link,
    }
    save_info(new_info)
    st.success("Information saved! You can edit or copy directly from the fields above.")
