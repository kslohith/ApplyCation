import pdfplumber
from keybert import KeyBERT
from difflib import SequenceMatcher
import re

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