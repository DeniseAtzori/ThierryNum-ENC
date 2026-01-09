# Que fait cette application ?

L'application **IAnahid** permet de valider manuellement les annotations générées automatiquement par un modèle supervisé (ici YOLO pour les tag_1), de choisir une classe pour les clusters générés par un modèle non-supervisé (ici Dino/EfficientNet pour les tag_2), et de générer des descriptions automatiques pour les images via trois modèles de Mistral (une clé API est nécessaire).

Une fois l'application lancée, vous pouvez choisir le niveau d'annotation à valider o l'option "légende" depuis la barre de configuration située à gauche. Les images sont affichées selon l'ordre du fichier CSV de référence et il est possible de les faire défiler même sans validation. Les modifications sont enregistrées automatiquement dans le fichier CSV.

L'application sauvegarde l'état au moment de la fermeture et affiche la première photo non validée lors de la session suivante.
Un aperçu des lignes du dataframe est disponible en bas pendant la validation.

# Comment lancer l'app IAnahid ?

1. Installez Streamlit dans votre environnement : `pip install streamlit pandas`.
2. Changez le path du votre fichier "annotations.csv" dans le script de l'appli (CSV_PATH). Assurez-vous que les colonnes de votre fichier correspondent à l'exemple fourni sur GitHub (exemple.csv) et que tous les liens aux images soient actifs et fonctionnels.
3. Lancez l'app sur le terminal : `streamlit 9-interface_validation.py`.