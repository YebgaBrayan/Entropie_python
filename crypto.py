import cv2
import hashlib
import os
import requests
import argparse
import mysql.connector
from mysql.connector import errorcode
from PIL import Image, ImageFilter
import sys

def capturer_image_camera(filepath):
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        print("Erreur : Impossible d'accéder à la caméra.")
        return False

    ret, frame = cap.read()  
    if ret:
        cv2.imwrite(filepath, frame)  
        print(f"Image capturée et sauvegardée sous : {filepath}")
        cap.release() 
        return True
    else:
        print("Erreur : Impossible de capturer l'image.")
        cap.release()  
        return False
    
def telecharger_image(url, filepath, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        with open(filepath, 'wb') as image_file:
            image_file.write(response.content)
        print(f"Image téléchargée et sauvegardée sous : {filepath}")
        return filepath
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")
        return None
def collecte_pixel_image(filepath):
    try:
        with Image.open(filepath) as img:
            pixels = list(img.getdata())
        return pixels
    except (FileNotFoundError, IOError) as e:
        print(f"Erreur lors de la collecte des pixels : {e}")
        return None

def hash_pixels(pixels):
    m = hashlib.sha512()
    pixel_bytes = bytearray()
    for pixel in pixels:
        pixel_bytes.extend(pixel if isinstance(pixel, (list, tuple)) else [pixel])
    m.update(pixel_bytes)
    return m.digest()

if __name__ == "__main__":
    main()