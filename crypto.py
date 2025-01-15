import cv2
import hashlib
import os
import requests
import argparse
import mysql.connector
from mysql.connector import errorcode
from PIL import Image, ImageFilter
import sys

if len(sys.argv) == 1:
    sys.argv.append('-h')

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

def redimensionner_image(filepath, dimensions):
    try:
        with Image.open(filepath) as img:
            largeur, hauteur = map(int, dimensions.split('x'))
            img = img.resize((largeur, hauteur))
            img.save(filepath)
            print(f"Image redimensionnée à {dimensions}.")
    except IOError as e:
        print(f"Erreur lors du redimensionnement de l'image : {e}")

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

def generateur_aleatoire_image(filepath, longueur, output_format):
    if not isinstance(longueur, int) or longueur <= 0:
        return "Erreur : La longueur doit être un entier positif."

    pixels = collecte_pixel_image(filepath)
    if pixels is None:
        return "Erreur : Impossible de lire le fichier."

    hash_result = hash_pixels(pixels)
    random_sequence = int.from_bytes(hash_result, byteorder='big')
    
    if output_format == "hex":
        return hex(random_sequence)[:longueur]
    elif output_format == "bin":
        return bin(random_sequence)[:longueur]
    else:
        return str(random_sequence)[:longueur]

def enregistrer_dans_fichier(contenu, export_path, format_export):
    try:
        with open(export_path, 'w') as file:
            if format_export == "json":
                import json
                json.dump({"nombre_aleatoire": contenu}, file)
            elif format_export == "csv":
                import csv
                writer = csv.writer(file)
                writer.writerow(["nombre_aleatoire"])
                writer.writerow([contenu])
            else:
                file.write(contenu)
        print(f"Nombre aléatoire exporté dans : {export_path}")
    except IOError as e:
        print(f"Erreur d'E/S lors de l'enregistrement du fichier : {e}")

def enregistrer_dans_bd(contenu, host, user, password, database):
    try:
        conn_params = {
            'host': host,
            'user': user,
            'database': database
        }
        if password:
            conn_params['password'] = password

        conn = mysql.connector.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS nombres_aleatoires
                          (id INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(255))''')
        cursor.execute('INSERT INTO nombres_aleatoires (nombre) VALUES (%s)', (contenu,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Nombre aléatoire sauvegardé dans la base de données MySQL.")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Erreur : Identifiant ou mot de passe incorrect.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Erreur : La base de données n'existe pas.")
        else:
            print(err)

def main():
    parser = argparse.ArgumentParser(description='Générateur de nombre aléatoire à partir d\'une image.')

    parser.add_argument('-url', type=str, help='URL de l\'image à télécharger.')
    parser.add_argument('-path', type=str, help='Chemin pour sauvegarder l\'image téléchargée ou capturée.')
    parser.add_argument('-capture', action='store_true', help='Capturer une image à partir de la caméra.')
    parser.add_argument('-len', type=int, help='Longueur du nombre aléatoire à générer.')
    parser.add_argument('-export', type=str, help='Chemin pour exporter le nombre généré dans un fichier.')
    parser.add_argument('-db', action='store_true', help='Indique si le nombre doit être sauvegardé dans la base de données MySQL.')
    parser.add_argument('-host', type=str, help='Hôte de la base de données MySQL.')
    parser.add_argument('-user', type=str, help='Utilisateur de la base de données MySQL.')
    parser.add_argument('-password', type=str, default='', help='Mot de passe de la base de données MySQL (laisser vide si non requis).')
    parser.add_argument('-database', type=str, help='Nom de la base de données MySQL.')
    parser.add_argument('-timeout', type=int, default=10, help='Délai d\'attente maximal en secondes pour le téléchargement de l\'image.')
    parser.add_argument('-format', type=str, choices=['hex', 'bin', 'dec'], default='dec', help='Format du nombre aléatoire généré (hex, bin, dec).')
    parser.add_argument('-log', type=str, help='Chemin du fichier de journalisation.')
    parser.add_argument('-filter', type=str, help='Filtre à appliquer à l\'image (BLUR, CONTOUR, etc.).')
    parser.add_argument('-resize', type=str, help='Dimensions de redimensionnement de l\'image (e.g., 100x100).')
    parser.add_argument('-format-export', type=str, choices=['txt', 'json', 'csv'], default='txt', help='Format du fichier d\'exportation.')
    parser.add_argument('-verbose', action='store_true', help='Activer le mode verbeux pour les messages de sortie.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.5')

    args = parser.parse_args()

    if args.log:
        import logging
        logging.basicConfig(filename=args.log, level=logging.INFO)
        logging.info('Début du traitement')

    if args.capture:
        if args.path:
            if not capturer_image_camera(args.path):
                return  
        else:
            print("Erreur : Veuillez spécifier un chemin pour sauvegarder l'image capturée.")
            return

    if args.url:
        if args.path:
            telecharger_image(args.url, args.path, args.timeout)
        else:
            print("Erreur : Veuillez spécifier un chemin pour sauvegarder l'image téléchargée.")
            return
    elif args.path and os.path.isfile(args.path):
        print(f"Utilisation de l'image locale : {args.path}")
    else:
        print("Erreur : Aucun chemin d'image valide fourni.")
        return

    if args.filter:
        appliquer_filtre_image(args.path, args.filter)
    
    if args.resize:
        redimensionner_image(args.path, args.resize)

    if args.len:
        nombre_aleatoire = generateur_aleatoire_image(args.path, args.len, args.format)
    
        if args.export:
            enregistrer_dans_fichier(nombre_aleatoire, args.export, args.format_export)
        if args.db:
            enregistrer_dans_bd(nombre_aleatoire, args.host, args.user, args.password, args.database)
        if not args.export and not args.db:
            print(f"Nombre aléatoire généré : {nombre_aleatoire}")
    else:
        print("Erreur : Vous devez spécifier la longueur du nombre aléatoire avec -len.")
    
    if args.log:
        logging.info('Fin du traitement')
    
    if args.verbose:
        print("Traitement terminé avec succès.")

if __name__ == "__main__":
    main()