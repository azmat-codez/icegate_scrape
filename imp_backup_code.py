from PIL import Image, ImageEnhance
import pytesseract
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


captcha_image = r"images\full_0.3075625343036391.png"
print(captcha_image)
# captcha_image = "images\full_0.48989169857093195.png"


captcha_image = Image.open(captcha_image)


# captcha_image = captcha_image.convert("L")
# threshold = 40
# captcha_image = captcha_image.point(lambda p: p < threshold and 255)
# enhancer = ImageEnhance.Sharpness(captcha_image)
# captcha_image = enhancer.enhance(2.5)

captcha_image = captcha_image.resize((captcha_image.width * 2, captcha_image.height * 2))

image_path = f"img/captcha_{random.random()}.png"
captcha_image.save(image_path)
print(f"Processed image saved at: {image_path}")

captcha_text = pytesseract.image_to_string(captcha_image).strip()
print(captcha_text)

# ----------------------------------------------------------------------------------
