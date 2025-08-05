import streamlit as st
import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import datetime

# Load .env variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.warning(
        """
        ⚠️ **OpenAI API Key Required**  
        To generate cover letters, you must configure your OpenAI API key in the `.env` file or the app's ⚙️settings.  
        Make sure you have sufficient API credits available.  
        """
    )
    st.stop()  # Stop app if no API key
else:
    st.info(
        """
        ✅ OpenAI API key detected.  
        Note: generating cover letters consumes API credits. Monitor your usage to avoid unexpected charges.
        """
    )


    

openai = OpenAI(api_key=api_key)

# Folder where resumes are saved
RESUME_FOLDER = "resumes"
os.makedirs(RESUME_FOLDER, exist_ok=True)

# Base folder to save cover letters + job descriptions
BASE_OUTPUT_FOLDER = "cover_letters"
os.makedirs(BASE_OUTPUT_FOLDER, exist_ok=True)

# Streamlit Page Setup
st.set_page_config(page_title="Cover Letter Generator", layout="wide")
st.title("📄 AI Cover Letter Generator")

# List resumes in resumes folder
resume_files = [f for f in os.listdir(RESUME_FOLDER) if f.lower().endswith(".pdf")]
if not resume_files:
    st.warning("No resumes found! Please upload a resume on the Upload Resume page.")
    selected_resume = None
else:
    selected_resume = st.selectbox("Select Resume to Use", resume_files)

# Inputs to explicitly enter company name and job title (optional)
st.markdown("### Override extracted info (optional)")
explicit_title = st.text_input("Job Title (leave empty to auto-extract)")
explicit_company = st.text_input("Company Name (leave empty to auto-extract)")

# Text area for pasting job description
job_description_text = st.text_area("Paste Job Description Here")

# Function to extract PDF text
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

# Extract info from job description text
def extract_title_and_company(job_description):
    title_match = re.search(r'(?i)(Position|Title|Job Title)[:\s]*(.*)', job_description)
    company_match = re.search(r'(?i)(Company|Organization)[:\s]*(.*)', job_description)

    title = title_match.group(2).strip() if title_match else "Unknown_Position"
    company = company_match.group(2).strip() if company_match else "Unknown_Company"
    return title, company

# Sanitize strings for folder/file names
def sanitize_filename(s):
    s = s.lower()
    s = re.sub(r'\s+', '_', s)
    s = re.sub(r'[^\w\-]', '', s)  # remove everything except letters, digits, underscore, hyphen
    return s

# Button to generate cover letter
if st.button("Generate Cover Letter"):
    if selected_resume is None or not job_description_text.strip():
        st.error("Please select a resume and paste the job description.")
    else:
        # Extract or override title and company first (to build folder name)
        if explicit_title.strip():
            title = explicit_title.strip()
        else:
            title, _ = extract_title_and_company(job_description_text)

        if explicit_company.strip():
            company = explicit_company.strip()
        else:
            _, company = extract_title_and_company(job_description_text)

        # Sanitize company and title for safe folder naming
        safe_company = sanitize_filename(company)
        safe_title = sanitize_filename(title)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        folder_name = f"{safe_company}_{safe_title}_{timestamp}"
        session_folder = os.path.join(BASE_OUTPUT_FOLDER, folder_name)
        os.makedirs(session_folder, exist_ok=True)

        # Save the pasted job description
        job_desc_path = os.path.join(session_folder, "job_description.txt")
        with open(job_desc_path, "w", encoding="utf-8") as f:
            f.write(job_description_text)

        st.success(f"Job description saved to `{job_desc_path}`")

        # Extract text from selected resume PDF
        resume_path = os.path.join(RESUME_FOLDER, selected_resume)
        resume_text = extract_text_from_pdf(resume_path)

        # Prepare prompt
        role_description = (
            f"You are a cover letter generator with 20 years of experience. "
            f"Your task is to create a professional and concise cover letter body only, starting with the salutation (e.g., 'Dear Hiring Committee,') and ending before the signature or any closing formalities. "
            f"Do NOT include your name, contact information, date, enclosure lines, or signature. "
            f"Focus only on the core letter content tailored for the position of '{title}' at '{company}'."
        )

        structure = (
            "To compose a compelling cover letter, scrutinize the job description for key qualifications. "
            "Begin with a succinct introduction about the candidate's identity and career goals. "
            "Highlight skills aligned with the job, underpinned by tangible examples. "
            "Incorporate details about the company, emphasizing its mission or unique aspects that align with the candidate's values. "
            "Conclude by reaffirming the candidate's suitability, inviting further discussion. "
            "Do not make anything up, but feel free to use neighboring examples based on my resume. "
            "Use job-specific terminology and maintain a professional style suitable for the job role. "
            "Please provide your response in under 250 words."
        )

        content = f"{role_description}\n\n{structure}\n\nJob Description:\n{job_description_text}\n\nResume:\n{resume_text}"

        # Call OpenAI
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": role_description},
                {"role": "user", "content": content}
            ]
        )
        cover_letter = response.choices[0].message.content

        # Save generated cover letter in same folder
        cover_letter_path = os.path.join(session_folder, "cover_letter.txt")
        with open(cover_letter_path, "w", encoding="utf-8") as f:
            f.write(cover_letter)

        # Display generated cover letter
        st.subheader("📨 Generated Cover Letter")
        st.text_area("Cover Letter", cover_letter, height=300)

        # Download button
        st.download_button(
            label="📥 Download Cover Letter",
            data=cover_letter,
            file_name="cover_letter.txt",
            mime="text/plain"
        )
