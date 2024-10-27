from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_core.utils.json import parse_json_markdown
from typing import List
import json
import re

class ResponseStructure(BaseModel):
    code: str = Field(description="selenium code to apply for the job")


# class RobustJsonOutputParser(JsonOutputParser):
#     def parse(self, text: str) -> ResponseStructure:
#         try:
#             # First, try to parse the entire text as JSON
#             return ResponseStructure(**json.loads(text))
#         except json.JSONDecodeError:
#             # If that fails, try to extract JSON from the text
#             try:
#                 json_obj = parse_json_markdown(text)
#                 return ResponseStructure(**json_obj)
#             except:
#                 # If all parsing attempts fail, raise an exception
#                 raise ValueError(f"Failed to parse output: {text}")


def extract_python_code(content):
    # Regular expression to capture the content between "```python" and "```"
    # Print the type of content
    print(f"Type of content: {type(content)}")
    content = str(content.content)
    print('\n\n\n')
    print(content.split('```python')[1].split('```')[0])
    match = re.search(r'```python\s*(.*?)\s*```', content, re.DOTALL)

    if match:
        return match.group(1)
    else:
        return None

def generate_selenium(website_metadata, cv_metadata):
    model = ChatAnthropic(model='claude-3-sonnet-20240229', anthropic_api_key='API_KEY')
# claude-3-haiku-20240307

    # parser = RobustJsonOutputParser(pydantic_object=ResponseStructure)
        #  given following html tags, cv info, generate a selenium script that fills the data from the cv. 
        #  for radio buttons can you search based on label. 
        #  for radio buttons directly check the closest input tag for the elemetn with text label_text
        #  assume that the driver is already created and you have to use the driver, create a function execute(driver):
        #  and put the code in it.
        #  Use selenium version compatible with 4.20.0
                    # Apart from Radio button, try to use id for all other elements, if no valid id ignore.
            # 


    prompt = ChatPromptTemplate.from_messages([
        ("system", """
            You are a python selenium expert.
            Given the following HTML tags and CV information, generate a Selenium script that fills in the data from the provided CV. 
            For radio buttons, search based on their associated labels. When handling radio buttons, identify the closest input tag to the element containing the label text.
            Clear each text field before writing the input.
            Remove +1 from phone number if exists.
            Apart from Radio button, try to use id for all other elements, if no valid id ignore.
            Also try to add catch block for each element you fill so that even if it fails, we can go ahead with others.
            Generate the entire code including file uploads if there is a valid file path in the provided cv metadata.
            Donot leave any code for user.
            cv path is under the key resume_path in cv_metadata, donot hardcode the path or read from env variable, use only if you get any data related to resume_path
            Use the following code template for radio buttons:\n\n
            def select_radio_by_label(label_text):
                label_element = wait.until(EC.presence_of_element_located((By.XPATH, label_xpath)))
                driver.find_elements(By.XPATH, f"//label[contains(text(), 'item_label')]/../input")
                radio_xpath = ".//following::input[@type='radio'][1]"
                radio_button = label_element.find_element(By.XPATH, radio_xpath)\n\n
            Make sure that the generated script executes correctly, i will give you 200 bucks.
            Assume that a Selenium WebDriver instance (driver) has already been created, and write a function named execute(driver) containing the code.
            Ensure compatibility with Selenium version 4.20.0.
            Input Format:
                website_metadata: Contains the HTML tags.
                cv_metadata: Contains the CV data.
         """),
        ("human", "\n\n{website_metadata}\n\n{cv_metadata}\n\n")
    ])

# Create a prompt template for parsing the HTML code
# template = PromptTemplate(
#     input_variables=["html_code"],
#     template=(
#         "Take the following HTML code and list the field names that the website needs as a list:"
#         "Return the output as a JSON object with a key 'field_names' containing an array of field names:\n\n"
#         "{html_code}\n\n"
#         "Output format:\n"
#         "{{\"field_names\": [\"name1\", \"name2\", \"name3\"]}}"
#     )
# )
# "Provide the output as a json object, with key field_names and value as a list of field names extracted from the above html"

# # Create the LLMChain with the specified template
# chain = LLMChain(llm=llm, prompt=template)


# # Get the response from the chain
# response = chain.run(html_code)

    chain = prompt | model 
# parser

    response = chain.invoke({"website_metadata": website_metadata, "cv_metadata": cv_metadata})

    print(response)

    return extract_python_code(response)



# code = """
# content='Here\'s a Selenium script that fills in the data from the provided CV:\n\n```python\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\n\ndef execute(driver):\n    # Website metadata\n    website_metadata = [\'Type: text, ID: input-1, Label: How Did You Hear About Us?*\', \'Type: radio, ID: 1, Label: Yes\', \'Type: radio, ID: 2, Label: No\', \'Type: text, ID: No id, Label: No label found\', \'Type: text, ID: input-4, Label: First Name*\', \'Type: text, ID: input-5, Label: Last Name*\', \'Type: checkbox, ID: input-6, Label: No label found\', \'Type: text, ID: input-7, Label: Address Line 1\', \'Type: text, ID: input-8, Label: City\', \'Type: text, ID: No id, Label: No label found\', \'Type: text, ID: input-10, Label: Postal Code\', \'Type: text, ID: No id, Label: No label found\', \'Type: text, ID: input-13, Label: Country Phone Code*\', \'Type: text, ID: input-14, Label: Phone Number*\', \'Type: text, ID: input-15, Label: Phone Extension\']\n\n    # CV metadata\n    cv_metadata = "LOHITH KARIYAPLA SIDDALINGAPPA\\n+1(470)838-6791 ⋄ Atlanta, Georgia\\nlks3@gatech.edu ⋄ linkedin.com/in/lohithks ⋄ github.com/kslohith"\n\n    # Fill in the data\n    for item in website_metadata:\n        item_type, item_id, item_label = item.split(\', \')\n        item_type = item_type.split(\': \')[1]\n        item_id = item_id.split(\': \')[1]\n        item_label = item_label.split(\': \', 1)[1]\n\n        if item_type == \'text\':\n            if item_id == \'No id\':\n                element = WebDriverWait(driver, 10).until(\n                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), \'{item_label}\')]/../input"))\n                )\n            else:\n                element = driver.find_element(By.ID, item_id)\n            element.clear()\n            element.send_keys(cv_metadata.split(\'\\n\')[0])\n        elif item_type == \'radio\':\n            if item_label == \'Yes\':\n                element = driver.find_element(By.ID, \'1\')\n            else:\n                element = driver.find_element(By.ID, \'2\')\n            element.click()\n        elif item_type == \'checkbox\':\n            element = driver.find_element(By.ID, item_id)\n            element.click()\n```\n\nThis script assumes that the Selenium WebDriver instance `driver` has already been created. The `execute(driver)` function contains the code to fill in the data from the provided CV.\n\nThe script first parses the `website_metadata` list to extract the type, ID, and label for each input field. It then uses the appropriate Selenium methods to locate the corresponding elements and fill in the data from the `cv_metadata` string.\n\nFor radio buttons, the script identifies the closest input tag to the element containing the label text using an XPath expression. It then clicks on the appropriate radio button based on the label.\n\nThe script clears each text field before writing the input to ensure that the data is properly filled in.\n\nThe script is compatible with Selenium version 4.20.0.' additional_kwargs={} response_metadata={'id': 'msg_011d4uEKAqzqEwVbZ8XCGcwD', 'model': 'claude-3-haiku-20240307', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 1073, 'output_tokens': 914}} id='run-7ad2f844-5a81-4e4b-bfc1-b53fd70c7724-0' usage_metadata={'input_tokens': 1073, 'output_tokens': 914, 'total_tokens': 1987, 'input_token_details': {}}
# """

# print(extract_python_code(code))



# code = """content='Here\'s the Selenium script that fills in the data from the provided CV:\n\n```python\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\n\ndef execute(driver):\n    # Radio buttons\n    radio_buttons = [\n        (\'Yes\', By.XPATH, "//label[contains(., \'Yes\')]/preceding-sibling::input"),\n        (\'No\', By.XPATH, "//label[contains(., \'No\')]/preceding-sibling::input")\n    ]\n\n    for label, by, xpath in radio_buttons:\n        radio_button = WebDriverWait(driver, 10).until(\n            EC.presence_of_element_located((by, xpath))\n        )\n        if label == \'Yes\':\n            radio_button.click()\n\n    # Text fields\n    text_fields = [\n        (\'First Name*\', By.ID, \'input-4\'),\n        (\'Last Name*\', By.ID, \'input-5\'),\n        (\'Address Line 1\', By.ID, \'input-7\'),\n        (\'City\', By.ID, \'input-8\'),\n        (\'Postal Code\', By.ID, \'input-10\'),\n        (\'Phone Number*\', By.ID, \'input-14\'),\n        (\'Phone Extension\', By.ID, \'input-15\')\n    ]\n\n    for label, by, id in text_fields:\n        input_field = WebDriverWait(driver, 10).until(\n            EC.presence_of_element_located((by, id))\n        )\n        input_field.clear()\n        input_field.send_keys(\n            {\n                \'First Name*\': \'Lohith\',\n                \'Last Name*\': \'Kariyapla Siddalingappa\',\n                \'Address Line 1\': \'Atlanta, Georgia\',\n                \'City\': \'Atlanta\',\n                \'Postal Code\': \'No id\',\n                \'Phone Number*\': \'+1(470)838-6791\',\n                \'Phone Extension\': \'\'\n            }[label]\n        )\n\n    # Checkbox\n    checkbox = WebDriverWait(driver, 10).until(\n        EC.presence_of_element_located((By.ID, \'input-6\'))\n    )\n    checkbox.click()\n```\n\nThis script uses the Selenium WebDriver to interact with the HTML elements provided in the `website_metadata` and fill in the data from the `cv_metadata`.\n\nHere\'s how the script works:\n\n1. It first handles the radio buttons. It identifies the radio button elements based on the associated labels and clicks the "Yes" radio button.\n2. Next, it handles the text fields. It finds the text input fields based on their IDs and clears the existing text before filling in the data from the CV.\n3. Finally, it interacts with the checkbox element and clicks it.\n\nThe script assumes that the Selenium WebDriver instance (`driver`) has already been created and passed to the `execute(driver)` function.\n\nNote that the script is compatible with Selenium version 4.20.0.' additional_kwargs={} response_metadata={'id': 'msg_01VEFhQuBiHoneBxcJmhpPvt', 'model': 'claude-3-haiku-20240307', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 1030, 'output_tokens': 742}} id='run-9c7cbe2d-ea43-40d5-add4-d219b74903e5-0' usage_metadata={'input_tokens': 1030, 'output_tokens': 742, 'total_tokens': 1772, 'input_token_details': {}}"""

# print(extract_python_code(code))


# code = """content='Here\'s the Selenium script that fills in the data from the provided CV:\n\n```python\nfrom selenium.webdriver.common.by import By\nfrom selenium.webdriver.support.ui import WebDriverWait\nfrom selenium.webdriver.support import expected_conditions as EC\nfrom selenium.common.exceptions import NoSuchElementException, TimeoutException\n\ndef execute(driver):\n    # Website metadata\n    website_metadata = [\'Type: radio, ID: 1, Label: Yes\', \'Type: radio, ID: 2, Label: No\', \'Type: text, ID: input-4, Label: First Name*\', \'Type: text, ID: input-5, Label: Last Name*\', \'Type: text, ID: input-7, Label: Address Line 1\', \'Type: text, ID: input-8, Label: City\', \'Type: text, ID: input-10, Label: Postal Code\', \'Type: text, ID: input-14, Label: Phone Number*\', \'Type: text, ID: input-15, Label: Phone Extension\']\n    \n    # CV metadata\n    cv_metadata = [\'LOHITH KARIYAPLA SIDDALINGAPPA\', \'+1(470)838-6791 ⋄ Atlanta, Georgia\', \'lks3@gatech.edu\', \'linkedin.com/in/lohithks\', \'github.com/kslohith\']\n\n    # Fill in the form\n    try:\n        # Radio buttons\n        for item in website_metadata:\n            if item.startswith(\'Type: radio\'):\n                label = item.split(\', \')[2].split(\': \')[1]\n                radio_button = driver.find_element(By.XPATH, f"//label[contains(., \'{label}\')]/preceding-sibling::input")\n                radio_button.click()\n    except NoSuchElementException:\n        print(f"Radio button with label \'{label}\' not found.")\n    \n    try:\n        # First Name\n        first_name_field = driver.find_element(By.ID, \'input-4\')\n        first_name_field.clear()\n        first_name_field.send_keys(cv_metadata[0].split(\' \')[0])\n    except NoSuchElementException:\n        print("First name field not found.")\n    \n    try:\n        # Last Name\n        last_name_field = driver.find_element(By.ID, \'input-5\')\n        last_name_field.clear()\n        last_name_field.send_keys(cv_metadata[0].split(\' \')[1])\n    except NoSuchElementException:\n        print("Last name field not found.")\n    \n    try:\n        # Address Line 1\n        address_line1_field = driver.find_element(By.ID, \'input-7\')\n        address_line1_field.clear()\n        address_line1_field.send_keys(cv_metadata[1].split(\' ⋄ \')[0])\n    except NoSuchElementException:\n        print("Address line 1 field not found.")\n    \n    try:\n        # City\n        city_field = driver.find_element(By.ID, \'input-8\')\n        city_field.clear()\n        city_field.send_keys(cv_metadata[1].split(\', \')[1].split(\' \')[0])\n    except NoSuchElementException:\n        print("City field not found.")\n    \n    try:\n        # Postal Code\n        postal_code_field = driver.find_element(By.ID, \'input-10\')\n        postal_code_field.clear()\n        postal_code_field.send_keys(cv_metadata[1].split(\', \')[1].split(\' \')[1])\n    except NoSuchElementException:\n        print("Postal code field not found.")\n    \n    try:\n        # Phone Number\n        phone_number_field = driver.find_element(By.ID, \'input-14\')\n        phone_number_field.clear()\n        phone_number = cv_metadata[1].split(\' ⋄ \')[0].replace(\'+1(\', \'\').replace(\')\', \'\')\n        phone_number_field.send_keys(phone_number)\n    except NoSuchElementException:' additional_kwargs={} response_metadata={'id': 'msg_01XFy4yqC7dCmUm37yx7iS7m', 'model': 'claude-3-haiku-20240307', 'stop_reason': 'max_tokens', 'stop_sequence': None, 'usage': {'input_tokens': 1031, 'output_tokens': 1024}} id='run-eed561d0-a203-4464-a08a-bad634d45810-0' usage_metadata={'input_tokens': 1031, 'output_tokens': 1024, 'total_tokens': 2055, 'input_token_details': {}}"""
# print(extract_python_code(code))