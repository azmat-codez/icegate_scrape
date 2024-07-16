import requests
from PIL import Image
from io import BytesIO
import pytesseract
from bs4 import BeautifulSoup

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# Step 1: Get CAPTCHA image and decode it
captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
session = requests.Session()
captcha_response = session.get(captcha_url)
captcha_image = Image.open(BytesIO(captcha_response.content))

# Use Tesseract to decode the CAPTCHA
captcha_text = pytesseract.image_to_string(captcha_image).strip()

print(captcha_text)
exit()







# Step 2: Submit form with decoded CAPTCHA
url = "https://enquiry.icegate.gov.in/enquiryatices/airIgmEntry"
data = {
    "IGM_loc_Name": "BANGALORE+ACC+(INBLR4)",
    "MAWB_NO": "17673198753",
    "captchaResp": captcha_text
}

# response = session.post(url, data=data)

# # Step 3: Check the response
# if response.status_code == 200:
#     print("Form submitted successfully!")
#     # Process the response as needed
# else:
#     print("Failed to submit the form.")



response = requests.post(url, data=data)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    print(soup.title.string)

    result = soup.find(id='resultId')
    print(result)
else:
    print("Failed to retrieve the page")
