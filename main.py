import io
import PyPDF2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon=":page_facing_up:")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format, and let the app review its content locally.")


def extract_pdf_text(uploaded_file) -> str:
    pdf_bytes = io.BytesIO(uploaded_file.getvalue())
    reader = PyPDF2.PdfReader(pdf_bytes)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages).strip()


def build_feedback(resume_text: str) -> list[str]:
    feedback: list[str] = []

    if len(resume_text) < 400:
        feedback.append("Add more detail about your impact, tools, and measurable results.")
    if "@" not in resume_text:
        feedback.append("Include a professional email address.")
    if not any(keyword in resume_text.lower() for keyword in ["experience", "work", "employment"]):
        feedback.append("Add a clear work experience section.")
    if not any(keyword in resume_text.lower() for keyword in ["skill", "tools", "technology"]):
        feedback.append("Add a dedicated skills section.")
    if not any(char.isdigit() for char in resume_text):
        feedback.append("Use numbers to show outcomes, for example percentages, revenue, or time saved.")

    if not feedback:
        feedback.append("The resume already covers the core basics well. Focus on sharper wording and stronger quantified achievements.")

    return feedback


uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    resume_text = extract_pdf_text(uploaded_file)

    if not resume_text:
        st.error("No readable text was found in this PDF.")
    else:
        st.subheader("Extracted Text Preview")
        st.text_area("Resume Text", resume_text[:3000], height=250)

        st.subheader("Resume Feedback")
        for item in build_feedback(resume_text):
            st.write(f"- {item}")

        st.caption("This review runs locally inside the Streamlit app.")
