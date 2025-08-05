import streamlit as st
import os

RESUME_FOLDER = "resumes"
os.makedirs(RESUME_FOLDER, exist_ok=True)

st.title("📤 Manage Uploaded Resumes")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    save_path = os.path.join(RESUME_FOLDER, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Saved resume: {uploaded_file.name}")

st.markdown("---")
st.subheader("Your Uploaded Resumes")

resume_files = os.listdir(RESUME_FOLDER)
if not resume_files:
    st.info("No resumes uploaded yet.")
else:
    resume_to_delete = None

    for resume_name in resume_files:
        col1, col2, col3 = st.columns([6, 1, 1])
        with col1:
            st.write(resume_name)
        with col2:
            pdf_path = os.path.join(RESUME_FOLDER, resume_name)
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            st.download_button(
                label="View",
                data=pdf_bytes,
                file_name=resume_name,
                mime="application/pdf",
                key=f"download_{resume_name}"
            )
        with col3:
            if st.button("Delete", key=f"delete_{resume_name}"):
                resume_to_delete = resume_name

    if resume_to_delete:
        os.remove(os.path.join(RESUME_FOLDER, resume_to_delete))
        st.info(f"Resume '{resume_to_delete}' deleted. Please refresh the page.")
