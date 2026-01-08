import streamlit as st
import pandas as pd
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Correcteur de Clustering Pro", layout="wide")

# Injection de CSS pour le redimensionnement d'image adaptatif
st.markdown("""
    <style>
    .stImage > img {
        max-height: 60vh;
        width: auto;
        margin-left: auto;
        margin-right: auto;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PARAMÈTRES ET CONSTANTES ---
CSV_PATH = "images_inference_ok.csv" #PATH CSV

# Vocabulaires contrôlés
VOCAB_TAG_1 = [
    "1.1. Photographie", 
    "1.2. Réproduction de plan architectural", 
    "1.3 Autre document reproduit (gravure, dessin, etc)", 
    "1.4. Matériel de conditionnement"
    "1.5 Autre"
]

VOCAB_TAG_2 = [
    "2.1 Architecture", 
    "2.2 Objet", 
    "2.3 Personne", 
    "2.4 Paysage", 
    "2.5 Animal", 
    "2.6 Végétal"
]

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Initialisation des colonnes de validation si absentes
        if 'validated_tag_1' not in df.columns:
            df['validated_tag_1'] = False
        if 'validated_tag_2' not in df.columns:
            df['validated_tag_2'] = False
        return df
    else:
        st.error(f"Fichier {path} introuvable.")
        return None

def save_data(df, path):
    df.to_csv(path, index=False)

# Initialisation du DataFrame
if 'df' not in st.session_state:
    st.session_state.df = load_data(CSV_PATH)

# --- BARRE LATÉRALE (SÉLECTION DU MODE) ---
with st.sidebar:
    st.title("⚙️ Paramètres")
    tag_target = st.radio(
        "Sur quel tag souhaitez-vous travailler ?",
        ("tag_1", "tag_2"),
        help="L'application filtrera les images non validées pour ce tag spécifique."
    )
    
    # Mise à jour du vocabulaire selon le choix
    current_vocab = VOCAB_TAG_1 if tag_target == "tag_1" else VOCAB_TAG_2
    validation_col = f"validated_{tag_target}"

    st.divider()
    
    # Statistiques
    df = st.session_state.df
    done = df[validation_col].sum()
    total = len(df)
    st.metric("Progression", f"{done}/{total}", f"{int(done/total*100)}%")
    
    if st.button("Sauvegarder maintenant"):
        save_data(st.session_state.df, CSV_PATH)
        st.success("Fichier enregistré !")

# --- LOGIQUE D'INDEXATION ---
def get_next_index(target_col):
    df = st.session_state.df
    non_validated = df[df[f"validated_{target_col}"] == False].index
    return non_validated[0] if not non_validated.empty else None

# Réinitialiser l'index si on change de tag cible
if 'last_tag_target' not in st.session_state or st.session_state.last_tag_target != tag_target:
    st.session_state.current_idx = get_next_index(tag_target)
    st.session_state.last_tag_target = tag_target
    st.session_state.show_correction = False

# --- LOGIQUE DE VALIDATION ---
def validate_entry(correct_tag=None):
    idx = st.session_state.current_idx
    col_to_update = tag_target
    val_col = f"validated_{tag_target}"
    
    if correct_tag:
        st.session_state.df.at[idx, col_to_update] = correct_tag
    
    st.session_state.df.at[idx, val_col] = True
    save_data(st.session_state.df, CSV_PATH)
    
    # Passer à la suivante
    st.session_state.current_idx = get_next_index(tag_target)
    st.session_state.show_correction = False

# --- INTERFACE PRINCIPALE ---
st.title(f"🔍 Correction manuelle : {tag_target}")

if st.session_state.current_idx is not None:
    idx = st.session_state.current_idx
    row = st.session_state.df.iloc[idx]
    
    # Affichage de l'image (le CSS s'occupe du resize)
    st.image(row['image_url'], caption=row['title'])
    
    valeur_actuelle = row[tag_target] if pd.notna(row[tag_target]) else "Vide"
    
    st.info(f"**Valeur actuelle pour {tag_target} :** `{valeur_actuelle}`")
    
    st.write("### Est-ce correct ?")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ OUI (Valider)", use_container_width=True):
            validate_entry()
            st.rerun()
    with c2:
        if st.button("❌ NON (Modifier)", use_container_width=True):
            st.session_state.show_correction = True

    # Formulaire de correction
    if st.session_state.get('show_correction', False):
        st.write("---")
        # On propose le vocabulaire ou la saisie libre
        choix = st.selectbox("Sélectionnez la catégorie correcte :", ["-- Choisir --"] + current_vocab)
        
        # Optionnel: saisie libre si non présent dans la liste
        saisie_libre = st.text_input("Ou saisir manuellement si absent de la liste :")
        
        if st.button("Confirmer la modification"):
            final_val = saisie_libre if saisie_libre else choix
            if final_val != "-- Choisir --" or saisie_libre:
                validate_entry(final_val)
                st.rerun()
            else:
                st.warning("Veuillez sélectionner ou saisir une valeur.")

else:
    st.balloons()
    st.success(f"Toutes les images ont été validées pour le **{tag_target}** !")
    if st.button("Réinitialiser les validations pour ce tag"):
        st.session_state.df[validation_col] = False
        save_data(st.session_state.df, CSV_PATH)
        st.rerun()

# Aperçu du tableau en bas
with st.expander("Voir le tableau des données"):
    st.dataframe(st.session_state.df)