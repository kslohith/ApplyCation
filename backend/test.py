# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Initialize the webdriver (replace 'path/to/chromedriver' with the actual path to your Chrome driver)
# driver = webdriver.Chrome()

# # Navigate to the page with the form
# driver.get('https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Senior-Software-Engineer--Kubernetes---DGX-Cloud_JR1989230-1?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78')

# # Fill in the name
# # name_field = driver.find_element(By.ID, 'name')
# # name_field.send_keys('LOHITH KARIYAPLA SIDDALINGAPPA')

# # # Fill in the phone number
# # phone_field = driver.find_element(By.ID, 'phone')
# # phone_field.send_keys('+1(470)838-6791')

# # # Fill in the email
# # email_field = driver.find_element(By.ID, 'email')
# # email_field.send_keys('lks3@gatech.edu')

# # # Fill in the LinkedIn profile
# # linkedin_field = driver.find_element(By.ID, 'linkedin')
# # linkedin_field.send_keys('linkedin.com/in/lohithks')

# # # Fill in the GitHub profile
# # github_field = driver.find_element(By.ID, 'github')
# # github_field.send_keys('github.com/kslohith')

# # # Select the education level
# # education_level = driver.find_element(By.XPATH, "//label[contains(text(), 'Master of Science')]")
# # education_level.click()

# # # Select the programming languages
# # languages = ['Go', 'Java', 'Python', 'C', 'Javascript', 'SQL', 'C++']
# # for language in languages:
# #     language_checkbox = driver.find_element(By.XPATH, f"//label[contains(text(), '{language}')]")
# #     language_checkbox.click()

# # # Select the frameworks
# # frameworks = ['Tensorflow', 'Kubernetes', 'React', 'AWS', 'Docker', 'Microservices', 'Kafka', 'Pytorch']
# # for framework in frameworks:
# #     framework_checkbox = driver.find_element(By.XPATH, f"//label[contains(text(), '{framework}')]")
# #     framework_checkbox.click()

# # # Select the AWS certification
# # aws_cert_radio = driver.find_element(By.XPATH, "//label[contains(text(), 'AWS Certified Solutions Architect Associate')]")
# # aws_cert_radio.click()

# # # Fill in the experience details
# # experience_field = driver.find_element(By.ID, 'experience')
# # experience_field.send_keys('CitiBank, Cloudera, JP Morgan Chase & Co.')

# # # Fill in the research details
# # research_field = driver.find_element(By.ID, 'research')
# # research_field.send_keys('Advanced Database Systems Lab')

# # # Fill in the projects details
# # projects_field = driver.find_element(By.ID, 'projects')
# # projects_field.send_keys('GTSearch, Pgvector Remote')

# # # Submit the form
# # submit_button = driver.find_element(By.ID, 'submit')
# # submit_button.click()

# # Wait for the page to load after submission
# import time
# time.sleep(45)
# def execute(driver):
#     # Type text in "How Did You Hear About Us?*" field
#     # driver.find_element("input-1").send_keys("Referral")

#     # Select "Yes" radio button
#     driver.find_element("//label[text()=\'Yes\']/preceding-sibling::input").click()

#     # Type text in "First Name*" field
#     driver.find_element("input-4").send_keys("Lohith")

#     # Type text in "Last Name*" field
#     driver.find_element("input-5").send_keys("Kariyapla Siddalingappa")

#     # Check the checkbox (no label)
#     driver.find_element("input-6").click()

#     # Type text in "Address Line 1" field
#     driver.find_element("input-7").send_keys("Atlanta, Georgia")

#     # Type text in "City" field
#     driver.find_element("input-8").send_keys("Atlanta")

#     # Type text in "Postal Code" field
#     driver.find_element("input-10").send_keys("30332")

#     # Type text in "Country Phone Code*" field
#     driver.find_element("input-13").send_keys("+1")

#     # Type text in "Phone Number*" field
#     driver.find_element("input-14").send_keys("4708386791")

#     # Type text in "Phone Extension" field
#     driver.find_element("input-15").send_keys("")


# execute(driver)
# wait = WebDriverWait(driver, 90)
# wait.until(EC.presence_of_element_located((By.ID, 'success_message')))

# # Close the browser
# driver.quit()

# Function text received from the API (as a string)
# function_text = """
# def my_function(some_object):
#     print('Original function logic')
#     print(some_object)
# """

# # Modify the function to add custom logic
# additional_code = """
#     print('Added logic')
#     print('Value:', some_object.get('value', 'No value provided'))
# """
# # Find where to inject the code (e.g., before the function ends)
# modified_function_text = function_text.replace('print(some_object)', 'print(some_object)' + additional_code)

# # Execute the modified function code
# exec(modified_function_text)

# # Create the object to pass to the function
# my_object = {'value': 42}

# # Call the function with the created object
# my_function(my_object)



from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def execute(driver):
    # Fill in "How Did You Hear About Us?" field
    how_did_you_hear = driver.find_element(By.ID, "input-1")
    how_did_you_hear.send_keys("Referral")

    # Select "Yes" radio button
    yes_radio = driver.find_element(By.XPATH, "//label[contains(., \'Yes\')]/preceding-sibling::input")
    yes_radio.click()

    # Fill in "First Name" field
    first_name = driver.find_element(By.ID, "input-4")
    first_name.send_keys("Lohith")

    # Fill in "Last Name" field
    last_name = driver.find_element(By.ID, "input-5")
    last_name.send_keys("Kariyapla Siddalingappa")

    # Check "No label found" checkbox
    no_label_checkbox = driver.find_element(By.ID, "input-6")
    no_label_checkbox.click()

    # Fill in "Address Line 1" field
    address_line1 = driver.find_element(By.ID, "input-7")
    address_line1.send_keys("Atlanta, Georgia")

    # Fill in "City" field
    city = driver.find_element(By.ID, "input-8")
    city.send_keys("Atlanta")

    # Fill in "Postal Code" field
    postal_code = driver.find_element(By.ID, "input-10")
    postal_code.send_keys("30332")

    # Fill in "Country Phone Code" field
    country_phone_code = driver.find_element(By.ID, "input-13")
    country_phone_code.send_keys("+1")

    # Fill in "Phone Number" field
    phone_number = driver.find_element(By.ID, "input-14")
    phone_number.send_keys("4708386791")

    # Fill in "Phone Extension" field
    phone_extension = driver.find_element(By.ID, "input-15")
    phone_extension.send_keys("")
