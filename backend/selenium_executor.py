from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time


def initialize(url):
    # url = 'https://jobs.ashbyhq.com/snowflake/177a14c7-5c5f-4709-8986-98a7aab884f1/application?src=Simplify'
    driver = webdriver.Chrome()

    driver.get(url)
    return driver


def click_element_by_text(driver, text, timeout=10):
    try:
        # Define the XPath for the different elements that might contain the text
        xpath = (
            f"//button[contains(text(), '{text}')] | "
            f"//a[contains(text(), '{text}')] | "
            f"//input[@type='button' or @type='submit'][@value='{text}']"
        )

        # Wait until an element matching the XPath is visible
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )

        # Click the element once it's found and clickable
        element.click()
        print(f"Clicked the element with text: '{text}'")
        return True
    except Exception as e:
        print(f"Element with text '{text}' not found or not clickable within {timeout} seconds: {e}")
        return False



def click_button_in_popup(driver, button_text, timeout=15):
    try:
        # Wait for the pop-up to appear by checking for the presence of an element within the pop-up
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{button_text}')]"))
        )

        # Find the button with the specified text inside the pop-up
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{button_text}')]"))
        )
        
        # Click the button
        button.click()
        print(f"Clicked the '{button_text}' button in the pop-up.")
        return True
    except Exception as e:
        print(f"Failed to find or click the '{button_text}' button within {timeout} seconds: {e}")
        return False


def fill_and_submit_login_form(driver, email, password, timeout=15):
    try:
        # Find the email input field by locating the closest label with text "Email Address"
        email_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//label[contains(text(), 'Email Address')]/following::input[1] | "
                "//label[contains(text(), 'Email Address')]/ancestor::*[self::div or self::span]//input[1] | "
                "//label[contains(text(), 'Email Address')]/../following-sibling::input[1] | "
                "//input[@placeholder='Email Address']"
            ))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Find the password input field by looking for an input of type 'password'
        password_input = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((
                By.XPATH, "//input[@type='password' or @placeholder='Password']"
            ))
        )
        password_input.clear()
        password_input.send_keys(password)

        # Find and click the sign-in button by text or button type
        sign_in_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(text(), 'Sign In')] | //input[@type='submit' and @value='Sign In']"
            ))
        )
        hover = ActionChains(driver).move_to_element(sign_in_button)
        hover.click().perform()
        # sign_in_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "input-12"))
        # )
        # driver.execute_script("arguments[0].click();", sign_in_button)
        # sign_in_button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='signInSubmitButton']"))
        # )
        # print(sign_in_button)
        # driver.execute_script("arguments[0].scrollIntoView(true);", sign_in_button)

# Now click the Sign In button
        # sign_in_button.click()
        # driver.execute_script("arguments[0].scrollIntoView(true);", sign_in_button)
        # sign_in_button.click()
        # button = driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='signInSubmitButton']")
        # driver.execute_script("arguments[0].click();", button)

        print("Filled in the login form and clicked the sign-in button.")
        return True
    except Exception as e:
        print(f"Failed to fill in the login form or click the sign-in button: {e}")
        return False


def preprocess(driver, url):
    if 'workday' not in url:
        return
    try:
        if not click_element_by_text(driver, 'Apply'):
            raise Exception('error')
        if not click_button_in_popup(driver, 'Apply Manually'):
            raise Exception('error')
        if not fill_and_submit_login_form(driver, 'rmulumudy@gatech.edu', 'Spectre@573'):
            raise Exception('error')
        print("Successfully clicked the 'Apply' button.")

    except Exception as e:
        print(f"Could not find or click the 'Apply' button. Error: {str(e)}")

    # Wait for a moment to allow any page transitions
    time.sleep(2)


def close(driver):
    time.sleep(50)
    driver.quit()


def move_to_next_page(driver, timeout=20):
    move_to_next_page = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[contains(text(), 'Save and Continue')] | //input[@type='submit' and @value='Save and Continue']"
            ))
        )
    hover = ActionChains(driver).move_to_element(move_to_next_page)
    hover.click().perform()

def check_submit_button_exists(driver):
    try:
        # Try to find a button element with the text "Submit"
        submit_button = driver.find_element(By.XPATH, "//button[normalize-space(text())='Submit']")
        return True
    except NoSuchElementException:
        return False



def hardcoded_exec(driver):
    # Type text in "How Did You Hear About Us?*" field
    # driver.find_element("input-1").send_keys("Referral")

    input_field = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "input-1"))
    )
    input_field.click()

    menu_item = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'menuItem')]"))
    )

    # Click on the first element found
    menu_item.click()

    menu_item = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'menuItem')]"))
    )

    # Click on the first element found
    menu_item.click()


    dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "input-12"))
    )
    driver.execute_script("arguments[0].click();", dropdown_button)


    options = WebDriverWait(driver, 10).until(
    EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "[role='option']"))
    )

    # Iterate through the options, print their text, and click the desired one
    for option in options:
        print(option.text)  # This prints the text of each option
        if option.text == "Home":  # Replace "Home" with the desired option text
            option.click()
            break

    # # Select "Yes" radio button
    # driver.find_element("//label[text()=\'Yes\']/preceding-sibling::input").click()

    # # Type text in "First Name*" field
    # driver.find_element("input-4").send_keys("Lohith")

    # # Type text in "Last Name*" field
    # driver.find_element("input-5").send_keys("Kariyapla Siddalingappa")

    # # Check the checkbox (no label)
    # driver.find_element("input-6").click()

    # # Type text in "Address Line 1" field
    # driver.find_element("input-7").send_keys("Atlanta, Georgia")

    # # Type text in "City" field
    # driver.find_element("input-8").send_keys("Atlanta")

    # # Type text in "Postal Code" field
    # driver.find_element("input-10").send_keys("30332")

    # # Type text in "Country Phone Code*" field
    # driver.find_element("input-13").send_keys("+1")

    # # Type text in "Phone Number*" field
    # driver.find_element("input-14").send_keys("4708386791")

    # # Type text in "Phone Extension" field
    # driver.find_element("input-15").send_keys("")

def execute2(driver):
    # Fill in "How Did You Hear About Us?" field
    # how_did_you_hear = driver.find_element(By.ID, "input-1")
    # how_did_you_hear.send_keys("Referral")

    # Select "Yes" radio button
    # yes_radio = driver.find_element(By.XPATH, "//label[contains(., \'Yes\')]/preceding-sibling::input")
    # yes_radio.click()

    # Fill in "First Name" field
    first_name = driver.find_element(By.ID, "input-4")
    first_name.clear()
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




def execute3(driver):
    # Parse the website_metadata
    website_metadata = ['Type: radio, ID: 1, Label: Yes', 'Type: radio, ID: 2, Label: No', 'Type: text, ID: input-4, Label: First Name*', 'Type: text, ID: input-5, Label: Last Name*', 'Type: checkbox, ID: input-6, Label: No label found', 'Type: text, ID: input-7, Label: Address Line 1', 'Type: text, ID: input-8, Label: City', 'Type: text, ID: input-10, Label: Postal Code', 'Type: text, ID: input-14, Label: Phone Number*', 'Type: text, ID: input-15, Label: Phone Extension']

    # Parse the CV data
    cv_metadata = [
        'LOHITH KARIYAPLA SIDDALINGAPPA',
        '+1(470)838-6791',
        'Atlanta, Georgia',
        'lks3@gatech.edu',
        'linkedin.com/in/lohithks',
        'github.com/kslohith'
    ]

    # Fill in the form
    for item in website_metadata:
        item_type, item_id, item_label = item.split(', ')
        item_type = item_type.split(': ')[1]
        item_id = item_id.split(': ')[1]
        item_label = item_label.split(': ')[1]
        print(item_type, item_label, item_id)
        if item_type == 'radio':
            radio_buttons = driver.find_elements(By.XPATH, f"//label[contains(text(), '{item_label}')]/../input")
            for radio_button in radio_buttons:
                if radio_button.get_attribute('id') == item_id:
                    radio_button.click()
                    break
        elif item_type == 'text':
            if item_id == 'No id':
                text_field = driver.find_element(By.XPATH, f"//label[contains(text(), '{item_label}')]/../input")
            else:
                text_field = driver.find_element(By.ID, item_id)
            text_field.clear()
            if item_label == 'First Name*':
                text_field.send_keys(cv_metadata[0])
            elif item_label == 'Last Name*':
                text_field.send_keys(cv_metadata[0].split()[1])
            elif item_label == 'Address Line 1':
                text_field.send_keys(cv_metadata[2])
            elif item_label == 'City':
                text_field.send_keys(cv_metadata[2].split(',')[0])
            elif item_label == 'Postal Code':
                text_field.send_keys(cv_metadata[2].split(',')[1].strip())
            elif item_label == 'Phone Number*':
                text_field.send_keys(cv_metadata[1])
            elif item_label == 'Phone Extension':
                text_field.send_keys('')
        elif item_type == 'checkbox':
            checkbox = driver.find_element(By.ID, item_id)
            checkbox.click()



def select_radio_by_label(driver, label_text):
    label_xpath = f"//label[contains(text(), '{label_text}')]"
    label_element = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
    radio_xpath = ".//following::input[@type='radio'][1]"
    radio_button = label_element.find_element(By.XPATH, radio_xpath)
    radio_button.click()

def execute4(driver):
    wait = WebDriverWait(driver, 10)

    try:
        name_field = driver.find_element(By.ID, "_systemfield_name")
        name_field.clear()
        name_field.send_keys("LOHITH KARIYAPLA SIDDALINGAPPA")
    except:
        pass

    try:
        email_field = driver.find_element(By.ID, "_systemfield_email")
        email_field.clear()
        email_field.send_keys("lks3@gatech.edu")
    except:
        pass

    try:
        phone_field = driver.find_element(By.ID, "phone")
        phone_field.clear()
        phone_field.send_keys("(470)838-6791")
    except:
        pass

    try:
        linkedin_field = driver.find_element(By.ID, "question_26091185002")
        linkedin_field.clear()
        linkedin_field.send_keys("linkedin.com/in/lohithks")
    except:
        pass

    try:
        website_field = driver.find_element(By.ID, "question_26091186002")
        website_field.clear()
        website_field.send_keys("github.com/kslohith")
    except:
        pass

    try:
        recent_work_field = driver.find_element(By.ID, "question_26091187002")
        recent_work_field.clear()
        recent_work_field.send_keys("Cloudera")
    except:
        pass

    try:
        select_radio_by_label(driver, "I am a U.S. person.")
    except:
        pass

    try:
        select_radio_by_label(driver, "No - I have never been employed by PwC.")
    except:
        pass

    try:
        agree_checkbox = driver.find_element(By.ID, "46fcc0cc-af1b-4b47-a5e1-466841d30920_2ded3ef9-36d5-4e49-a11c-9cd79f053a35-labeled-checkbox-0")
        agree_checkbox.click()
    except:
        pass

    try:
        select_radio_by_label(driver, "Male")
    except:
        pass

    try:
        select_radio_by_label(driver, "Asian (Not Hispanic or Latino)")
    except:
        pass

    try:
        select_radio_by_label(driver, "I am not a protected veteran")
    except:
        pass

    # File upload
    resume_path = "/Users/rohith/Desktop/apply/selenium_gen/cvs/Sanjay Ramaswamy_resume.pdf"
    resume_upload = driver.find_element(By.ID, "_systemfield_resume")
    resume_upload.send_keys(resume_path)


    time.sleep(5)

# # url = 'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Senior-Software-Engineer--Kubernetes---DGX-Cloud_JR1989230-1?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78'
# url = 'https://jobs.ashbyhq.com/snowflake/177a14c7-5c5f-4709-8986-98a7aab884f1/application'
# driver = initialize(url)
# preprocess(driver, url)
# # hardcoded_exec(driver)
# execute4(driver)
# # move_to_next_page(driver)
# close(driver)