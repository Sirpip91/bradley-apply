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
        return datetime.strptime(date_str, "%b %Y").date()
    except:
        return datetime.today().date()

st.title("🗃️ Common Information")
st.header("Enter the information then at the bottom press save.")
st.markdown("You can then easily come back here to copy for your applications.")

info = load_info()

def get_val(key):
    return info.get(key, "")

# ------------------------------
# Personal Info Section
# ------------------------------
st.header("Personal Information 👤")

first_name = st.text_input("First Name", get_val("first_name"))
last_name = st.text_input("Last Name", get_val("last_name"))

st.markdown("---")

# ------------------------------
# Contact Info Section
# ------------------------------
st.header("Contact Information 📞")

email = st.text_input("Email", get_val("email"))
phone = st.text_input("Phone", get_val("phone"))

st.markdown("---")

# ------------------------------
# Online Profiles Section
# ------------------------------
st.header("Online Profiles 🌐")

linkedin = st.text_input("LinkedIn", get_val("linkedin"))
website = st.text_input("Website", get_val("website"))
github = st.text_input("GitHub", get_val("github"))

st.markdown("---")

# ------------------------------
# Address Details Section
# ------------------------------
st.header("Address Details 📍")

street = st.text_input("Street", get_val("street"))
city = st.text_input("City", get_val("city"))
state = st.text_input("State", get_val("state"))
zip_code = st.text_input("Zip Code", get_val("zip_code"))
country = st.text_input("Country", get_val("country"))

st.markdown("---")

# ------------------------------
# Work Experience Section
# ------------------------------
st.header("Work Experience 💼")

work_exp_list = info.get("work_experience", [])
num_jobs = st.number_input("Number of work experiences to have", min_value=1, max_value=10, value=max(len(work_exp_list), 1), step=1)

st.markdown("---")

work_experience_updated = []

for i in range(num_jobs):
    st.subheader(f"Work Experience #{i+1}")

    if i < len(work_exp_list):
        job = work_exp_list[i]
    else:
        job = {}

    job_title = st.text_input("Job Title", job.get("job_title", ""), key=f"job_title_{i}")
    company = st.text_input("Company", job.get("company", ""), key=f"company_{i}")

    # Parse saved dates
    start_date_val = parse_date(job.get("start_date", "Jan 2023"))
    end_date_val = None
    if job.get("end_date") and job.get("end_date").lower() != "present":
        end_date_val = parse_date(job.get("end_date"))

    current = st.checkbox("Currently Employed Here", value=job.get("current", False), key=f"current_{i}")

    start_date = st.date_input("Start Date", value=start_date_val, key=f"start_date_{i}")
    st.write("Formatted Start Date:", start_date.strftime("%b %d, %Y"))

    if not current:
        end_date = st.date_input("End Date", value=end_date_val if end_date_val else datetime.today().date(), key=f"end_date_{i}")
        st.write("Formatted End Date:", end_date.strftime("%b %d, %Y"))
    else:
        end_date = None

    duties = st.text_area("Job Duties", job.get("duties", ""), height=150, key=f"duties_{i}")

    work_experience_updated.append({
        "job_title": job_title,
        "company": company,
        "start_date": start_date.strftime("%b %d, %Y"),
        "end_date": "Present" if current else end_date.strftime("%b %d, %Y"),
        "current": current,
        "duties": duties,
    })



st.markdown("---")

if st.button("💾 Save Information"):
    new_info = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "website": website,
        "github": github,
        "street": street,
        "city": city,
        "state": state,
        "zip_code": zip_code,
        "country": country,
        "work_experience": work_experience_updated
    }
    save_info(new_info)
    st.success("Information saved! You can edit or copy directly from the fields above.")
