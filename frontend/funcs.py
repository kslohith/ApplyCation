import pdfplumber
from keybert import KeyBERT
from difflib import SequenceMatcher
import re
import os
from google.cloud import firestore
from google.cloud import storage
import json
import anthropic
from dotenv import load_dotenv
load_dotenv()

claude_key = os.getenv("CLAUDE_API_KEY")
client = anthropic.Anthropic(
    api_key=claude_key,
)

# Set the environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

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

def claude_api_call(Prompt):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system="",
        messages=[
            {"role": "user", "content": Prompt} 
        ]
    )
    return message.content[0].text

def get_keyword(text):
    """Get keywords from a phrase using Claude API."""
    prompt = f"""Given the following text scraped from a resume, please extract and return a list of important skills and keywords that would be essential for job searching and helpful for matching with job descriptions. 
    Focus on technical skills, certifications, and relevant experiences that stand out.
    Resume Text:
    {text}
    Output format: Return the keywords as a Python list, e.g., ['keyword1', 'keyword2', 'keyword3']."""
    res = claude_api_call(prompt)
    # Extract only list from the response
    res_reg = re.findall(r'\[([^\]]+)\]', res)
    # print(res_reg)
    return res_reg

user_dict = {}
def create_user_profile(name, email, uploaded_file, job_role, job_type, experience, gender = None, race = None, sponsorship = None, veteran_status = None, disability_status = None) -> dict:
    """Creates a user profile dictionary."""
    resume_text = extract_text_from_pdf(uploaded_file)
    keywords = get_keyword(resume_text)
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