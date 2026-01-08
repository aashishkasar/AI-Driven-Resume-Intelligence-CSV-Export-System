# ============================================================
# LLM-Powered Resume Parser (ZIP -> CSV)
# Tech Stack: Streamlit, LangChain, Google Gemini, PDF/DOCX
# ============================================================

import os
import zipfile
import tempfile
import csv

import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

from PyPDF2 import PdfReader
from docx import Document

# ------------------------------------------------------------
# ENV SETUP
# ------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------
# STREAMLIT CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Resume ZIP Analyzer | TektonAI",
    page_icon="📄",
    layout="wide"
)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 Resume Analyzer")
    st.markdown("🦜🔗 **Powered by LangChain + Gemini LLMs**")
    st.divider()

    user_api_key = st.text_input(
        "🔑 Gemini API Key",
        type="password",
        help="Optional: Override system Gemini key"
    )

    st.markdown(
        """
        ### 📌 Instructions
        - Upload a ZIP file
        - Resumes can be **PDF or DOCX**
        - Click **Analyze Resumes**
        - Download structured CSV
        """
    )

    st.divider()
    st.caption("Designed & Developed by **Aashish**")
    st.caption("TektonAI © 2026")

# ------------------------------------------------------------
# API KEY RESOLUTION
# ------------------------------------------------------------
if user_api_key:
    os.environ["GOOGLE_API_KEY"] = user_api_key
else:
    os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# ------------------------------------------------------------
# MAIN UI
# ------------------------------------------------------------
st.title("📦 Resume ZIP ➜ 🧾 Structured CSV")
st.caption("🦜 Powered by **LangChain** | ⚡ Gemini LLMs")
st.markdown(
    "Automatically extract **skills, experience, education, and profiles** from resumes using **LLMs**."
)

# ------------------------------------------------------------
# LLM SETUP
# ------------------------------------------------------------
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

# ------------------------------------------------------------
# STRUCTURED OUTPUT SCHEMA
# ------------------------------------------------------------
class ResumeSchema(BaseModel):
    name: str = Field(description="Candidate full name")
    email: str = Field(description="Email address")
    phone: str = Field(description="Phone number")
    skills: str = Field(description="Technical skills")
    experience_summary: str = Field(description="Short work experience summary")
    education: str = Field(description="Education details")
    linkedin: str = Field(description="LinkedIn profile URL")
    github: str = Field(description="GitHub profile URL")

parser = PydanticOutputParser(pydantic_object=ResumeSchema)

# ------------------------------------------------------------
# PROMPT TEMPLATE
# ------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert HR resume analyzer. Extract resume information strictly in the given schema."),
    ("user", "Resume Text:\n{resume_text}\n\n{format_instructions}")
])

# ------------------------------------------------------------
# FILE READERS
# ------------------------------------------------------------
def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "".join(page.extract_text() or "" for page in reader.pages)

def read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

# ------------------------------------------------------------
# RESUME PROCESSOR
# ------------------------------------------------------------
def extract_resume_data(resume_text: str) -> dict:
    llm = get_llm()
    chain = prompt | llm | parser
    result = chain.invoke({
        "resume_text": resume_text,
        "format_instructions": parser.get_format_instructions()
    })
    return result.dict()

# ------------------------------------------------------------
# ZIP HANDLER
# ------------------------------------------------------------
def process_zip(zip_file) -> list[dict]:
    extracted_data = []

    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file.name)
        with open(zip_path, "wb") as f:
            f.write(zip_file.getbuffer())

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        for root, _, files in os.walk(temp_dir):
            for file in files:
                path = os.path.join(root, file)

                if file.lower().endswith(".pdf"):
                    text = read_pdf(path)
                elif file.lower().endswith(".docx"):
                    text = read_docx(path)
                else:
                    continue

                if text.strip():
                    try:
                        extracted_data.append(extract_resume_data(text))
                    except Exception as e:
                        st.warning(f"⚠️ Failed to parse {file}: {e}")

    return extracted_data

# ------------------------------------------------------------
# CSV WRITER
# ------------------------------------------------------------
def write_csv(data: list[dict]) -> str:
    temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    fieldnames = list(ResumeSchema.model_fields.keys())

    with open(temp_csv.name, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return temp_csv.name

# ------------------------------------------------------------
# UI ACTIONS
# ------------------------------------------------------------
uploaded_zip = st.file_uploader(
    "📦 Upload ZIP file containing resumes",
    type=["zip"]
)

if uploaded_zip:
    st.info(f"Uploaded: **{uploaded_zip.name}**")

    if st.button("🔍 Analyze Resumes", use_container_width=True):
        with st.spinner("Processing resumes with Gemini..."):
            results = process_zip(uploaded_zip)

        if results:
            csv_path = write_csv(results)

            st.success(f"✅ Processed {len(results)} resumes")

            with open(csv_path, "rb") as f:
                st.download_button(
                    "⬇️ Download CSV",
                    data=f,
                    file_name="resume_analysis.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            st.subheader("📊 Preview")
            st.dataframe(results, use_container_width=True)
        else:
            st.error("❌ No valid resumes found")
