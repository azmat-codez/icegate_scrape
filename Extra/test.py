import time

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
    
    if '1' in captcha_text:
        retries.append((captcha_text, captcha_text.replace('1', 'l')))
        retries.append((captcha_text, captcha_text.replace('1', 'I')))
    if 'l' in captcha_text:
        retries.append((captcha_text, captcha_text.replace('l', '1')))
    if 'I' in captcha_text:
        retries.append((captcha_text, captcha_text.replace('I', '1')))

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

if final_response:
    with open("parse_page.html", "w", encoding='utf-8') as f:
        f.write(final_response.prettify())
    print("Page saved successfully.")
else:
    print("Failed to retrieve valid data after multiple attempts.")
