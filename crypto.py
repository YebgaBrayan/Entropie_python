import cv2
import hashlib
import os
import requests
import argparse
import mysql.connector
from mysql.connector import errorcode
from PIL import Image, ImageFilter
import sys

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