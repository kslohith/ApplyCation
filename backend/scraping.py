from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from google.cloud import storage
import time
import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

claude_key = os.getenv("CLAUDE_API_KEY")

client = anthropic.Anthropic(
    api_key=claude_key,
)

google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_application_credentials

def claude_api_call(Prompt):
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        system="",
        messages=[
            {"role": "user", "content": Prompt} 
        ]
    )
    return message.content[0].text
# def claude_api_call(Prompt):
#     message = client.messages.create(
#         model="claude-3-haiku-20240307",
#         max_tokens=1024,
#         system="",
#         messages=[
#             {"role": "user", "content": Prompt} 
#         ]
#     )
#     return message.content[0].text

def download_from_bucket(bucket_name):
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # List all blobs in the bucket
    blobs = bucket.list_blobs()

    all_candidate_data = []

    for blob in blobs:
        if blob.name.endswith('.json'):
            # Download the blob content as a string
            json_data = blob.download_as_string()

            # Parse the JSON data
            data = json.loads(json_data)

            all_candidate_data.append(data)

    return all_candidate_data


def get_relevant_jobs():
    # Load all the candidate data from the Database (Google Cloud)
    candidate_data = download_from_bucket('candidate_data_smart_apply')

    # Scrap all jobs from the relevant websites
    driver = webdriver.Chrome()

    wait = WebDriverWait(driver, 10)

    company_urls = [
        #'https://mastercard.wd1.myworkdayjobs.com/en-US/CorporateCareers',
        # 'https://intel.wd1.myworkdayjobs.com/en-US/External',
        # 'https://trimble.wd1.myworkdayjobs.com/en-US/TrimbleCareers/',
        'https://nvidia.wd5.myworkdayjobs.com/NVIDIAExternalCareerSite?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78',
        # 'https://cvshealth.wd1.myworkdayjobs.com/CVS_Health_Careers',
        # 'https://motorolasolutions.wd5.myworkdayjobs.com/en-US/Careers/',
        # 'https://bah.wd1.myworkdayjobs.com/en-US/BAH_Jobs', 
    ]  # Add your company URLs here

    jobs = []
    for company_url in company_urls:
        jobstosend = []
        driver.get(company_url)
        try:
            today = True
            while today:
                time.sleep(2)
                wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
                
                job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')

                for job_element in job_elements:
                    job_title_element = job_element.find_element(By.XPATH, './/h3/a')
                    job_id_element = job_element.find_element(By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
                    job_id = job_id_element.text
                    posted_on_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
                    posted_on = posted_on_element.text
                    if 'posted today' in posted_on.lower() or 'posted yesterday' in posted_on.lower():
                        job_href = job_title_element.get_attribute('href')
                        job_title = job_title_element.text
                        # To Do: Save the jobs which are already applied and dont add them to the list
                        jobstosend.append((job_title, job_href))
                    else:
                        today = False
                        break
                next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
                if "disabled" in next_button.get_attribute("class"):
                    break  # exit loop if the "next" button is disabled
                next_button.click()
        except Exception as e:
            print(f"An error occurred while processing {company_url}: {str(e)}")
            continue

        for job_title, job_href in jobstosend:
            driver.get(job_href)
            time.sleep(1)
            job_posting_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-automation-id="job-posting-details"]')))
            job_posting_text = job_posting_element.text
            job_keyword_prompt = f"""Given the job posting: {job_posting_text}, find the keywords that best describe the job. Return the top 10 most relavent and important keywords in the format. Return in this format: [Keyword1,keyword2,...keyword10]. Do not return anything apart from this."""
            job_keywords = claude_api_call(job_keyword_prompt) 
            jobs.append((job_title, job_href, job_keywords))

    candidate_relevent_jobs = {}

    for candidate in candidate_data:
        for name, details in candidate.items():
            candidate_relevent_jobs[name] = {}
            candidate_relevent_jobs[name]['resume_url'] = details.get('resume_url')
            candidate_relevent_jobs[name]['skills'] = details.get('keywords', [])
            candidate_relevent_jobs[name]['raw_resume_text'] = details.get('raw_resume_text')
            #Use the candidate data and job data to find best matches
            Prompt = f"""Given the following skills from my resume: {candidate_relevent_jobs[name]['skills']}, find the jobs that best match my skills out of the following jobs: {jobs}.
                Then, filter the jobs based on the following criteria: 
                - Job Role: {candidate_relevent_jobs[name]['job_role']}
                - Job Type: {candidate_relevent_jobs[name]['job_type']}
                - Experience Level: {candidate_relevent_jobs[name]['experience']}
                - Sponsorship: {candidate_relevent_jobs[name]['sponsorship']}
                Only return jobs that closely match the skills and the specified criteria; otherwise, return an empty dict. 
                Return in the format: [job_url1, job_url2,...]. Do not return anything else, just return the list of strings containing job URLs."""
            candidate_relevent_jobs[name]['jobs'] = claude_api_call(Prompt)
    
    return candidate_relevent_jobs
