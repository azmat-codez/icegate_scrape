import easyocr
import cv2
import matplotlib.pyplot as plt
import numpy as np


try:
    image_path = r'img\captcha_0.14884159552467469.png'
    reader = easyocr.Reader(['en'])
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = reader.readtext(gray_image)
    captcha_text = ''.join([result[1] for result in results])
except Exception as err:
    print('ERROR: ', err)
    
    
    