import requests
from PIL import Image, ImageOps, ImageEnhance
from io import BytesIO
import pytesseract
import os

#def resize_image_with_white_background(original_image, target_size):
    #new_image = Image.new("RGB", target_size, "white")
    #position = ((target_size[0] - original_image.width) // 2, (target_size[1] - original_image.height) // 2)
    #new_image.paste(original_image, position)
    
    #return new_image

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'


for i in range(10):
    captcha_url = "https://old.icegate.gov.in/iceLogin/CaptchaImg.jpg"
    response = requests.get(captcha_url)
    print(response)
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data)) 
        image = image.convert('L')
        image = ImageOps.invert(image)
        enhancer = ImageEnhance.Contrast(image)
        factor = 3.0  # Adjust this factor as needed (1.0 means no change)
        image = enhancer.enhance(factor)
        #target_size = (600, 200)
        #image=resize_image_with_white_background(image,target_size)
        captcha_text = pytesseract.image_to_string(image)
        
        
        
        logs_folder = r'image'
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)
        log_file_path = os.path.join(logs_folder, 'captcha_log.txt')
        with open(log_file_path, "a") as file:
            file.write(captcha_text+"\n")  
            captcha_image_path = os.path.join(logs_folder, f"captcha_{i}.png")   
            image.save(captcha_image_path)    
            print(f"CAPTCHA {i} text and image saved successfully.")
        print(captcha_text)
            
            
