import requests
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from io import BytesIO
import pytesseract
import random

# Set tesseract command path
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Create a session and fetch the captcha image
session = requests.Session()
captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
captcha_response = session.get(captcha_url)
captcha_image = Image.open(BytesIO(captcha_response.content))
# captcha_image = "img\full_0.510743332866213.png"

# Convert the image to grayscale (black and white)
captcha_image = captcha_image.convert("L")

# Apply threshold to get a binary image
threshold = 40
captcha_image = captcha_image.point(lambda p: p < threshold and 255)

# Save the image for cv2 processing
captcha_image.save("captcha_image.png")

# Read the image using cv2
image = cv2.imread("captcha_image.png", cv2.IMREAD_GRAYSCALE)

# Detect the skew angle of the text
coords = np.column_stack(np.where(image > 0))
angle = cv2.minAreaRect(coords)[-1]

# Correct the angle
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle

(h, w) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# Enhance the rotated image
rotated_pil = Image.fromarray(rotated)
enhancer = ImageEnhance.Sharpness(rotated_pil)
rotated_pil = enhancer.enhance(2.0)  # Increase sharpness by a factor of 2

# Save and display the rotated image path
image_path = f"images/rotated_{random.random()}.png"
print(image_path)
rotated_pil.save(image_path)

# Perform OCR on the enhanced and rotated image
captcha_text = pytesseract.image_to_string(rotated_pil).strip()

print(captcha_text)
