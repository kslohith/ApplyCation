# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# import time

# # Sample JSON data
# data = {
#     "Name": "Sai Shirini Prathigadapa",
#     "Email": "saishirini3@gmail.com",
#     "Phone": "+1 716-275-9094",
#     "Resume": "/path/to/SaiShirini_Resume-1.pdf",  # Update this path
#     "LinkedIn Profile": "https://www.linkedin.com/in/sai-shirini-ba329b189/",
#     "Website": "https://github.com/SaiShirini3/Portfolio.git",
#     "Where have you most recently worked?": "University at Buffalo"
# }

# # Initialize the WebDriver
# driver = webdriver.Chrome()  # No need for executable_path if chromedriver is in the PATH

# # Open the application page
# driver.get("https://jobs.ashbyhq.com/snowflake/177a14c7-5c5f-4709-8986-98a7aab884f1/application")

# # Fill the form using the provided JSON data
# driver.find_element(By.ID, "_systemfield_name").send_keys(data["Name"])
# driver.find_element(By.ID, "_systemfield_email").send_keys(data["Email"])
# driver.find_element(By.ID, "phone").send_keys(data["Phone"])

# # Upload the resume
# # resume_upload = driver.find_element(By.ID, "_systemfield_resume")
# # resume_upload.send_keys(data["Resume"])

# # Fill LinkedIn Profile
# driver.find_element(By.ID, "question_26091185002").send_keys(data["LinkedIn Profile"])

# # Fill Website
# driver.find_element(By.ID, "question_26091186002").send_keys(data["Website"])

# # Fill 'Where have you most recently worked?'
# driver.find_element(By.ID, "question_26091187002").send_keys(data["Where have you most recently worked?"])

# # # Optional: Wait for a few seconds to review the form
# time.sleep(120)

# # # Close the driver
# # driver.quit()



# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import time

# # Initialize the webdriver (replace with your browser driver path)
# driver = webdriver.Chrome()

# # Open the target URL
# driver.get('https://jobs.ashbyhq.com/snowflake/177a14c7-5c5f-4709-8986-98a7aab884f1/application?src=Simplify')
# # Wait for elements to be available before interacting with them
# wait = WebDriverWait(driver, 10)

# # Data from the CV
# cv_data = {
#     'name': 'LOHITH KARIYAPLA SIDDALINGAPPA',
#     'email': 'lks3@gatech.edu',
#     'phone': '+1(470)838-6791',
#     'resume_path': '/path/to/resume.pdf',  # Change to the actual path of the resume file
#     'cover_letter_path': '/path/to/cover_letter.pdf',  # Change to the actual path of the cover letter file
#     'linkedin_profile': 'linkedin.com/in/lohithks',
#     'website': 'github.com/kslohith',
#     'recent_job': 'CitiBank',
#     'citizenship_status': 'None of the above; I am a citizen of a different country.',  # Adjust based on the option you want
#     'pwc_employment_status': 'No - I have never been employed by PwC.',
#     'privacy_notice': True,  # Set to True if the checkbox needs to be selected
#     'gender': 'Male',  # Adjust based on the option you want
#     'race': 'Asian (Not Hispanic or Latino)',  # Adjust based on the option you want
#     'veteran_status': 'I am not a protected veteran',  # Adjust based on the option you want
# }

# # Fill out the form fields using the IDs
# wait.until(EC.presence_of_element_located((By.ID, '_systemfield_name'))).send_keys(cv_data['name'])
# wait.until(EC.presence_of_element_located((By.ID, '_systemfield_email'))).send_keys(cv_data['email'])
# wait.until(EC.presence_of_element_located((By.ID, 'phone'))).send_keys(cv_data['phone'])
# # wait.until(EC.presence_of_element_located((By.ID, '_systemfield_resume'))).send_keys(cv_data['resume_path'])
# # wait.until(EC.presence_of_element_located((By.ID, 'cover_letter'))).send_keys(cv_data['cover_letter_path'])
# wait.until(EC.presence_of_element_located((By.ID, 'question_26091185002'))).send_keys(cv_data['linkedin_profile'])
# wait.until(EC.presence_of_element_located((By.ID, 'question_26091186002'))).send_keys(cv_data['website'])
# wait.until(EC.presence_of_element_located((By.ID, 'question_26091187002'))).send_keys(cv_data['recent_job'])

# def select_radio_by_label(label_text):
#     # Find the label element containing the specified text
#     label_xpath = f"//label[contains(text(), '{label_text}')]"
#     label_element = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
    
#     # Find the closest radio button input following the label
#     radio_xpath = ".//following::input[@type='radio'][1]"
#     radio_button = label_element.find_element(By.XPATH, radio_xpath)
#     radio_button.click()

# # Select radio buttons based on labels
# select_radio_by_label(cv_data['citizenship_status'])
# select_radio_by_label(cv_data['pwc_employment_status'])
# select_radio_by_label(cv_data['gender'])
# select_radio_by_label(cv_data['race'])
# select_radio_by_label(cv_data['veteran_status'])

# # Accept privacy notice checkbox if applicable
# if cv_data['privacy_notice']:
#     checkbox_xpath = "//label[contains(text(), 'I have read and agree to the Snowflake Candidate Privacy Notice')]/preceding-sibling::input[@type='checkbox']"
#     checkbox = wait.until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
#     checkbox.click()
# # Submit the form (if a submit button is present)
# # submit_button = wait.until(EC.presence_of_element_located((By.ID, 'submit_button_id')))
# # submit_button.click()

# # Close the driver after submission
# time.sleep(50)
# driver.quit()

import json
import logging
from html_downloader import get_website_fields
from generate_selenium import generate_selenium
from selenium_executor import initialize, close, preprocess, hardcoded_exec, move_to_next_page, check_submit_button_exists
import os
import requests
from urllib.parse import urlparse


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def download_file_to_cvs_folder(file_url):
    # Parse the file name from the URL
    parsed_url = urlparse(file_url)
    file_name = os.path.basename(parsed_url.path)
    
    # Create the 'cvs' folder at the same level as the current script if it doesn't exist
    cvs_folder_path = os.path.join(os.path.dirname(__file__), 'cvs')
    os.makedirs(cvs_folder_path, exist_ok=True)
    
    # Full path to save the downloaded file
    file_path = os.path.join(cvs_folder_path, file_name)
    
    # Download the file
    response = requests.get(file_url)
    response.raise_for_status()  # Ensure the request was successful

    # Save the content to the file
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    return file_path


def format_website_fields(job_url, website_metadata):
    if 'workday' not in job_url:
        return website_metadata
    
    # Labels to exclude
    exclude_labels = ['How Did You Hear About Us?', 'Country Phone Code', 'No label found']

    # Filtering out dictionaries with the specified labels
    filtered_metadata = [
        item for item in website_metadata
        if not any(exclude_label in item for exclude_label in exclude_labels)
    ]

    return filtered_metadata



with open('payload.txt', 'r') as f:    
    data = json.loads(f.read())

for key in data.keys():
    val = data[key]
    file_path = download_file_to_cvs_folder(val['cv'])
    val['jobs'] = eval(val['jobs'])
    for job_url in val['jobs']:
        logger.info(f'Started applying job: {job_url} for applicant: {key}')
        driver = initialize(job_url)
        preprocess(driver, job_url)
        while True:
            website_metadata = get_website_fields(job_url, driver)
            cv_metadata = val['raw_resume_text']
            cv_metadata += f",\n cv_path: {file_path},\n resume_path: {file_path}"
            print(file_path)
            print(website_metadata)
            website_metadata = format_website_fields(job_url, website_metadata)
            selenium_code = generate_selenium(website_metadata, cv_metadata)
            print(selenium_code)
            if selenium_code:
                exec(selenium_code)
                if not 'execute' not in locals() and 'execute' not in globals():
                    logger.warning("Function 'execute' not found. Skipping execution.")
                    break
                else:
                    try:
                        execute(driver)
                        hardcoded_exec(driver)
                    except:
                        logger.error("Unable to exec hardcoded stuff")
                    
                    if check_submit_button_exists(driver):
                        break
                    move_to_next_page(driver)
            else:
                logger.error('no selenium code exists')
                break
            close(driver)
            
        break
    logger.info(f'Job application done for {key}')
    break



