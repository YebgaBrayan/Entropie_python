import cv2
import hashlib
import requests
from PIL import Image, ImageFilter
import argparse

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

def appliquer_filtre_image(filepath, filtre):
    try:
        with Image.open(filepath) as img:
            if filtre == "BLUR":
                img = img.filter(ImageFilter.BLUR)
            elif filtre == "CONTOUR":
                img = img.filter(ImageFilter.CONTOUR)
            img.save(filepath)
            print(f"Filtre {filtre} appliqué à l'image.")
    except IOError as e:
        print(f"Erreur lors de l'application du filtre à l'image : {e}")

def collecte_pixel_image(filepath):
    try:
        with Image.open(filepath) as img:
            return list(img.getdata())
    except (FileNotFoundError, IOError) as e:
        print(f"Erreur lors de la collecte des pixels : {e}")
        return None

def generateur_aleatoire_image(filepath, longueur, output_format):
    pixels = collecte_pixel_image(filepath)
    if pixels is None:
        return "Erreur : Impossible de lire le fichier."
    hash_result = hashlib.sha512(bytearray(p for pixel in pixels for p in (pixel if isinstance(pixel, tuple) else [pixel]))).digest()
    random_sequence = int.from_bytes(hash_result, byteorder='big')
    if output_format == "hex":
        return hex(random_sequence)[:longueur]
    elif output_format == "bin":
        return bin(random_sequence)[:longueur]
    else:
        return str(random_sequence)[:longueur]

def main():
    parser = argparse.ArgumentParser(description='Générateur de nombre aléatoire à partir d\'une image.')
    parser.add_argument('-url', type=str, help='URL de l\'image à télécharger.')
    parser.add_argument('-path', type=str, help='Chemin pour sauvegarder l\'image.')
    parser.add_argument('-capture', action='store_true', help='Capturer une image à partir de la caméra.')
    parser.add_argument('-len', type=int, help='Longueur du nombre aléatoire à générer.')
    parser.add_argument('-filter', type=str, help='Filtre à appliquer à l\'image (BLUR, CONTOUR, etc.).')
    parser.add_argument('-format', type=str, choices=['hex', 'bin', 'dec'], default='dec', help='Format du nombre aléatoire généré (hex, bin, dec).')

    args = parser.parse_args()

    if args.capture and args.path:
        if not capturer_image_camera(args.path):
            return
    elif args.url and args.path:
        if not telecharger_image(args.url, args.path, 10):
            return
    elif args.path:
        print(f"Utilisation de l'image locale : {args.path}")
    else:
        print("Erreur : Aucun chemin d'image valide fourni.")
        return

    if args.filter:
        appliquer_filtre_image(args.path, args.filter)

    if args.len:
        nombre_aleatoire = generateur_aleatoire_image(args.path, args.len, args.format)
        print(f"Nombre aléatoire généré : {nombre_aleatoire}")
    else:
        print("Erreur : Vous devez spécifier la longueur du nombre aléatoire avec -len.")

if __name__ == "__main__":
    main()
