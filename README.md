# Entropie_python By YEBGA MIYOGOG Brayan

Générateur de nombres aléatoires grâce à l'entropie

Il utilise des images, soit capturées par une caméra, soit téléchargées depuis une URL. Il offre plusieurs fonctionnalités, comme l'application de filtres d'image, le redimensionnement, et l'exportation des résultats vers un fichier ou une base de données MySQL. Voici un résumé des principales fonctions et de leur rôle :

               Fonctionnalités Principales

Capture d'Image :

Utilise la caméra pour capturer une image et la sauvegarder à un emplacement spécifié.

Téléchargement d'Image :

Télécharge une image depuis une URL et la sauvegarde localement.

Application de Filtres :

Applique des filtres d'image (comme flou ou contour) à l'image sauvegardée.

Redimensionnement d'Image :

Redimensionne l'image à des dimensions spécifiées.

Collecte des Pixels :

Récupère les données de pixels de l'image et les utilise pour générer un nombre aléatoire.

Génération de Nombres Aléatoires :

Génère un nombre aléatoire à partir des pixels de l'image en utilisant un hachage.

Exportation des Résultats :

Exportation des résultats vers un fichier (formats : texte, JSON, CSV) ou sauvegarde dans une base de données MySQL.

Journalisation :

Enregistre les messages et les erreurs dans un fichier de journalisation si spécifié.
            
            Comment Utiliser le Script ?

Vous pouvez exécuter le script en ligne de commande avec divers arguments :

-url: URL de l'image à télécharger.
-path: chemin pour sauvegarder l'image.
-capture: option pour capturer une image à partir de la caméra.
-len: longueur du nombre aléatoire à générer.
-export: chemin pour exporter le nombre aléatoire.
-db: indique si le nombre doit être sauvegardé dans la base de données MySQL.
-host, -user, -password, -database: informations de connexion à la base de données MySQL.
-timeout: délai d'attente pour le téléchargement de l'image.
-format: format du nombre aléatoire généré (hex, bin, dec).
-filter: filtre à appliquer à l'image (BLUR, CONTOUR, etc.).
-resize: dimensions pour redimensionner l'image.
-format-export: format du fichier d'exportation (txt, json, csv).
-verbose: active le mode verbeux pour les messages de sortie.
                        Exemple d'Exécution

python votre_script.py -url http://example.com/image.jpg -path image.jpg -len 10 -export resultat.txt -db -host localhost -user root -password votre_mot_de_passe -database votre_db

                    Points à Vérifier

Assurez-vous que toutes les bibliothèques nécessaires sont installées (opencv-python, Pillow, requests, mysql-connector-python).

Vérifiez que votre caméra est accessible si vous utilisez la fonction de capture d'image.

Assurez-vous que les informations de connexion à la base de données MySQL sont correctes.