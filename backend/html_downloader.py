from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def fetch_html_main(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to the URL
        page.goto(url)
        
        # Wait for a specific element to load (optional)
        page.wait_for_selector("h1")  # Change selector as needed
        
        # Get the HTML content
        html_code = page.content()
        
        # Close the browser
        browser.close()
        
        return html_code


def fetch_html(url, driver):
    time.sleep(5)
    
    html_source = driver.page_source

    return html_source
 



# def get_sibling(input_tag, soup):
#     # 3. Check for siblings (span, div, or text) directly next to the input
#     sibling_texts = []
#     for sibling in input_tag.find_previous_siblings():
#         if sibling.name in ['span', 'div', 'label', 'p']:
#             sibling_texts.append(sibling.get_text(strip=True))
#     for sibling in input_tag.find_next_siblings():
#         if sibling.name in ['span', 'div', 'label', 'p']:
#             sibling_texts.append(sibling.get_text(strip=True))
    
#     # 4. Check siblings of the parent (uncle elements)
#     parent = input_tag.find_parent()
#     if parent:
#         for sibling in parent.find_previous_siblings():
#             if sibling.name in ['span', 'div', 'label', 'p']:
#                 sibling_texts.append(sibling.get_text(strip=True))
#         for sibling in parent.find_next_siblings():
#             if sibling.name in ['span', 'div', 'label', 'p']:
#                 sibling_texts.append(sibling.get_text(strip=True))
    
#     # 5. Check siblings of the grandparent (if the parent didn't have any meaningful labels)
#     grandparent = parent.find_parent() if parent else None
#     if grandparent:
#         for sibling in grandparent.find_previous_siblings():
#             if sibling.name in ['span', 'div', 'label', 'p']:
#                 sibling_texts.append(sibling.get_text(strip=True))
#         for sibling in grandparent.find_next_siblings():
#             if sibling.name in ['span', 'div', 'label', 'p']:
#                 sibling_texts.append(sibling.get_text(strip=True))


def get_label(input_tag, soup):
    # 1. Check if the input has an associated label with 'for' attribute
    if 'id' in input_tag.attrs:
        label = soup.find('label', {'for': input_tag['id']})
        if label:
            return label.get_text(strip=True)
    
    # 2. Check if the input is wrapped inside a <label> directly
    parent_label = input_tag.find_parent('label')
    if parent_label:
        return parent_label.get_text(strip=True)
    
    # 3. Check if the input is inside a div or similar and the previous sibling is a text/label
    prev_sibling = input_tag.find_previous_sibling()
    if prev_sibling and prev_sibling.name in ['label', 'div', 'span', 'p']:
        return prev_sibling.get_text(strip=True)
    
    # 4. Check for text in the grandparent or further up, like a div containing descriptive text
    grandparent = input_tag.find_parent(['div', 'span'])
    if grandparent:
        # Find any text nodes or labels directly within this container
        label_texts = grandparent.find_all(text=True, recursive=False)
        if label_texts:
            return ' '.join(text.strip() for text in label_texts if text.strip())

    # No label found
    return None



def format_html(html_code):
    # print(html_code)
    lst = []
    soup = BeautifulSoup(html_code, 'html.parser')
    input_elements = soup.find_all('input')
    for input_tag in input_elements:
        # input_type = input_tag.get('type', 'text')
        # input_name = input_tag.get('name')
        # input_placeholder = input_tag.get('placeholder', '')
        # input_value = input_tag.get('value', '')
        input_type = input_tag.get('type', 'text')
        input_id = input_tag.get('id', 'No id')
        input_label = get_label(input_tag, soup) or 'No label found'
        # sibling_label = get_sibling(input_tag, soup) or 'No label found'
        
        lst.append(f'Type: {input_type}, ID: {input_id}, Label: {input_label}')
    

    # Extract button elements with values 'Yes' or 'No'
    button_elements = soup.find_all('button')
    for button_tag in button_elements:
        button_value = button_tag.get('value', '').strip().lower()
        if button_value in ['yes', 'no']:
            button_id = button_tag.get('id', 'No id')
            button_label = get_label(button_tag, soup) or 'No label found'
            
            lst.append(f'Type: button, ID: {button_id}, Label: {button_label}, Value: {button_value.capitalize()}')
    

    return lst


def get_website_fields(url, driver = None):
    # Usage
    # url = 'https://jobs.ashbyhq.com/snowflake/177a14c7-5c5f-4709-8986-98a7aab884f1/application'
    html = ''
    if driver:
        html = fetch_html(url, driver)
    else:
        html = fetch_html_main(url)

    return format_html(html)



# print(get_website_fields('https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/US-CA-Santa-Clara/Senior-Software-Engineer--Kubernetes---DGX-Cloud_JR1989230-1?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8&jobFamilyGroup=0c40f6bd1d8f10ae43ffaefd46dc7e78'))
# print(get_website_fields('https://jobs.ashbyhq.com/snowflake/177a14c7-5c5f-4709-8986-98a7aab884f1/application'))