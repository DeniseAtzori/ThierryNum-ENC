<p align="center">
  <img src="https://www.chartes.psl.eu/themes/custom/arc_enc/logo.svg" height="100" alt="Logo ENC" style="margin-right:20px;" />
  <img src="https://www.chartes.psl.eu/sites/default/files/public/styles/default_medium/public/media/image/2024-04/2021_inha_20_ans_version_simple_rvb_144x463.png?itok=LNZuSrlh" height="100" alt="Logo INHA" style="margin-right:20px;" />
  <img src="https://www.chartes.psl.eu/sites/default/files/public/styles/default_medium/public/media/image/2026-01/dim-pamir.png?itok=uex4GUSy" height="100" alt="Logo PAMIR" />
</p>

# Table of Contents / Indice
* [Français (Original)](#français)
* [English Translation](#english)
* [Traduzione Italiana](#italiano)

---

<a name="français"></a>

# Pré-indexation automatique des premiers lots de numérisations du fonds Nicole et Jean-Michel Thierry de l'INHA: Institut national d'histoire de l'art

Projet réalisé par **Denise Atzori**, **Thaïs Raffray** et **Chiara Tedesco** dans le cadre d'une semaine de Hackathon organisée par l'École nationale des Chartes - PSL.

## **Contexte**
Le fonds Nicole et Jean-Michel Thierry: env. 100 000 photographies, films et dossiers de documentation et de recherche - 1950-2017.
Un premier volet de numérisations sur le patrimoine arménien et géorgien, destiné à être documenté par une communauté d’experts.

## **Corpus et données**
- 297 lots d’archives structurés en manifestes IIIF et présentant un corpus de 8196 vues
- Une fraction du corpus de 1 335 vues enrichies manuellement par des mots-clés scientifiques [modèle de données créé par campagne d’annotation experte participative](https://cloud.inha.fr/s/JmK4z2HAf6TseqB)

## **Objectifs**
- Classer automatiquement 8196 vues selon:
    - Types de vue
    - Sujets représentés
- Générer des titres longs pour les images

## **Stratégie adoptée**
- Entraînement d’un modèle supervisé (*YOLO nano v11*) sur les images annotées par l’équipe de recherche pour le premier niveau d'annotation et benchmarking
- Benchmarking de modèles non-supervisés pour la classification des sujets du deuxième niveau d'annotation (*CLIP, EfficientNet, DINO-v2, ViT*)
- Inférences sur les images non annotées pour comparer les résultats des modèles
- Création d'un interface graphique avec la librairie Python streamlit pour la validation manuelle des annotations automatiques
- Benchmarking des modèles pour la génération des descriptions (*Qwen3-Max, ministral-8b-2512, mistral-medium-2508, pixtral-12b-2409*)

## **Difficultés rencontrées**
- Erreurs dans les annotations manuelles de certaines images (elle ne suit pas toujours les nœuds de l’arborescence) -> solution: correction avec un script
- Pas assez de données annotées pour chaque classe dans le niveau 2 -> solution: clustering non-supervisé pour le tag_2

## **Livrés (dans ce dossier)**
- ### **Code sur forme de notebooks et code py:**
    - **1-extraction_annotations.ipynb**: scrapping des images avec annotations manuelle et creation CSV
    - **2-training_yolo_tag1.ipynb**: pré-processing données et entraînement Yoloy11n-cls pour le premier niveau
    - **3-training_yolo_tag2.ipynb**: pré-processing données et entraînement Yoloy11n-cls pour le deuxième niveau
    - **4-inference_yolo.ipynb**: inferénce avec Yolo et production du csv
    - **5-merge_inference_images_csv.ipynb**: script pour ajouter les inférences de Yolo sur le csv
    - **6-clustering_dino.ipynb**: inferénce et clustering (non-supervisé) avec Dinov2 pour le deuxième niveau
    - **7-clustering_efficentnet.ipynb**: inferénce et clustering (non-supervisé) avec EfficientNetv7 pour le deuxième niveau
    - **8-fusioner_clustering_images.ipynb**: script pour fusioner les resultats du clustering (tag_2) dans le CSV des images
    - **9-IAnahid.py**: app streamlit pour la validation manuelle des annotations et la génération des légendes(à lancer avec les instruction dans instruction_streamlit.txt)
- ### **Modèles:**
    - **Dossier Yolo best-unbalaced**: poids du modèle, result.csv et confusion_matrix d'un modèle Yoloy11n-cls entraîné avec un dataset déséquilibré sur les photographies (tag_1)
    - **Dossier Yolo best-balaced**: poids du modèle, result.csv et confusion_matrix d'un modèle Yoloy11n-cls entraîné avec un dataset équilibré sur toutes les classes (tag_1)
- ### **Dossier Documentation:**
    - **Documentation_ThierryNum-ENC.pdf**: compte-rendu du travail pendant l'hackathon
    - **requirements.txt**: liste des requirements à installer pour que le code fonctionne
    - **images_test_inference**: dossier avec une centaines des images pour tester l'inference du tag_1
    - **images_inference.csv**: resultat de l'inference de Yolo (balanced)
    - **images_test_clustering**: dossier avec une centaines des photo de test pour le clustering du tag_2
    - **clustering_results(dino/eff).csv**: resultats du clustering de Dino et EfficentNet
    - **instruction_IAnahid.md**: informations pour lancer streamlit
    - **exemple.csv**: fichier avec un clustering aléatoire pour essayer l'app

---

<a name="english"></a>

# Automatic pre-indexing of the first batches of digitizations from the Nicole and Jean-Michel Thierry collection at INHA: Institut national d'histoire de l'art

Project carried out by **Denise Atzori**, **Thaïs Raffray** and **Chiara Tedesco** as part of a Hackathon week organized by the École nationale des Chartes - PSL

## **Context**
The Nicole and Jean-Michel Thierry collection: approx. 100,000 photographs, films and documentation and research files - 1950-2017.
A first phase of digitizations on Armenian and Georgian heritage, intended to be documented by a community of experts.

## **Corpus and data**
- 297 archival batches structured as IIIF manifests and presenting a corpus of 8196 views
- A fraction of the corpus of 1,335 views manually enriched with scientific keywords [data model created by a participatory expert annotation campaign](https://cloud.inha.fr/s/JmK4z2HAf6TseqB)

## **Objectives**
- Automatically classify 8196 views according to:
    - View types
    - Subjects represented
- Generate long titles for the images

## **Strategy adopted**
- Training of a supervised model (*YOLO nano v11*) on the images annotated by the research team for the first level of annotation and benchmarking
- Benchmarking of unsupervised models for the classification of subjects in the second level of annotation (*CLIP, EfficientNet, DINO-v2, ViT*)
- Inferences on non-annotated images to compare model results
- Creation of a graphical interface with the Python streamlit library for manual validation of automatic annotations
- Benchmarking of models for description generation (*Qwen3-Max, ministral-8b-2512, mistral-medium-2508, pixtral-12b-2409*)

## **Difficulties encountered**
- Errors in the manual annotations of certain images (they do not always follow the tree nodes) -> solution: correction with a script
- Not enough annotated data for each class in level 2 -> solution: unsupervised clustering for tag_2

## **Deliverables (in this folder)**
- ### **Code in the form of notebooks and .py code:**
    - **1-extraction_annotations.ipynb**: scraping of images with manual annotations and CSV creation
    - **2-training_yolo_tag1.ipynb**: data pre-processing and training of Yolov11n-cls for the first level
    - **3-training_yolo_tag2.ipynb**: data pre-processing and training of Yolov11n-cls for the second level
    - **4-inference_yolo.ipynb**: inference with Yolo and CSV production
    - **5-merge_inference_images_csv.ipynb**: script to add Yolo inferences to the CSV
    - **6-clustering_dino.ipynb**: inference and clustering (unsupervised) with Dinov2 for the second level
    - **7-clustering_efficentnet.ipynb**: inference and clustering (unsupervised) with EfficientNetv7 for the second level
    - **8-fusioner_clustering_images.ipynb**: script to merge clustering results (tag_2) into the images CSV
    - **9-IAnahid.py**: streamlit app for manual validation of annotations and caption generation (to be launched with the instructions in instruction_streamlit.txt)
- ### **Models:**
    - **Yolo best-unbalanced folder**: model weights, result.csv and confusion_matrix of a Yolov11n-cls model trained with an unbalanced dataset on photographs (tag_1)
    - **Yolo best-balanced folder**: model weights, result.csv and confusion_matrix of a Yolov11n-cls model trained with a balanced dataset across all classes (tag_1)
- ### **Documentation folder:**
    - **images_test_inference**: folder with a hundred images to test tag_1 inference
    - **images_inference.csv**: result of the Yolo inference (balanced)
    - **images_test_clustering**: folder with a hundred test photos for tag_2 clustering
    - **clustering_results(dino/eff).csv**: clustering results from Dino and EfficientNet
    - **instruction_IAnahid.txt**: information for launching streamlit
    - **exemple.csv**: file with random clustering to test the app

---

<a name="italiano"></a>

# Pre-indicizzazione automatica dei primi lotti di digitalizzazioni del fondo Nicole e Jean-Michel Thierry dell'INHA: Institut national d'histoire de l'art

Progetto realizzato da **Denise Atzori**, **Thaïs Raffray** e **Chiara Tedesco** nel quadro di una settimana di Hackathon organizzata dall'École nationale des Chartes - PSL.

## **Contesto**
Il fondo Nicole e Jean-Michel Thierry: circa 100.000 fotografie, film e dossier di documentazione e ricerca - 1950-2017.
Una prima fase di digitalizzazione sul patrimonio armeno e georgiano, destinata a essere documentata da una comunità di esperti.

## **Corpus e dati**
- 297 lotti d'archivio strutturati in manifesti IIIF e contenenti un corpus di 8196 viste
- Una frazione del corpus di 1.335 viste arricchite manualmente con parole chiave scientifiche [modello di dati creato tramite campagna di annotazione esperta partecipativa](https://cloud.inha.fr/s/JmK4z2HAf6TseqB)

## **Obiettivi**
- Classificare automaticamente 8196 viste secondo:
    - Tipi di vista
    - Soggetti rappresentati
- Generare titoli lunghi per le immagini

## **Strategia adottata**
- Addestramento di un modello supervisionato (*YOLO nano v11*) sulle immagini annotate dal team di ricerca per il primo livello di annotazione e benchmarking
- Benchmarking di modelli non supervisionati per la classificazione dei soggetti del secondo livello di annotazione (*CLIP, EfficientNet, DINO-v2, ViT*)
- Inferenze sulle immagini non annotate per confrontare i risultati dei modelli
- Creazione di un'interfaccia grafica con la libreria Python streamlit per la validazione manuale delle annotazioni automatiche
- Benchmarking dei modelli per la generazione delle descrizioni (*Qwen3-Max, ministral-8b-2512, mistral-medium-2508, pixtral-12b-2409*)

## **Difficoltà incontrate**
- Errori nelle annotazioni manuali di alcune immagini (non seguono sempre i nodi dell'alberatura) -> soluzione: correzione con uno script
- Insufficienza di dati annotati per ogni classe nel livello 2 -> soluzione: clustering non supervisionato per il tag_2

## **Consegnati (in questa cartella)**
- ### **Codice sotto forma di notebook e codice py:**
    - **1-extraction_annotations.ipynb**: scraping delle immagini con annotazioni manuali e creazione CSV
    - **2-training_yolo_tag1.ipynb**: pre-processing dei dati e addestramento Yolov11n-cls per il primo livello
    - **3-training_yolo_tag2.ipynb**: pre-processing dei dati e addestramento Yolov11n-cls per il secondo livello
    - **4-inference_yolo.ipynb**: inferenza con Yolo e produzione del csv
    - **5-merge_inference_images_csv.ipynb**: script per aggiungere le inferenze di Yolo sul csv
    - **6-clustering_dino.ipynb**: inferenza e clustering (non supervisionato) con Dinov2 per il secondo livello
    - **7-clustering_efficentnet.ipynb**: inferenza e clustering (non supervisionato) con EfficientNetv7 per il secondo livello
    - **8-fusioner_clustering_images.ipynb**: script per unire i risultati del clustering (tag_2) nel CSV delle immagini
    - **9-IAnahid.py**: app streamlit per la validazione manuale delle annotazioni e la generazione delle didascalie (da lanciare con le istruzioni in instruction_streamlit.txt)
- ### **Modelli:**
    - **Cartella Yolo best-unbalanced**: pesi del modello, result.csv e confusion_matrix di un modello Yolov11n-cls addestrato con un dataset sbilanciato sulle fotografie (tag_1)
    - **Cartella Yolo best-balanced**: pesi del modello, result.csv e confusion_matrix di un modello Yolov11n-cls addestrato con un dataset bilanciato su tutte le classi (tag_1)
- ### **Cartella Documentazione:**
    - **images_test_inference**: cartella con un centinaio di immagini per testare l'inferenza del tag_1
    - **images_inference.csv**: risultato dell'inferenza di Yolo (balanced)
    - **images_test_clustering**: cartella con un centinaio di foto di test per il clustering del tag_2
    - **clustering_results(dino/eff).csv**: risultati del clustering di Dino ed EfficientNet
    - **instruction_IAnahid.txt**: informazioni per lanciare streamlit
    - **exemple.csv**: file con un clustering casuale per provare l'app