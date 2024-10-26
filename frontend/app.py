import streamlit as st
from funcs import *

st.set_page_config(page_title="📝 Smart Apply", page_icon="📝", layout="centered")

st.title("📝 Smart Apply!")

name = st.text_input("Full Name *", placeholder="John Doe")
email = st.text_input("Email Address *", placeholder="you@example.com")

st.write("## Upload Your Resume")
uploaded_file = st.file_uploader("Choose your resume file *", type=("pdf"))

st.write("## Job Preferences")
job_roles = st.multiselect(
    "Select the roles you're interested in: *",
    ["Software Engineer", "Data Scientist", "Product Manager", "UI/UX Designer", "DevOps Engineer", "Project Manager", "Analyst", "Marketing Specialist", "Other"],
    help="Select one or more roles that match your interests"
)
other_role = ""
if "Other" in job_roles:
    other_role = st.text_input("Please specify other role")

job_type = st.selectbox(
    "What type of job are you looking for? *",
    ["Select an option", "Full-time", "Part-time", "Internship", "Contract", "Temporary"],
    help="Select the type of job you are looking for."
)

# Experience Level
experience_level = st.selectbox(
    "What is your experience level? *",
    ["Select an option", "Entry-level", "Mid-level", "Senior-level"],
    help="Select your experience level."
)

st.write("## Demographic Information")
# Demographic Information
gender = st.selectbox(
    "Gender",
    ["Select your gender", "Female", "Male", "Non-binary", "Prefer not to say", "Other"]
)
if gender == "Other":
    gender = st.text_input("Please specify your gender")

race_ethnicity = st.selectbox(
    "Race/Ethnicity",
    ["Select your race/ethnicity", "Asian", "Black or African American", "Hispanic or Latino", "White", "Native American or Alaska Native", "Native Hawaiian or Pacific Islander", "Prefer not to say", "Other"]
)
if race_ethnicity == "Other":
    race_ethnicity = st.text_input("Please specify your race/ethnicity")

sponsorship = st.selectbox(
    "Will you require sponsorship now or in the future?",
    ["Select an option", "Yes", "No"],
    help="Indicate if you will require work sponsorship for this role.",
)

veteran_status = st.selectbox(
    "Are you a veteran?",
    ["Select an option", "Yes", "No", "Prefer not to say"],
    placeholder= "Select an option",
)

disability_status = st.selectbox(
    "Do you have a disability?",
    ["Select an option", "Yes", "No", "Prefer not to say"],
    placeholder= "Select an option",
)

# Add a button to submit the form
if st.button("Submit"):
    if uploaded_file and job_roles and email and name and job_type and experience_level:
        st.success("Information submitted successfully!")
        users = create_user_profile(name, email, uploaded_file, job_roles, job_type, experience_level)
        users_with_resume = upload_resume_to_bucket(uploaded_file, users, "candidate_resume_smart_apply")
        upload_user_profile_to_bucket(users_with_resume, "candidate_data_smart_apply")
    else:
        st.info("Please complete all the required fields above to proceed.")

