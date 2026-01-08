# Pré-indexation automatique des premiers lots de numérisations du fonds Nicole et Jean-Michel Thierry

Projet réalisé par Denise Atzori, Thaïs Raffray et Chiara Tedesco dans le cadre d'une semaine de Hackathon organisée par l'École nationale des Chartes - PSL

1. ## Contexte
Le fonds Nicole et Jean-Michel Thierry: env. 100 000 photographies, films et dossiers de documentation et de recherche - 1950-2017.
Un premier volet de numérisations sur le patrimoine arménien et géorgien, destiné à être documenté par une communauté d’experts

2. ## Corpus et données
- 297 lots d’archives structurés en manifestes IIIF et présentant un corpus de 8 196 vues
- Une fraction du corpus de 1 335 vues enrichies manuellement par des mots-clés scientifiques [ modèle de données créé par campagne d’annotation experte participative: https://cloud.inha.fr/s/JmK4z2HAf6TseqB]

3. ## Objectifs
- Classer automatiquement 8196 vues selon:
    - Types de vue
    - Sujets représentés
- Générer des titres longs pour les images

4. ## Stratégie adoptée
- Entraînement d’un modèle supervisé (YOLO nano v11) sur les images annotées par l’équipe de recherche pour le premier niveau d'annotation et benchmarking
- Benchmarking de modèles non-supervisés pour la classification des sujets du deuxième niveau d'annotation (CLIP, EfficientNet, DINO-v2, ViT)
- Inférences sur les images non annotées pour comparer les résultats des modèles
- Création d'un interface graphique avec la librairie Python streamlit pour la validation manuelle des annotations automatiques
- 

5. ## Difficultés rencontrées
- Erreurs dans les annotations manuelles de certaines images (elle ne suit pas toujours les nœuds de l’arborescence) -> solution: correction avec un script
- Pas assez de données annotées pour chaque classe dans le niveau 2 -> solution: clustering pour le tag_2

6. ## Livrés (dans ce dossier)
- ### Code sur forme de notebooks et code py:
    - 1-extraction_annotations.ipynb: scrapping des images avec annotations manuelle et creation CSV
    - 2-training_yolo_tag1.ipynb: pré-processing données et entraînement Yoloy11n-cls pour le premier niveau
    - 3-training_yolo_tag2.ipynb: pré-processing données et entraînement Yoloy11n-cls pour le deuxième niveau
    - 4-inference_yolo.ipynb: inferénce avec Yolo et production du csv
    - 5-merge_inference_images_csv.ipynb: script pour ajouter les inférences de Yolo sur le csv
    - 6-clustering_dino.ipynb: inferénce et clustering (non-supervisé) avec Dinov2 pour le deuxième niveau
    - 7-clustering_efficentnet.ipynb: inferénce et clustering (non-supervisé) avec EfficientNetv7 pour le deuxième niveau
    - 8-fusioner_clustering_images.ipynb: script pour fusioner les resultats du clustering (tag_2) dans le CSV des images
    - 9-interface_validation.py: app streamlit pour la validation manuelle des annotations (à lancer avec les instruction dans instruction_streamlit.txt)
- ### Modèles:
    - Dossier Yolo best-unbalaced: poids du modèle, result.csv et confusion_matrix d'un modèle Yoloy11n-cls entraîné avec un dataset déséquilibré sur les photographies (tag_1)
    - Dossier Yolo best-balaced: poids du modèle, result.csv et confusion_matrix d'un modèle Yoloy11n-cls entraîné avec un dataset équilibré sur toutes les classes (tag_1)
- ### Dossier Documentation:
    - images_test_inference: dossier avec une centaines des images pour tester l'inference du tag_1
    - images_inference.csv: resultat de l'inference de Yolo (balanced)
    - images_test_clustering: dossier avec une centaines des photo de test pour le clustering du tag_2
    - clustering_results(dino/eff).csv: resultats du clustering de Dino et EfficentNet
    - instruction_streamlit.txt: informations pour lancer streamlit
    - exemple_annotation_automatique.csv: fichier csv avec tous les résultats des annotations automatiques prêts pour validation dans l'app streamlit


