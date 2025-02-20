import os
import json
import io
import pdfplumber
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env file!")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# ✅ Improved text extraction from PDFs
def extract_text_from_pdf(file_bytes):
    try:
        file_stream = io.BytesIO(file_bytes)  # Convert bytes to a file-like object
        extracted_text = ""

        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

        return extracted_text.strip() if extracted_text.strip() else ""  # ✅ Return empty string instead of None
    except Exception as e:
        print(f"❌ Error extracting text: {str(e)}")
        return ""  # ✅ Return empty string in case of error

# ✅ Function to call Gemini API
def extract_resume_info(resume_text):
    if not resume_text.strip():
        return {"error": "Empty resume text"}

    prompt = f"""
    Extract structured information from this resume:
    
    {resume_text[:1500]}  # ✅ Limit text to first 1500 characters to avoid token overflow
    
    Return only a valid JSON object in the following format:
    ```
    {{
        "name": "Full Name",
        "email": "Email Address",
        "phone": "Phone Number",
        "core_skills": ["Skill1", "Skill2", "Skill3"],
        "soft_skills": ["Skill1", "Skill2"],
        "experience": "Work experience details",
        "education": "Education details",
        "resume_rating": 8,
        "improvement_areas": "Areas where the resume can be improved",
        "upskill_suggestions": "Suggestions for additional skills"
    }}
    ```
    Ensure the response **ONLY** contains a valid JSON object, without any extra text, explanation, or formatting.
    """

    try:
        response = model.generate_content(prompt)

        if not response or not hasattr(response, 'text') or not response.text.strip():
            return {"error": "Gemini API returned an empty response."}

        # ✅ Extract JSON manually if Gemini returns additional text
        raw_response = response.text.strip()
        json_start = raw_response.find("{")
        json_end = raw_response.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            return {"error": "Gemini API response does not contain a valid JSON.", "raw_response": raw_response}

        json_data = raw_response[json_start:json_end]

        # ✅ Parse JSON safely
        try:
            structured_data = json.loads(json_data)
            return structured_data
        except json.JSONDecodeError:
            return {"error": "Invalid JSON response from Gemini API.", "raw_response": raw_response}

    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}

