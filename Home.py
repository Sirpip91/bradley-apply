import streamlit as st
import pandas as pd
import os
import json
import plotly.express as px
import plotly.graph_objects as go

# ========== 🛠 Setup Paths ==========
DATA_DIR = "data"
TRACKER_FILE = os.path.join(DATA_DIR, "application_tracker.csv")
INFO_FILE = os.path.join(DATA_DIR, "common_info.json")

# ========== 📂 Ensure Files Exist ==========
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(INFO_FILE):
    with open(INFO_FILE, "w") as f:
        json.dump({}, f, indent=2)

if not os.path.exists(TRACKER_FILE):
    # Create an empty CSV with appropriate columns
    pd.DataFrame(columns=["Date", "Position", "Company", "Status", "Notes"]).to_csv(TRACKER_FILE, index=False)

# ========== 🖼️ Streamlit UI ==========
st.set_page_config(page_title="Job Hunt Home", layout="wide")
st.title("🏠 Welcome to Your Job Hunt Hub")

st.markdown("""
Welcome! This tool helps you streamline your job search process with:
- ✍️ **Cover letter generation**
- 🧠 **Storing common application information**
- 📊 **Application tracking and analytics**

Use the sidebar at top left to navigate each section.
""")

# ========== 🧭 Feature Instructions ==========
st.subheader("🧭 How to Use This App")

st.markdown("#### 1. 📤 Upload Resume")
st.markdown("""
Use the **Resume Upload** page to upload your resume. This can help auto-fill parts of your cover letter or profile information.
""")

st.markdown("#### 2. 🧠 Enter Common Info")
st.markdown("""
Go to **'Common Info'** to enter your basic info like name, address, school, graduation year, and a few work experiences.

This info will be used to:
- Easily copy/paste into job applications
- Speed up cover letter generation
""")

st.markdown("#### 3. ✉️ Generate Cover Letters")
st.markdown("""
Use the **Cover Letter Generator** page after uploading your resume and filling in job-specific details.

You can:
- Generate letters using AI
- Tailor them with your personal info
- The Cover letter will read job information and your resume and create a custom letter based off the two.
""")

st.markdown("#### 4. 📑 Track Job Applications")
st.markdown("""
Use the **Application Tracker** to log jobs you've applied to.

Track:
- Date
- Position
- Company
- Status
- Notes

This section lets you monitor progress and avoid double applying.
""")

st.markdown("#### 5. 📈 View Analytics")
st.markdown("""
As you log more applications, the dashboard here will update with visual charts to help track your progress.
""")

# ========== 📊 Application Status ==========
df = pd.read_csv(TRACKER_FILE)

if not df.empty:
    st.subheader("📊 Current Application Status Overview")

    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Applications by Status",
        hole=0.4,
    )
    fig.update_traces(textinfo='label+value')

    fig.add_annotation(
        dict(
            text=f"<b>{status_counts['Count'].sum()}</b><br>Total",
            x=0.5,
            y=0.5,
            font_size=20,
            showarrow=False,
            font=dict(color="black"),
            bgcolor="white",
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📋 View Recent Applications"):
        st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
else:
    st.info("No applications tracked yet. Head to **'Application Tracker'** to get started.")

# ✅ Call to action
st.success("Use the sidebar ➡️ to get started!")
