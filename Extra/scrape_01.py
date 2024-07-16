import requests
from bs4 import BeautifulSoup

import requests
from PIL import Image
from io import BytesIO
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# Step 1: Get CAPTCHA image and decode it
captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
session = requests.Session()
captcha_response = session.get(captcha_url)
captcha_image = Image.open(BytesIO(captcha_response.content))

# Use Tesseract to decode the CAPTCHA
captcha_text = pytesseract.image_to_string(captcha_image).strip()


# url = "https://enquiry.icegate.gov.in/enquiryatices/igmICES_action"
url = "https://enquiry.icegate.gov.in/enquiryatices/airIgmEntry"

data = {
    "IGM_loc_Name": "BANGALORE+ACC+(INBLR4)",
    "MAWB_NO": "17673198753",
    "captchaResp": {captcha_text}  
}

response = requests.post(url, data=data)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(soup.title.string)

    result = soup.find(id='resultId')
    print(result)
else:
    print("Failed to retrieve the page")







import requests

def solve_captcha(api_key, site_url, site_key):
    # Request to solve CAPTCHA
    captcha_id = requests.post(
        "http://2captcha.com/in.php",
        data={"key": api_key, "method": "userrecaptcha", "googlekey": site_key, "pageurl": site_url}
    ).text.split('|')[1]
    
    # Poll for the CAPTCHA solution
    while True:
        resp = requests.get(f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}").text
        if resp == 'CAPCHA_NOT_READY':
            continue
        if 'OK|' in resp:
            return resp.split('|')[1]

# Your API key for the CAPTCHA solving service
api_key = "your_2captcha_api_key"
site_url = "https://enquiry.icegate.gov.in/enquiryatices/airIgmEntry"
site_key = "site_key_for_the_captcha"  # You need to find this in the site’s HTML

# Solve the CAPTCHA
captcha_solution = solve_captcha(api_key, site_url, site_key)

# Now use this solution in your original request
data = {
    "IGM_loc_Name": "BANGALORE+ACC+(INBLR4)",
    "MAWB_NO": "17673198753",
    "captchaResp": captcha_solution
}

response = requests.post(url, data=data)
# Handle the response as before
