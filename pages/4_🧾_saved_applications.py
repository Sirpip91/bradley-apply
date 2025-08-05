import streamlit as st 
import pandas as pd
import os
import datetime

# File location
TRACKER_FILE = "data/application_tracker.csv"

# Ensure file exists
if not os.path.exists(TRACKER_FILE):
    df_init = pd.DataFrame(columns=["Date", "Position", "Company", "Location", "Status", "Notes"])
    df_init.to_csv(TRACKER_FILE, index=False)

# Load existing data
df = pd.read_csv(TRACKER_FILE)

# Streamlit config
st.set_page_config(page_title="Application Tracker", layout="wide")
st.title("📊 Job Application Tracker")

# Add new application form
with st.form("add_application_form", clear_on_submit=True):
    st.subheader("➕ Add New Application")

    col1, col2 = st.columns(2)
    with col1:
        position = st.text_input("Position")
        company = st.text_input("Company")
        location = st.text_input("Location")
    with col2:
        date_applied = st.date_input("Date Applied", value=datetime.date.today())
        status = st.selectbox("Status", ["Applied", "Interviewing", "Offer", "Rejected"])
        notes = st.text_area("Notes (optional)")

    submitted = st.form_submit_button("Add Application")
    if submitted:
        new_row = {
            "Date": date_applied.strftime("%Y-%m-%d"),
            "Position": position.strip(),
            "Company": company.strip(),
            "Location": location.strip(),
            "Status": status,
            "Notes": notes.strip()
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(TRACKER_FILE, index=False)
        st.success(f"✅ Application to {company} for '{position}' added!")

# Editable Data Table
st.subheader("📄 Tracked Applications")
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    key="editable_applications"
)

# Save changes
if st.button("💾 Save Changes"):
    edited_df.to_csv(TRACKER_FILE, index=False)
    st.success("✅ Changes saved to application tracker!")
