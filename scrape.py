import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance
from io import BytesIO
import pytesseract
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

try:
    session = requests.Session()
    form_url = "https://enquiry.icegate.gov.in/enquiryatices/airIgmEntry"
    response = session.get(form_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # !--------------------------- CAPTCHA CODE START ---------------------------
    captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
    captcha_response = session.get(captcha_url)
    captcha_image = Image.open(BytesIO(captcha_response.content))


    captcha_image = captcha_image.convert("L")
    threshold = 40
    captcha_image = captcha_image.point(lambda p: p < threshold and 255)
    enhancer = ImageEnhance.Sharpness(captcha_image)
    captcha_image = enhancer.enhance(2.5)


    image_path = f"images/full_{random.random()}.png"
    print(image_path)
    captcha_image.save(image_path)

    captcha_text = pytesseract.image_to_string(captcha_image).strip()
    print(captcha_text)
    # !--------------------------- CAPTCHA CODE END ---------------------------
except Exception as err:
    print('ERROR I :', err)


try:
    data = {
        "IGM_loc_Name": "BANGALORE ACC (INBLR4)",
        # "MAWB_NO": "17673198753",
        # "MAWB_NO": "40694738630",
        "MAWB_NO": "61597695990",
        "captchaResp": captcha_text
    }

    submit_url = "https://enquiry.icegate.gov.in/enquiryatices/igmICES_action"
    response = session.post(submit_url, data=data)

    if response.status_code == 200:
        # print("Form submitted successfully!")
        result_soup = BeautifulSoup(response.content, 'html.parser')
        html_text = result_soup.prettify()
        
        f = open("parse_page.html", "w")
        f.write(html_text)
        f.close()
    else:
        print("Failed to submit the form. Status code:", response.status_code)
except Exception as err:
    print('ERROR II :', err)
