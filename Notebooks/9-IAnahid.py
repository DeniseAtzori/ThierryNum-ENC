import streamlit as st
import pandas as pd
import os
import base64
import requests
from PIL import Image
import io
import random
from mistralai import Mistral

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Correcteur Clustering & IA", layout="wide")

st.markdown("""
    <style>
    .stImage > img { max-height: 40vh; width: auto; margin: auto; display: block; border-radius: 10px; border: 1px solid #ddd; }
    .stTextArea textarea { font-size: 1.1rem; }
    .stButton button { width: 100%; border-radius: 5px; }
    .nav-info { text-align: center; font-weight: bold; padding: 10px; background: #f0f2f6; border-radius: 5px; }
    /* Style pour la grille d'images du cluster */
    .cluster-grid img { max-height: 200px; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

CSV_PATH = "random.csv"

PROMPT_MISTRAL = """Règles :
* Décrire uniquement les éléments visuellement observables (architecture, matériaux, organisation spatiale, objets, personnes, vêtements, gestes, inscriptions, paysage).
* Ne pas interpréter le sens, le symbolisme ou le contexte historique.
* Employer un langage précis, neutre et documentaire.
* Rédiger en phrases complètes (paragraphe), 2-3 lignes maximum.
Sortie : Une légende unique adaptée à un catalogue d'archive patrimoniale."""

VOCAB_TAG_2 = ["2.1 Architecture", "2.2 Objet", "2.3 Personne", "2.4 Paysage", "2.5 Animal", "2.6 Végétal"]

# --- FONCTIONS DE CHARGEMENT ---
@st.cache_data
def load_data(path):
    if not os.path.exists(path):
        st.error(f"Fichier {path} non trouvé.")
        return pd.DataFrame()
    
    with open(path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        separator = ';' if ';' in first_line else ','
    
    df = pd.read_csv(path, sep=separator, quotechar='"', on_bad_lines='warn', encoding='utf-8')
    df.columns = [c.strip() for c in df.columns]
    
    cols_check = {
        'validated_tag_1': False, 'validated_tag_2': False, 
        'validated_caption': False, 'image_caption': "",
        'tag_1': "", 'tag_2': "", 'clustering_id': "0"
    }
    for col, default in cols_check.items():
        if col not in df.columns:
            df[col] = default
            
    return df

def save_data(df, path):
    df.to_csv(path, sep=',', index=False, quoting=1, encoding='utf-8')

def get_image_as_b64(url):
    try:
        response = requests.get(url, timeout=10)
        img = Image.open(io.BytesIO(response.content))
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        return None

# --- INITIALISATION ---
if 'df' not in st.session_state:
    st.session_state.df = load_data(CSV_PATH)

# --- NAVIGATION ---
def get_first_unvalidated(col):
    df = st.session_state.df
    mask = (df[col] == False) | (df[col].isna()) | (df[col] == "")
    non_val = df[mask].index
    return non_val[0] if not non_val.empty else 0

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛠️ Configuration")
    if st.session_state.df.empty: st.stop()

    mode = st.radio("Mode de travail :", ["tag_1", "tag_2", "Légende (IA)", "Validation par Cluster"])
    st.divider()
    
    st.subheader("🔑 API Mistral")
    api_key = st.text_input("Clé API Mistral", type="password")
    model_name = st.selectbox("Modèle", ["pixtral-12b-2409", "ministral-8b-2512", "mistral-medium-2508"])
    
    st.divider()
    if mode != "Validation par Cluster":
        target_col = "validated_caption" if mode == "Légende (IA)" else f"validated_{mode}"
        done = st.session_state.df[st.session_state.df[target_col] == True].shape[0]
        total = len(st.session_state.df)
        st.metric("Images validées", f"{done} / {total}", f"{int(done/total*100) if total > 0 else 0}%")

# Reset index si changement de mode
if 'last_mode' not in st.session_state or st.session_state.last_mode != mode:
    st.session_state.last_mode = mode
    st.session_state.show_correction = False
    if mode == "Validation par Cluster":
        st.session_state.cluster_idx = 0
    else:
        target_col = "validated_caption" if mode == "Légende (IA)" else f"validated_{mode}"
        st.session_state.current_idx = get_first_unvalidated(target_col)

# --- LOGIQUE DE NAVIGATION CLASSIQUE ---
def move_next():
    if st.session_state.current_idx < len(st.session_state.df) - 1:
        st.session_state.current_idx += 1
        st.session_state.show_correction = False

def move_prev():
    if st.session_state.current_idx > 0:
        st.session_state.current_idx -= 1
        st.session_state.show_correction = False

# --- INTERFACE PRINCIPALE ---
st.title(f"🔍 Mode : {mode}")

# ---------------------------------------------------------
# MODE CLUSTER (NOUVELLE FONCTION)
# ---------------------------------------------------------
# ---------------------------------------------------------
# MODE CLUSTER (CORRIGÉ POUR ÉVITER LES 'NAN')
# ---------------------------------------------------------
if mode == "Validation par Cluster":
    # On récupère les IDs uniques, on convertit en string et on retire les valeurs nulles (nan)
    all_clusters = st.session_state.df['clustering_id'].dropna().unique().tolist()
    clusters = sorted([str(c) for c in all_clusters if str(c).lower() != 'nan' and str(c).strip() != ''])
    
    total_clusters = len(clusters)
    
    if total_clusters == 0:
        st.warning("Aucun cluster trouvé dans la colonne 'clustering_id'.")
    else:
        if 'cluster_idx' not in st.session_state or st.session_state.cluster_idx >= total_clusters:
            st.session_state.cluster_idx = 0
            
        c_id = clusters[st.session_state.cluster_idx]
        
        # Navigation Cluster
        col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
        with col_nav1:
            if st.button("⬅️ CLUSTER PRÉCÉDENT") and st.session_state.cluster_idx > 0:
                st.session_state.cluster_idx -= 1
                st.rerun()
        with col_nav2:
            if st.button("⏭️ SKIP CLUSTER (Sans valider)"):
                if st.session_state.cluster_idx < total_clusters - 1:
                    st.session_state.cluster_idx += 1
                    st.rerun()
        with col_nav3:
            st.markdown(f"<div class='nav-info'>Cluster {st.session_state.cluster_idx + 1} / {total_clusters}<br>(ID: {c_id})</div>", unsafe_allow_html=True)

        st.write(f"### Échantillon de 10 images pour le cluster : **{c_id}**")
        
        # Sélection des images (on convertit la colonne en string pour la comparaison)
        mask = st.session_state.df['clustering_id'].astype(str) == c_id
        df_cluster = st.session_state.df[mask]
        
        if df_cluster.empty:
            st.error("Ce cluster semble vide ou introuvable.")
        else:
            sample_size = min(10, len(df_cluster))
            df_sample = df_cluster.sample(n=sample_size, random_state=42)
            
            # Affichage en grille
            cols = st.columns(5)
            for i, (_, r) in enumerate(df_sample.iterrows()):
                if pd.notna(r['image_url']):
                    cols[i % 5].image(r['image_url'], use_container_width=True)
                else:
                    cols[i % 5].write("Image manquante")

            st.divider()
            
            # Action du cluster
            st.subheader("Attribuer une classe à tout le cluster")
            chosen_class = st.selectbox("Choisir la classe pour toutes ces images :", VOCAB_TAG_2, key="cluster_select")
            
            if st.button("✅ APPLIQUER À TOUT LE CLUSTER ET SUIVANT", type="primary"):
                # Mise à jour avec conversion string pour être sûr de matcher
                st.session_state.df.loc[st.session_state.df['clustering_id'].astype(str) == c_id, 'tag_2'] = chosen_class
                st.session_state.df.loc[st.session_state.df['clustering_id'].astype(str) == c_id, 'validated_tag_2'] = True
                
                save_data(st.session_state.df, CSV_PATH)
                st.success(f"Classe '{chosen_class}' appliquée au cluster {c_id}")
                
                if st.session_state.cluster_idx < total_clusters - 1:
                    st.session_state.cluster_idx += 1
                st.rerun()

# ---------------------------------------------------------
# MODES CLASSIQUES (tag_1, tag_2, Légende)
# ---------------------------------------------------------
else:
    idx = st.session_state.current_idx
    row = st.session_state.df.iloc[idx]
    total = len(st.session_state.df)

    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    with col_nav1:
        if st.button("⬅️ PRÉCÉDENT"):
            move_prev()
            st.rerun()
    with col_nav2:
        if st.button("⏭️ SKIP / SUIVANT (Sans valider)"):
            move_next()
            st.rerun()
    with col_nav3:
        st.markdown(f"<div class='nav-info'>{idx + 1} / {total}</div>", unsafe_allow_html=True)

    st.image(row['image_url'], caption=f"ID: {row.get('title', 'Sans titre')} | Cluster: {row.get('clustering_id', 'N/A')}")

    st.write("---")

    if mode in ["tag_1", "tag_2"]:
        val_actuelle = row[mode] if pd.notna(row[mode]) else "Non défini"
        st.info(f"**Valeur actuelle :** `{val_actuelle}`")
        
        c_ok, c_mod = st.columns(2)
        if c_ok.button("✅ VALIDER CETTE ATTRIBUTION", type="secondary"):
            st.session_state.df.at[idx, target_col] = True
            save_data(st.session_state.df, CSV_PATH)
            move_next()
            st.rerun()
            
        if c_mod.button("❌ MODIFIER LA CATÉGORIE"):
            st.session_state.show_correction = True

        if st.session_state.get('show_correction', False):
            vocab = ["1.1. Photographie", "1.2. Document écrit", "1.3 Autre document reproduit", "1.4. Matériel de conditionnement"] if mode == "tag_1" else VOCAB_TAG_2
            new_val = st.selectbox("Sélection :", vocab)
            if st.button("Enregistrer et Suivant"):
                st.session_state.df.at[idx, mode] = new_val
                st.session_state.df.at[idx, target_col] = True
                save_data(st.session_state.df, CSV_PATH)
                move_next()
                st.rerun()

    else: # MODE LÉGENDE
        if not api_key:
            st.warning("Clé API requise à gauche.")
        else:
            if st.button("🤖 Générer avec Mistral", type="primary"):
                with st.spinner("IA en cours..."):
                    img_b64 = get_image_as_b64(row['image_url'])
                    if img_b64:
                        try:
                            client = Mistral(api_key=api_key)
                            res = client.chat.complete(
                                model=model_name,
                                messages=[{"role": "user", "content": [{"type": "text", "text": PROMPT_MISTRAL}, {"type": "image_url", "image_url": f"data:image/jpeg;base64,{img_b64}"}]}]
                            )
                            st.session_state.temp_caption = res.choices[0].message.content.strip()
                        except Exception as e:
                            st.error(f"Erreur API : {e}")

            curr_cap = st.session_state.get('temp_caption', row['image_caption'])
            final_cap = st.text_area("Légende :", value=curr_cap if pd.notna(curr_cap) else "", height=150)
            
            if st.button("💾 ENREGISTRER LA LÉGENDE ET SUIVANT"):
                st.session_state.df.at[idx, 'image_caption'] = final_cap
                st.session_state.df.at[idx, 'validated_caption'] = True
                save_data(st.session_state.df, CSV_PATH)
                move_next()
                st.rerun()

# Aperçu du fichier pour vérification
with st.expander("Voir le tableau complet"):
    st.dataframe(st.session_state.df)