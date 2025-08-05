import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

# App config
st.set_page_config(page_title="Job Hunt Home", layout="wide")
st.title("🏠 Welcome to Your Job Hunt Hub")

st.markdown("""
Welcome! This tool helps you streamline your job search process with:
- ✍️ **Cover letter generation**
- 🧠 **Storing common application information**
- 📊 **Application tracking and analytics**

Use the sidebar at top left to navigate each section.
""")

# File path to tracker CSV
TRACKER_FILE = "data/application_tracker.csv"

# Feature Instructions
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

# Load application data if exists
if os.path.exists(TRACKER_FILE):
    df = pd.read_csv(TRACKER_FILE)
    st.subheader("📊 Current Application Status Overview")

    if not df.empty:
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]

        # Pie chart of application statuses
        fig = px.pie(
            status_counts,
            names="Status",
            values="Count",
            title="Applications by Status",
            hole=0.4  # Donut hole size,
        )
        fig.update_traces(textinfo='label+value')  # Show actual numbers instead of %

        # Add total count in the center
        total_apps = status_counts["Count"].sum()
        fig.add_annotation(
            dict(
                text=f"<b>{total_apps}</b><br>Total",
                x=0.5,
                y=0.5,
                font_size=20,
                showarrow=False,
                font=dict(color="black"),
                bgcolor="white",  # background color of annotation box
            )
        )

        st.plotly_chart(fig, use_container_width=True)
        with st.expander("📋 View Recent Applications"):
            st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
    else:
        st.info("No applications tracked yet. Head to **'Application Tracker'** to get started.")
else:
    st.info("No tracker file found. It will be created when you add your first application.")

# Call to action
st.success("Use the sidebar ➡️ to get started!")
