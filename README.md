

---

# 📄 LLM-Powered Resume Parser (ZIP ➜ CSV)

This project is an **AI-powered resume analysis system** built using **Streamlit**, **LangChain**, and **Google Gemini LLMs**.
It allows recruiters and HR teams to upload a **ZIP file containing multiple resumes (PDF/DOCX)** and automatically extract **structured candidate information** into a **downloadable CSV file**.

The system uses **LLM-driven structured output parsing** with **Pydantic schemas** for accuracy and consistency.

---

## 📌 Features

* Upload a **ZIP file** containing multiple resumes
* Supports **PDF** and **DOCX** resume formats
* Uses **Google Gemini LLM** via **LangChain**
* Extracts structured data:

  * Name
  * Email
  * Phone
  * Skills
  * Experience summary
  * Education
  * LinkedIn & GitHub URLs
* Enforces structured output using **PydanticOutputParser**
* Generates a **clean CSV file**
* Preview extracted data inside Streamlit
* Secure API key handling with **dotenv**
* Supports **user-provided API key override**

---

## 🧠 How the Code Works

### 1️⃣ Environment Setup

```python
load_dotenv()
```

* Loads environment variables from `.env`
* Keeps API keys secure and configurable

---

### 2️⃣ Streamlit Configuration

```python
st.set_page_config(
    page_title="Resume ZIP Analyzer | TektonAI",
    page_icon="📄",
    layout="wide"
)
```

* Sets application title, icon, and layout
* Optimized for wide data previews

---

### 3️⃣ Sidebar Controls

* Upload Gemini API key (optional override)
* Clear instructions for ZIP upload
* Branding and attribution

```python
user_api_key = st.text_input("🔑 Gemini API Key", type="password")
```

---

### 4️⃣ LLM Initialization

```python
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )
```

* Uses **Gemini Flash** for fast, deterministic output
* `temperature=0` ensures structured and stable responses
* LangChain acts as the LLM client

---

### 5️⃣ Structured Output Schema (Pydantic)

```python
class ResumeSchema(BaseModel):
    name: str
    email: str
    phone: str
    skills: str
    experience_summary: str
    education: str
    linkedin: str
    github: str
```

* Enforces **consistent schema**
* Prevents unstructured or noisy LLM output
* Ensures CSV-ready data

---

### 6️⃣ Prompt Engineering with Output Parser

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert HR resume analyzer..."),
    ("user", "Resume Text:\n{resume_text}\n\n{format_instructions}")
])
```

* System prompt defines HR expertise
* `format_instructions` strictly enforce schema output
* Combined with `PydanticOutputParser`

---

### 7️⃣ Resume File Readers

#### PDF Reader

```python
def read_pdf(path):
    reader = PdfReader(path)
```

#### DOCX Reader

```python
def read_docx(path):
    doc = Document(path)
```

* Extracts raw resume text for LLM processing

---

### 8️⃣ ZIP Processing Flow

```
ZIP Upload
   ↓
Extract Files
   ↓
Read PDF / DOCX
   ↓
LLM + Schema Parser
   ↓
Structured Resume Data
   ↓
CSV Generation
```

---

### 9️⃣ CSV Generation

```python
writer = csv.DictWriter(f, fieldnames=ResumeSchema.model_fields.keys())
```

* Automatically maps schema fields to CSV columns
* Generates clean, analysis-ready datasets

---

### 🔟 UI Output

* Downloadable CSV
* Live preview using `st.dataframe`
* Error handling for invalid resumes

---

## 📦 Dependencies

### `requirements.txt`

```txt
streamlit
langchain
langchain_google_genai
python-dotenv
pydantic
PyPDF2
python-docx
```

### Why These Dependencies?

| Package                | Purpose                      |
| ---------------------- | ---------------------------- |
| streamlit              | Web UI                       |
| langchain              | LLM orchestration            |
| langchain_google_genai | Google Gemini integration    |
| python-dotenv          | Secure API handling          |
| pydantic               | Structured output validation |
| PyPDF2                 | PDF text extraction          |
| python-docx            | DOCX text extraction         |

---

## 🔐 Why Use `dotenv`?

* Keeps API keys out of source code
* Prevents accidental GitHub leaks
* Supports environment-based configuration
* Allows user-provided API key override

### Example `.env`

```env
gemini=YOUR_GOOGLE_GEMINI_API_KEY
```

---

## 🚫 Why Use `.gitignore`?

Prevents sensitive and unnecessary files from being committed.

```gitignore
.env
__pycache__/
venv/
*.csv
*.zip
```

✅ Protects secrets
✅ Keeps repository clean
✅ Industry best practice

---

## 🚀 Run Locally (Step-by-Step)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/llm-resume-parser.git
cd llm-resume-parser
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add `.env` File (Optional)

```env
gemini=YOUR_GEMINI_API_KEY
```

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push project to **GitHub**
2. Open **Streamlit Cloud**
3. Select your repository
4. Add environment variable:

   ```
   gemini = YOUR_GEMINI_API_KEY
   ```
5. Deploy 🚀

---

## 📜 MIT License

```text
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

---

## 📚 Learning Outcomes

* LLM-driven document parsing
* Structured output enforcement with Pydantic
* ZIP file processing pipelines
* Resume NLP automation
* LangChain prompt orchestration
* CSV data engineering
* Production-ready Streamlit apps

---

## 🙌 Author

**Aashish**
AI / ML / GenAI Developer
TektonAI

---


