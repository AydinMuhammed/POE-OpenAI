import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
import base64

# Configuration de la page
st.set_page_config(
    page_title="Analyse d'Images Vision",
    page_icon="👁️",
    layout="wide"
)

# Titre de la page
st.title("👁️ Analyse d'Images avec Vision AI")
st.markdown("---")

# Configuration de l'API OpenAI avec saisie utilisateur
def initialize_openai_client(api_key):
    """Initialise le client OpenAI avec la clé API fournie par l'utilisateur"""
    try:
        if not api_key:
            return None
        
        if not api_key.startswith('sk-'):
            st.error("❌ Format de clé API invalide. La clé doit commencer par 'sk-'")
            return None
        
        # Initialisation du client OpenAI
        client = OpenAI(api_key=api_key)
        
        # Test de validation de la clé API
        try:
            # Test simple pour vérifier si la clé fonctionne
            test_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return client
        except Exception as e:
            st.error(f"❌ Clé API invalide ou problème de connexion: {str(e)}")
            return None
            
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation du client OpenAI: {str(e)}")
        return None

def vision_analyze_image(client, image, analysis_type="general"):
    """
    Analyse une image avec l'API Vision d'OpenAI
    
    Args:
        client: Client OpenAI initialisé
        image: Image PIL à analyser
        analysis_type: Type d'analyse ("general", "objects", "text", "detailed")
    
    Returns:
        str: Description/analyse de l'image
    """
    try:
        # Conversion de l'image en base64
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        image_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        # Définir le prompt selon le type d'analyse
        prompts = {
            "general": "Décris cette image de manière détaillée. Que vois-tu ?",
            "objects": "Identifie et liste tous les objets visibles dans cette image. Sois précis et méthodique.",
            "text": "Y a-t-il du texte dans cette image ? Si oui, transcris-le et explique son contexte.",
            "detailed": "Fais une analyse complète et détaillée de cette image : objets, personnes, couleurs, composition, style, ambiance, texte éventuel, et tout autre élément notable.",
            "artistic": "Analyse cette image d'un point de vue artistique : composition, couleurs, style, technique, émotion transmise.",
            "technical": "Analyse les aspects techniques de cette image : qualité, éclairage, perspective, mise au point, etc."
        }
        
        prompt = prompts.get(analysis_type, prompts["general"])
        
        # Appel à l'API Vision avec le nouveau modèle
        response = client.chat.completions.create(
            model="gpt-4o",  # Nouveau modèle Vision d'OpenAI
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse de l'image: {str(e)}")
        return None

def extract_image_metadata(image):
    """Extrait les métadonnées de base de l'image"""
    try:
        metadata = {
            "Format": image.format,
            "Mode": image.mode,
            "Taille": f"{image.size[0]} x {image.size[1]} pixels",
            "Nombre de canaux": len(image.getbands()) if hasattr(image, 'getbands') else "N/A"
        }
        
        # Essayer d'extraire des métadonnées EXIF si disponibles
        if hasattr(image, '_getexif') and image._getexif():
            exif = image._getexif()
            if exif:
                metadata["EXIF disponible"] = "Oui"
        
        return metadata
    except Exception as e:
        return {"Erreur": f"Impossible d'extraire les métadonnées: {str(e)}"}

# Section de saisie de la clé API
st.subheader("🔑 Configuration de l'API OpenAI")

col1, col2 = st.columns([3, 1])

with col1:
    api_key = st.text_input(
        "Entrez votre clé API OpenAI:",
        type="password",
        placeholder="sk-proj-...",
        help="Votre clé API OpenAI. Elle commence par 'sk-proj-' ou 'sk-'."
    )

with col2:
    st.markdown("### 💡 Comment obtenir une clé API ?")
    st.markdown("""
    1. Allez sur [platform.openai.com](https://platform.openai.com)
    2. Connectez-vous à votre compte
    3. Allez dans "API Keys"
    4. Créez une nouvelle clé
    5. Copiez-la ici
    """)

# Initialisation du client OpenAI
client = None
if api_key:
    with st.spinner("🔍 Validation de la clé API..."):
        client = initialize_openai_client(api_key)
    
    if client:
        st.success("✅ Clé API validée avec succès !")
    else:
        st.warning("⚠️ Clé API non validée. Veuillez vérifier votre clé.")

# Interface utilisateur (seulement si la clé API est valide)
if client:
    st.markdown("---")
    
    # Onglets pour différentes fonctionnalités
    tab1, tab2, tab3 = st.tabs(["🖼️ Analyser une Image", "📊 Analyse Comparative", "ℹ️ Informations"])

    with tab1:
        st.header("Analyse d'Image avec Vision AI")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Upload d'Image")
            
            # Upload d'image
            uploaded_file = st.file_uploader(
                "Choisissez une image à analyser",
                type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
                help="Formats supportés: PNG, JPG, JPEG, GIF, BMP"
            )
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Image à analyser", use_container_width=True)
                
                # Métadonnées de l'image
                with st.expander("📋 Métadonnées de l'image"):
                    metadata = extract_image_metadata(image)
                    for key, value in metadata.items():
                        st.text(f"{key}: {value}")
        
        with col2:
            st.subheader("🔍 Analyse")
            
            if uploaded_file:
                # Type d'analyse
                analysis_type = st.selectbox(
                    "Type d'analyse:",
                    ["general", "objects", "text", "detailed", "artistic", "technical"],
                    format_func=lambda x: {
                        "general": "🔍 Analyse générale",
                        "objects": "🎯 Détection d'objets",
                        "text": "📝 Reconnaissance de texte",
                        "detailed": "📖 Analyse détaillée",
                        "artistic": "🎨 Analyse artistique",
                        "technical": "⚙️ Analyse technique"
                    }[x]
                )
                
                # Bouton d'analyse
                if st.button("🚀 Analyser l'image", key="analyze", type="primary"):
                    with st.spinner("🔄 Analyse en cours..."):
                        analysis_result = vision_analyze_image(client, image, analysis_type)
                    
                    if analysis_result:
                        st.success("✅ Analyse terminée !")
                        
                        # Affichage du résultat
                        st.markdown("### 📋 Résultat de l'analyse")
                        st.markdown(analysis_result)
                        
                        # Sauvegarder dans la session pour comparaison
                        if 'analyses' not in st.session_state:
                            st.session_state.analyses = []
                        
                        st.session_state.analyses.append({
                            'image': image.copy(),
                            'type': analysis_type,
                            'result': analysis_result,
                            'filename': uploaded_file.name
                        })
                        
                        st.info("💾 Analyse sauvegardée pour comparaison dans l'onglet 'Analyse Comparative'")
            else:
                st.info("👆 Veuillez d'abord uploader une image")

    with tab2:
        st.header("📊 Analyse Comparative")
        
        if 'analyses' in st.session_state and st.session_state.analyses:
            st.markdown(f"**{len(st.session_state.analyses)} analyse(s) sauvegardée(s)**")
            
            # Affichage des analyses précédentes
            for i, analysis in enumerate(st.session_state.analyses):
                with st.expander(f"📸 {analysis['filename']} - {analysis['type']}"):
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.image(analysis['image'], caption=analysis['filename'], use_container_width=True)
                    
                    with col2:
                        st.markdown("**Type d'analyse:** " + analysis['type'])
                        st.markdown("**Résultat:**")
                        st.write(analysis['result'])
            
            # Bouton pour effacer l'historique
            if st.button("🗑️ Effacer l'historique"):
                st.session_state.analyses = []
                st.success("Historique effacé !")
                st.rerun()
        else:
            st.info("Aucune analyse sauvegardée. Analysez des images dans l'onglet 'Analyser une Image' pour les voir ici.")

    with tab3:
        st.header("ℹ️ Informations sur l'Analyse d'Images")
        
        st.markdown("""
        ### 🤖 À propos de Vision AI
        
        Cette application utilise **GPT-4o** d'OpenAI pour analyser les images.
        GPT-4o est le modèle multimodal le plus récent qui supporte l'analyse d'images.
        
        ### 🎯 Types d'analyses disponibles
        
        **🔍 Analyse générale**
        - Description générale de l'image
        - Identification des éléments principaux
        - Contexte et ambiance
        
        **🎯 Détection d'objets**
        - Liste détaillée des objets identifiés
        - Position et caractéristiques des objets
        - Relations entre les éléments
        
        **📝 Reconnaissance de texte**
        - Extraction du texte visible
        - Transcription et contexte
        - Analyse du contenu textuel
        
        **📖 Analyse détaillée**
        - Analyse complète et approfondie
        - Tous les éléments visuels
        - Description exhaustive
        
        **🎨 Analyse artistique**
        - Composition et style
        - Couleurs et technique
        - Émotion et esthétique
        
        **⚙️ Analyse technique**
        - Qualité de l'image
        - Aspects techniques
        - Éclairage et perspective
        
        ### 📋 Formats supportés
        - PNG, JPG, JPEG
        - GIF, BMP
        - Taille maximale recommandée: 20MB
        
        ### 💡 Conseils d'utilisation
        - Utilisez des images claires et bien éclairées
        - Évitez les images trop petites ou floues
        - Essayez différents types d'analyse pour des résultats variés
        - Sauvegardez vos analyses pour les comparer
        """)

else:
    # Message d'information si pas de clé API
    st.info("🔑 Veuillez entrer une clé API OpenAI valide pour utiliser l'analyse d'images.")
    
    st.markdown("### 📋 Instructions d'utilisation")
    st.markdown("""
    1. **Obtenez une clé API** sur [platform.openai.com](https://platform.openai.com/api-keys)
    2. **Entrez votre clé** dans le champ ci-dessus
    3. **Attendez la validation** (vérification automatique)
    4. **Uploadez une image** et choisissez le type d'analyse
    5. **Cliquez sur "Analyser l'image"** pour obtenir les résultats
    
    ⚠️ **Note de sécurité:** Votre clé API n'est pas stockée et reste privée à votre session.
    """)

# Sidebar avec informations
with st.sidebar:
    st.markdown("### 👁️ Vision AI")
    st.markdown("""
    **Fonctionnalités:**
    - 🔍 Analyse générale d'images
    - 🎯 Détection d'objets
    - 📝 Reconnaissance de texte
    - 🎨 Analyse artistique
    - ⚙️ Analyse technique
    - 📊 Comparaison d'analyses
    """)
    
    st.markdown("### 💡 Avantages")
    st.markdown("""
    - Analyse précise et détaillée
    - Multiples types d'analyses
    - Interface intuitive
    - Sauvegarde des résultats
    - Pas de limite de format
    """)
    
    # Statut de la connexion API
    st.markdown("### 🔌 Statut de l'API")
    if client:
        st.success("Connecté ✅")
    else:
        st.error("Non connecté ❌")

# Style CSS personnalisé
st.markdown("""
<style>
    .stTextInput > div > div > input[type="password"] {
        font-family: monospace;
    }
    
    .analysis-result {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)
