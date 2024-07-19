from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import pytesseract
import requests
from bs4 import BeautifulSoup
import random
import time


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

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
    
    image_path = f"images/captcha_{random.random()}.png"
    captcha_image_rotated.save(image_path)
    print(f"Processed image saved at: {image_path}")
    
    captcha_text = pytesseract.image_to_string(captcha_image_rotated).strip()
    return captcha_text

def get_response(session, captcha_text):
    captcha_text = captcha_text.replace(' ', '')
    data = {
        "IGM_loc_Name": "BANGALORE ACC (INBLR4)",
        "MAWB_NO": "61597695990",
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

# ---------------------------------------------------------

        angles = [0, -10, -13, -16, -18]
        final_response = None

        start_time = time.time()
        session_duration = 5 * 60  # 5 minutes in seconds

        for angle in angles:
            captcha_text = get_captcha_text(captcha_image, angle)
            
            # Robust checks and retries
            if len(captcha_text) != 6 or not captcha_text.isalnum():
                continue

            retries = [(captcha_text, captcha_text)]  # List of tuples (original, modified)
            print(retries)
            
            if '1' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('1', 'l')))
                retries.append((captcha_text, captcha_text.replace('1', 'I')))
            if 'l' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('l', '1')))
            if 'I' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('I', '1')))
                retries.append((captcha_text, captcha_text.replace('I', '9')))
            if 'a' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('a', 'd')))
            if 'f' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('f', 'J')))
            if 'J' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('J', 'j')))
            if 'j' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('j', 'J')))
            if 'O' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('O', 'o')))
                retries.append((captcha_text, captcha_text.replace('O', '0')))
            if '0' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('0', 'o')))
                retries.append((captcha_text, captcha_text.replace('0', 'O')))
            if 'o' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('o', 'O')))
                retries.append((captcha_text, captcha_text.replace('o', '0')))
            if 'S' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('S', 's')))
                retries.append((captcha_text, captcha_text.replace('S', '5')))
                retries.append((captcha_text, captcha_text.replace('S', '2')))
            if '5' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('5', 'S')))
                retries.append((captcha_text, captcha_text.replace('5', 's')))
            if '2' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('2', 'S')))
                retries.append((captcha_text, captcha_text.replace('2', 's')))
            if 'X' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('X', 'x')))
            if 'x' in captcha_text:
                retries.append((captcha_text, captcha_text.replace('x', 'X')))
            

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
                            print(data)
                            break
                    break

        if final_response:
            with open("parse_page.html", "w", encoding='utf-8') as f:
                f.write(final_response.prettify())
            print("Page saved successfully.")
        else:
            print("Failed to retrieve valid data after multiple attempts.")

    except Exception as err:
        print('ERROR:', err)


if __name__ == "__main__":
    main()
