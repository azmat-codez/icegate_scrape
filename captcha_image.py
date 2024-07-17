from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import random


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def get_captcha_text(image_path, angle):
    
    captcha_image = Image.open(image_path)
    
    captcha_image = captcha_image.resize((captcha_image.width * 2, captcha_image.height * 2))
    captcha_image_with_padding = ImageOps.expand(captcha_image, border=30, fill='white')
    captcha_image_rotated = captcha_image_with_padding.rotate(angle, expand=True, fillcolor='white')
    
    image_path = f"img/captcha_{random.random()}.png"
    captcha_image_rotated.save(image_path)
    print(f"Processed image saved at: {image_path}")
    
    captcha_text = pytesseract.image_to_string(captcha_image_rotated).strip()
    return captcha_text




if __name__ == "__main__":
    
    image_path = r"ZAll Captcha Image/captcha_0.5884668225004858.png"
    angles = [0,  -10,  -13,  -16, -18]
    extracted_text = ""
    for angle in angles:
        extracted_text = get_captcha_text(image_path, angle)
        print(f"Extracted text at {angle} degrees: {extracted_text}")
    #     if len(extracted_text) == 6 and extracted_text.isalnum():
    #         break
    # print(f"Final extracted text: {extracted_text}")
