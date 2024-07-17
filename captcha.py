import requests
from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import pytesseract
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


# !---------------------------- DIRECT IMAGE ------------------------------
# captcha_image = ""
# captcha_text = pytesseract.image_to_string(captcha_image).strip()
# print(captcha_text)
# exit()
# !---------------------------- DIRECT IMAGE ------------------------------


session = requests.Session()
captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
captcha_response = session.get(captcha_url)
captcha_image = Image.open(BytesIO(captcha_response.content))

# captcha_image = ""

captcha_image = captcha_image.convert("L")
threshold = 40
captcha_image = captcha_image.point(lambda p: p < threshold and 255)
enhancer = ImageEnhance.Sharpness(captcha_image)
captcha_image = enhancer.enhance(2.5)

captcha_image = captcha_image.resize((captcha_image.width * 2, captcha_image.height * 2))

image_path = f"images/full_{random.random()}.png"
captcha_image.save(image_path)
print(image_path)

captcha_text = pytesseract.image_to_string(captcha_image).strip()
print(captcha_text)

