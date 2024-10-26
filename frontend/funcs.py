import pdfplumber
from keybert import KeyBERT
from difflib import SequenceMatcher
import re
import os
from google.cloud import firestore
from google.cloud import storage
import json

# Set the environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "root-array-439820-h6-32e68f23ed2e.json"

# Initialize Firestore client
db = firestore.Client()

# Initialize Google Cloud Storage client
storage_client = storage.Client()

# Function to extract text from PDF
def extract_text_from_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_skills_section(text):
    """Extracts the 'Skills' section from the resume text."""
    # Look for "Skills" section heading and capture text until the next section
    skills_match = re.search(r"(Skills|Technical Skills|Core Competencies)\s*[:\-]?\s*(.*?)(?=\n[A-Z][a-z]|\n\n|\Z)", text, re.IGNORECASE | re.DOTALL)
    if skills_match:
        return skills_match.group(2).strip()
    return text  # If no skills section found, return the whole text


def remove_similar_keywords(keywords):
    """Removes similar keywords to reduce redundancy."""
    unique_keywords = []
    for keyword, score in keywords:
        # Check if the keyword is similar to any in unique_keywords
        if not any(SequenceMatcher(None, keyword, k).ratio() > 0.8 for k, _ in unique_keywords):
            unique_keywords.append((keyword, score))
    return unique_keywords


# Initialize KeyBERT model
kw_model = KeyBERT()

def extract_keywords(text):
    # First, try to isolate the skills section
    # skills_text = extract_skills_section(text)
    
    # Extract a larger pool of keywords for diversity
    raw_keywords = kw_model.extract_keywords(
        # skills_text, 
        text,
        keyphrase_ngram_range=(1, 3), 
        stop_words="english", 
        top_n=50, 
        diversity=0.7
    )
    # Remove similar or redundant keywords, limit to top 30
    filtered_keywords = remove_similar_keywords(raw_keywords)
    return [kw[0] for kw in filtered_keywords][:30]

user_dict = {}
def create_user_profile(name, email, uploaded_file, job_role, job_type, experience, gender = None, race = None, sponsorship = None, veteran_status = None, disability_status = None) -> dict:
    """Creates a user profile dictionary."""
    resume_text = extract_text_from_pdf(uploaded_file)
    keywords = extract_keywords(resume_text)
    user_dict[name] = {
        "email": email,
        "job_role": job_role,
        "job_type": job_type,
        "experience": experience,
        "keywords": keywords,
        "uploaded_file": None,
        "raw_resume_text": resume_text,
        "gender": gender,
        "race": race,
        "sponsorship": sponsorship,
        "veteran_status": veteran_status,
        "disability_status": disability_status
    }
    return user_dict

def upload_user_profile_to_bucket(user_dict, bucket_name, filename="user_profile.json"):
    """Uploads the user_dict to Google Cloud Storage as a JSON file."""
    # Convert the dictionary to JSON format
    json_data = json.dumps(user_dict)
    
    # Specify the bucket and create a Blob (file object) in the bucket
    bucket = storage_client.get_bucket(bucket_name)
    name = list(user_dict.keys())[-1] 
    filename = f"{name}_profile.json" 
    blob = bucket.blob(filename)
    
    # Upload JSON data to the blob
    blob.upload_from_string(json_data, content_type="application/json")
    print(f"{filename} uploaded to {bucket_name}.")