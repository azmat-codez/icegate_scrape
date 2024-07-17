from PIL import Image, ImageEnhance, ImageOps
from io import BytesIO
import pytesseract
import requests
from bs4 import BeautifulSoup
import random

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\A100156\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def get_captcha_text(captcha_image, angle):
    captcha_image = captcha_image.convert("L")
    threshold = 40
    captcha_image = captcha_image.point(lambda p: p < threshold and 255)
    
    enhancer = ImageEnhance.Sharpness(captcha_image)
    captcha_image = enhancer.enhance(2.5)
    
    captcha_image = captcha_image.resize((captcha_image.width * 2, captcha_image.height * 2))
    captcha_image_with_padding = ImageOps.expand(captcha_image, border=30, fill='white')
    
    captcha_image_rotated = captcha_image_with_padding.rotate(angle, expand=True, fillcolor='white')
    
    # image_path = f"ZAll Captcha Image/captcha_{random.random()}.png"
    # captcha_image_rotated.save(image_path)
    # print(f"Processed image saved at: {image_path}")
    
    captcha_text = pytesseract.image_to_string(captcha_image_rotated).strip()
    return captcha_text

def get_response(session, captcha_text):
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

        angles = [0, -10, -13, -16, -18]
        final_response = None
        
        for angle in angles:
            captcha_text = get_captcha_text(captcha_image, angle)
            print(f"Captcha text for angle {angle}: {captcha_text}")
            response_soup = get_response(session, captcha_text)

            if response_soup and 'Invalid Code! Please try again!' not in response_soup.text:
                final_response = response_soup
                tbody = final_response.find('tbody')
                if tbody:
                    td_elements = tbody.find_all('td')
                    if len(td_elements) >= 6:
                        data = {}
                        data['awb_number'] = td_elements[1].get_text(strip=True)
                        data['port_shipment'] = td_elements[2].get_text(strip=True)
                        data['port_destination'] = td_elements[3].get_text(strip=True)
                        data['pkgs'] = td_elements[4].get_text(strip=True)
                        data['gross_weight'] = td_elements[5].get_text(strip=True)
                        print(data)
                break

        # if final_response:
        #     with open("parse_page.html", "w", encoding='utf-8') as f:
        #         f.write(final_response.prettify())
        #     print("Page saved successfully.")
        # else:
        #     print("Failed to retrieve valid data after multiple attempts.")
    except Exception as err:
        print('ERROR:', err)

if __name__ == "__main__":
    main()
