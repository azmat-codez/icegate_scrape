from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import pytesseract
import requests
from bs4 import BeautifulSoup
import easyocr
import cv2
import time
import numpy as np
import random



location = 'BANGALORE ACC (INBLR4)'
mawb_no = "61597695990"

def get_captcha_text(captcha_image, angle):

    captcha_image = captcha_image.convert("L")
    threshold = 40
    captcha_image = captcha_image.point(lambda p: p < threshold and 255)
    
    enhancer = ImageEnhance.Sharpness(captcha_image)
    captcha_image = enhancer.enhance(3)
    enhancer = ImageEnhance.Contrast(captcha_image)
    captcha_image = enhancer.enhance(3)
    
    captcha_image = captcha_image.resize((captcha_image.width * 2, captcha_image.height * 2))
    captcha_image_with_padding = ImageOps.expand(captcha_image, border=30, fill='white')
    captcha_image_rotated = captcha_image_with_padding.rotate(angle, expand=True, fillcolor='white')
    
    image_array = np.array(captcha_image_rotated)
    image = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)
    
    reader = easyocr.Reader(['en'])
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray_image)
    captcha_text = ''.join([result[1] for result in results])
    
    image_path = f"images/captcha_{random.random()}.png"
    captcha_image_rotated.save(image_path)
    print(f"Processed image saved at: {image_path}")
    
    return captcha_text


def get_response(session, captcha_text):
    captcha_text = captcha_text.replace(' ', '')
    data = {
        "IGM_loc_Name": location,
        "MAWB_NO": mawb_no,
        "captchaResp": captcha_text
    }

    submit_url = "https://enquiry.icegate.gov.in/enquiryatices/igmICES_action"
    response = session.post(submit_url, data=data)
    
    if response.status_code == 200:
        result_soup = BeautifulSoup(response.content, 'html.parser')
        return result_soup
    return None

def main():
    try:
        session = requests.Session()
        form_url = "https://enquiry.icegate.gov.in/enquiryatices/airIgmEntry"
        response = session.get(form_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        captcha_url = "https://enquiry.icegate.gov.in/enquiryatices/CaptchaImg.jpg"
        captcha_response = session.get(captcha_url)
        captcha_image = Image.open(BytesIO(captcha_response.content))

        angles = [0, -10, -17]
        final_response = None

        start_time = time.time()
        session_duration = 5 * 60

        for angle in angles:
            captcha_text = get_captcha_text(captcha_image, angle)
            
            if len(captcha_text) != 6 or not captcha_text.isalnum():
                continue
            retries = [(captcha_text, captcha_text)]
            
            # --------------------Do Text Maniplutation --------------------
            if '1' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('1', 'l')))
                retries.append((captcha_text, captcha_text.replace('1', 'I')))
            if 'l' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('l', '1')))
            
            for original, modified in retries:
                if time.time() - start_time > session_duration:
                    print("Session timed out.")
                    break
                captcha_text = modified
                print(f"Trying captcha text: {captcha_text} (original: {original})")
                
                response_soup = get_response(session, captcha_text)
                
                if response_soup and 'Invalid Code! Please try again!' not in response_soup.text:
                    final_response = response_soup
                    tbody = final_response.find('tbody')
                    if tbody:
                        td_elements = tbody.find_all('td')
                        if len(td_elements) >= 6:
                            data = {
                                'awb_number': td_elements[1].get_text(strip=True),
                                'port_shipment': td_elements[2].get_text(strip=True),
                                'port_destination': td_elements[3].get_text(strip=True),
                                'pkgs': td_elements[4].get_text(strip=True),
                                'gross_weight': td_elements[5].get_text(strip=True)
                            }
                            return data
                            break
                    break

    except Exception as err:
        print('ERROR:', err)


if __name__ == "__main__":
    main()
