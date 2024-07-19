import requests
from bs4 import BeautifulSoup
import random
import os

try:
    # Create session
    session = requests.Session()
    
    # Get the form page
    form_url = "https://enquiry.icegate.gov.in/enquiryatices/airIgmEntry"
    response = session.get(form_url)
    response.raise_for_status()
    
    # Get the captcha image
    captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
    captcha_response = session.get(captcha_url)
    captcha_response.raise_for_status()
    
    # Ensure the 'images' directory exists
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Save the captcha image
    image_path = f"images/captcha_{random.random()}.png"
    with open(image_path, 'wb') as f:
        f.write(captcha_response.content)
    print(f"Captcha image saved at: {image_path}")
    
    # Prompt user to enter the captcha text
    captcha_text = input('Enter the Captcha: ')
    
    # Form data
    data = {
        "IGM_loc_Name": "BANGALORE ACC (INBLR4)",
        "MAWB_NO": "17673198753",
        "captchaResp": captcha_text
    }
    
    # Submit the form
    response = session.post(form_url, data=data)
    response.raise_for_status()
    
    # Parse and print the response
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.title.string)
    
except requests.exceptions.RequestException as req_err:
    print('Request Error:', req_err)
except Exception as err:
    print('ERROR:', err)
