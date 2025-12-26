import streamlit as st
import google.generativeai as genai
from PIL import Image
import os
import json

# Connexion à l'API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="LibrisScan", layout="centered")

st.title("📚 Assistant de Lecture")

# Capture Photo
img_file = st.camera_input("Scanner la couverture")

if img_file:
    img = Image.open(img_file)
    
    # Instruction de formatage
    prompt = "Identifie ce livre. Réponds UNIQUEMENT au format JSON avec les clés : titre, auteur, editeur, annee, essence, architecture, critique, extraits, achat_lien."
    
    with st.spinner('Analyse littéraire en cours...'):
        response = model.generate_content([prompt, img])
        # Nettoyage et lecture du JSON
        data = json.loads(response.text.replace('```json', '').replace('```', ''))
        
        # Affichage structuré
        st.header(f"{data['titre']}")
        st.subheader(f"{data['auteur']} | {data['editeur']} ({data['annee']})")
        
        st.markdown("### 🖋️ L'Essence")
        st.write(data['essence'])
        
        st.markdown("### 🏗️ Architecture")
        st.write(data['architecture'])
        
        st.markdown("### 🔍 Critique")
        st.write(data['critique'])
        
        st.markdown("### 💬 Extraits")
        for ex in data['extraits']:
            st.info(ex)
            
        # Bouton d'achat
        st.link_button("Acheter sur Place des Libraires", data['achat_lien'])
