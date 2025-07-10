import streamlit as st
import openai
import requests
from io import BytesIO
import base64
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Projet Final - Générateur d'Histoires Visuelles",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Générateur d'Histoires Visuelles")
st.markdown("---")

# Fonctions utilitaires
def initialize_openai_client(api_key):
    """Initialise le client OpenAI avec la clé API fournie par l'utilisateur"""
    try:
        if not api_key:
            return None
        
        if not api_key.startswith('sk-'):
            st.error("❌ Format de clé API invalide. La clé doit commencer par 'sk-'")
            return None
        
        # Initialisation du client OpenAI
        client = openai.OpenAI(api_key=api_key)
        
        # Test de validation de la clé API
        try:
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

def improve_story_prompt(client, user_prompt, creativity_level=0.8):
    """Améliore et complète un prompt d'histoire avec ChatGPT"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """Tu es un expert en création d'histoires et en génération d'images. 
                 Ta mission est d'améliorer et de compléter un prompt d'histoire fourni par l'utilisateur.
                 Tu dois:
                 1. Enrichir l'histoire avec des détails visuels
                 2. Ajouter des éléments narratifs captivants
                 3. Créer une description qui sera parfaite pour générer une image
                 4. Garder l'essence de l'idée originale
                 5. Répondre en français
                 6. IMPORTANT: Éviter tout contenu violent, politique, sexuel ou inapproprié
                 7. Privilégier des thèmes positifs, créatifs et familiaux
                 
                 Ton amélioration doit être créative, détaillée, visuellement riche et adaptée à DALL-E."""},
                {"role": "user", "content": f"Améliore et complète cette idée d'histoire en évitant tout contenu inapproprié: {user_prompt}"}
            ],
            max_tokens=500,
            temperature=creativity_level
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"❌ Erreur lors de l'amélioration du prompt: {str(e)}")
        return None

def generate_image_with_dalle(client, prompt, size="1024x1024", quality="standard"):
    """Génère une image avec DALL-E basée sur le prompt"""
    try:
        # Nettoyer et optimiser le prompt pour DALL-E
        cleaned_prompt = clean_prompt_for_dalle(prompt)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=cleaned_prompt,
            size=size,
            quality=quality,
            n=1
        )
        
        # Récupérer l'URL de l'image
        image_url = response.data[0].url
        
        # Télécharger l'image
        image_response = requests.get(image_url)
        image_data = BytesIO(image_response.content)
        
        return image_data, image_url
        
    except Exception as e:
        error_message = str(e)
        if "image_generation_user_error" in error_message:
            st.error("❌ Le contenu de votre histoire ne peut pas être illustré par DALL-E.")
            st.error("💡 Essayez de modifier votre histoire pour éviter les contenus sensibles, violents ou inappropriés.")
            st.info("🔄 Vous pouvez personnaliser le prompt dans la section 'Personnaliser le prompt pour l'image'")
        else:
            st.error(f"❌ Erreur lors de la génération d'image: {str(e)}")
        return None, None

def clean_prompt_for_dalle(prompt):
    """Nettoie et optimise le prompt pour DALL-E"""
    # Supprimer les mots ou phrases potentiellement problématiques
    problematic_words = [
        "violent", "violence", "sang", "mort", "tuer", "guerre", "arme",
        "politique", "religion", "sexuel", "nu", "nudité", "drogue",
        "alcool", "cigarette", "tabac", "haine", "discrimination"
    ]
    
    cleaned_prompt = prompt.lower()
    
    # Remplacer les mots problématiques par des alternatives
    replacements = {
        "violent": "énergique",
        "violence": "action",
        "sang": "rouge",
        "mort": "endormi",
        "tuer": "vaincre",
        "guerre": "conflit",
        "arme": "outil",
        "politique": "gouvernement",
        "religion": "spiritualité",
        "drogue": "potion",
        "alcool": "boisson",
        "cigarette": "bâton",
        "tabac": "herbe"
    }
    
    for word, replacement in replacements.items():
        cleaned_prompt = cleaned_prompt.replace(word, replacement)
    
    # Limiter la longueur du prompt (DALL-E a une limite)
    if len(cleaned_prompt) > 1000:
        cleaned_prompt = cleaned_prompt[:1000] + "..."
    
    # Ajouter des termes positifs pour améliorer la génération
    positive_terms = "artistic, beautiful, detailed, high quality, masterpiece"
    cleaned_prompt = f"{cleaned_prompt}, {positive_terms}"
    
    return cleaned_prompt

def describe_image(client, image_data):
    """Génère une description de l'image avec GPT-4 Vision"""
    try:
        # Convertir l'image en base64
        image_data.seek(0)
        image_base64 = base64.b64encode(image_data.read()).decode()
        
        response = client.chat.completions.create(
            model="gpt-4o",  # Modèle mis à jour pour Vision
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Décris cette image en détail. Raconte ce que tu vois, l'atmosphère, les couleurs, les personnages, l'action qui se déroule. Sois créatif et narratif dans ta description."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la description d'image: {str(e)}")
        st.error(f"Détails de l'erreur: {type(e).__name__}")
        return None

# Section de saisie de la clé API
st.subheader("🔑 Configuration de l'API OpenAI")

col1, col2 = st.columns([3, 1])

with col1:
    api_key = st.text_input(
        "Entrez votre clé API OpenAI:",
        type="password",
        placeholder="sk-...",
        help="Votre clé API OpenAI. Elle commence par 'sk-'."
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

# Interface utilisateur principale
if client:
    st.markdown("---")
    
    # Onglets pour organiser le workflow
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Création d'Histoire", "🎨 Génération d'Image", "🖼️ Galerie", "ℹ️ À propos"])
    
    with tab1:
        st.header("📝 Création et Amélioration d'Histoire")
        st.markdown("Commencez par entrer votre idée d'histoire, l'IA l'améliorera pour vous !")
        
        # Zone de saisie du prompt utilisateur
        user_prompt = st.text_area(
            "Entrez votre idée d'histoire:",
            placeholder="Ex: Un chat magique qui explore une forêt enchantée...",
            height=100,
            help="Décrivez votre idée d'histoire, même brièvement. L'IA va l'enrichir !"
        )
        
        # Paramètres pour l'amélioration
        with st.expander("⚙️ Paramètres d'amélioration"):
            creativity_level = st.slider(
                "Niveau de créativité",
                min_value=0.1,
                max_value=1.0,
                value=0.8,
                step=0.1,
                help="Plus élevé = plus créatif mais moins prévisible"
            )
        
        if st.button("🚀 Améliorer mon histoire", type="primary", disabled=not user_prompt):
            if user_prompt:
                with st.spinner("🔄 Amélioration de votre histoire en cours..."):
                    improved_prompt = improve_story_prompt(client, user_prompt, creativity_level)
                
                if improved_prompt:
                    st.success("✅ Histoire améliorée avec succès !")
                    
                    # Afficher l'amélioration
                    st.markdown("### 📖 Votre histoire améliorée")
                    st.markdown(f"**Histoire originale:** {user_prompt}")
                    st.markdown("---")
                    st.markdown(f"**Histoire améliorée:** {improved_prompt}")
                    
                    # Stocker dans la session
                    st.session_state.improved_story = improved_prompt
                    st.session_state.original_story = user_prompt
                    
                    st.info("👉 Passez à l'onglet 'Génération d'Image' pour créer une image de votre histoire !")
    
    with tab2:
        st.header("🎨 Génération d'Image avec DALL-E")
        st.markdown("Créez une image basée sur votre histoire améliorée")
        
        # Vérifier si une histoire améliorée existe
        if "improved_story" in st.session_state:
            st.markdown("### 📖 Histoire à illustrer")
            st.info(st.session_state.improved_story)
            
            # Paramètres de génération d'image
            col1, col2 = st.columns(2)
            
            with col1:
                image_size = st.selectbox(
                    "Taille de l'image",
                    ["1024x1024", "1792x1024", "1024x1792"],
                    help="Format carré ou rectangulaire"
                )
            
            with col2:
                image_quality = st.selectbox(
                    "Qualité de l'image",
                    ["standard", "hd"],
                    help="HD coûte plus cher mais offre plus de détails"
                )
            
            # Option pour modifier le prompt avant génération
            with st.expander("🎨 Personnaliser le prompt pour l'image"):
                st.markdown("💡 **Conseil:** Évitez les contenus violents, politiques ou inappropriés pour DALL-E")
                custom_prompt = st.text_area(
                    "Modifiez le prompt si nécessaire:",
                    value=st.session_state.improved_story,
                    height=150,
                    help="Vous pouvez ajuster le prompt pour l'image. Évitez les contenus sensibles."
                )
                
                # Afficher un aperçu du prompt nettoyé
                if custom_prompt:
                    cleaned_preview = clean_prompt_for_dalle(custom_prompt)
                    if cleaned_preview != custom_prompt.lower() + ", artistic, beautiful, detailed, high quality, masterpiece":
                        st.info("🔄 Aperçu du prompt optimisé pour DALL-E:")
                        st.code(cleaned_preview[:200] + "..." if len(cleaned_preview) > 200 else cleaned_preview)
            
            if "custom_prompt" not in locals():
                custom_prompt = st.session_state.improved_story
            
            # Bouton de génération
            if st.button("🎨 Générer l'image", type="primary"):
                with st.spinner("🎨 Génération de l'image en cours... (cela peut prendre 30-60 secondes)"):
                    image_data, image_url = generate_image_with_dalle(
                        client, 
                        custom_prompt, 
                        size=image_size, 
                        quality=image_quality
                    )
                
                if image_data and image_url:
                    st.success("✅ Image générée avec succès !")
                    
                    # Afficher l'image
                    image = Image.open(image_data)
                    st.image(image, caption="Votre histoire visualisée", use_column_width=True)
                    
                    # Stocker dans la session
                    st.session_state.generated_image = image_data
                    st.session_state.image_url = image_url
                    st.session_state.image_prompt = custom_prompt
                    
                    # Boutons d'action
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Téléchargement
                        image_data.seek(0)
                        st.download_button(
                            label="📥 Télécharger l'image",
                            data=image_data.getvalue(),
                            file_name="histoire_visualisee.png",
                            mime="image/png"
                        )
                    
                    with col2:
                        # Bouton pour générer une description
                        if st.button("🔍 Décrire l'image"):
                            # Copier image_data pour éviter les problèmes de position
                            image_data_copy = BytesIO()
                            image_data.seek(0)
                            image_data_copy.write(image_data.read())
                            image_data_copy.seek(0)
                            
                            with st.spinner("🔄 Génération de la description..."):
                                description = describe_image(client, image_data_copy)
                            
                            if description:
                                st.session_state.image_description = description
                                st.rerun()
                            else:
                                st.error("❌ Impossible de générer la description. Vérifiez votre clé API et réessayez.")
                    
                    # Afficher la description si elle existe
                    if "image_description" in st.session_state:
                        st.markdown("### 📝 Description de l'image")
                        st.markdown(st.session_state.image_description)
            
            # Si une image existe déjà dans la session, l'afficher
            elif "generated_image" in st.session_state:
                st.markdown("### 🎨 Image générée précédemment")
                st.info("Une image a déjà été générée pour cette histoire.")
                
                # Afficher l'image existante
                image = Image.open(st.session_state.generated_image)
                st.image(image, caption="Votre histoire visualisée", use_column_width=True)
                
                # Boutons d'action pour l'image existante
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Téléchargement
                    st.session_state.generated_image.seek(0)
                    st.download_button(
                        label="📥 Télécharger l'image",
                        data=st.session_state.generated_image.getvalue(),
                        file_name="histoire_visualisee.png",
                        mime="image/png"
                    )
                
                with col2:
                    # Bouton pour générer une description
                    if st.button("🔍 Décrire l'image", key="describe_existing"):
                        # Copier image_data pour éviter les problèmes de position
                        image_data_copy = BytesIO()
                        st.session_state.generated_image.seek(0)
                        image_data_copy.write(st.session_state.generated_image.read())
                        image_data_copy.seek(0)
                        
                        with st.spinner("🔄 Génération de la description..."):
                            description = describe_image(client, image_data_copy)
                        
                        if description:
                            st.session_state.image_description = description
                            st.rerun()
                        else:
                            st.error("❌ Impossible de générer la description. Vérifiez votre clé API et réessayez.")
                
                with col3:
                    # Générer une nouvelle image
                    if st.button("🔄 Générer une nouvelle image"):
                        # Supprimer l'ancienne image de la session
                        if "generated_image" in st.session_state:
                            del st.session_state["generated_image"]
                        if "image_url" in st.session_state:
                            del st.session_state["image_url"]
                        if "image_description" in st.session_state:
                            del st.session_state["image_description"]
                        st.rerun()
                
                # Afficher la description si elle existe
                if "image_description" in st.session_state:
                    st.markdown("### 📝 Description de l'image")
                    st.markdown(st.session_state.image_description)
        else:
            st.info("👈 Veuillez d'abord créer une histoire dans l'onglet 'Création d'Histoire'")
    
    with tab3:
        st.header("🖼️ Galerie de vos Créations")
        st.markdown("Visualisez vos histoires et images créées")
        
        if "generated_image" in st.session_state:
            # Afficher la création complète
            st.markdown("### 🎭 Votre Création Complète")
            
            # Histoire originale
            if "original_story" in st.session_state:
                st.markdown("**💭 Idée originale:**")
                st.markdown(st.session_state.original_story)
            
            # Histoire améliorée
            if "improved_story" in st.session_state:
                st.markdown("**📖 Histoire améliorée:**")
                st.markdown(st.session_state.improved_story)
            
            # Image générée
            st.markdown("**🎨 Image générée:**")
            image = Image.open(st.session_state.generated_image)
            st.image(image, caption="Votre histoire visualisée", use_column_width=True)
            
            # Prompt utilisé pour l'image
            if "image_prompt" in st.session_state:
                with st.expander("🎨 Prompt utilisé pour l'image"):
                    st.code(st.session_state.image_prompt)
            
            # Description de l'image si disponible
            if "image_description" in st.session_state:
                st.markdown("**🔍 Description de l'image:**")
                st.markdown(st.session_state.image_description)
            
            # Actions
            st.markdown("### 🎯 Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Téléchargement de l'image
                st.session_state.generated_image.seek(0)
                st.download_button(
                    label="📥 Télécharger l'image",
                    data=st.session_state.generated_image.getvalue(),
                    file_name="ma_creation.png",
                    mime="image/png"
                )
            
            with col2:
                # Exporter le tout en texte
                if st.button("📄 Exporter tout en texte"):
                    export_text = f"""=== MA CRÉATION ===

IDÉE ORIGINALE:
{st.session_state.get('original_story', 'Non disponible')}

HISTOIRE AMÉLIORÉE:
{st.session_state.get('improved_story', 'Non disponible')}

PROMPT POUR L'IMAGE:
{st.session_state.get('image_prompt', 'Non disponible')}

DESCRIPTION DE L'IMAGE:
{st.session_state.get('image_description', 'Non disponible')}

URL DE L'IMAGE:
{st.session_state.get('image_url', 'Non disponible')}
"""
                    st.download_button(
                        label="📄 Télécharger le texte",
                        data=export_text,
                        file_name="ma_creation_complete.txt",
                        mime="text/plain"
                    )
            
            with col3:
                # Nouvelle création
                if st.button("🔄 Nouvelle création"):
                    # Effacer la session
                    for key in ['improved_story', 'original_story', 'generated_image', 'image_url', 'image_prompt', 'image_description']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.rerun()
        
        else:
            st.info("🎨 Aucune création disponible. Créez votre première histoire dans l'onglet 'Création d'Histoire' !")
    
    with tab4:
        st.header("ℹ️ À propos du Projet")
        st.markdown("""
        ### 🎭 Générateur d'Histoires Visuelles
        
        Cette application combine plusieurs fonctionnalités d'OpenAI pour créer une expérience créative complète :
        
        #### 🛠️ Fonctionnalités utilisées :
        
        **1. 💬 Chat GPT (Amélioration d'histoires)**
        - Utilise GPT-4 pour enrichir vos idées d'histoires
        - Ajoute des détails visuels et narratifs
        - Optimise le prompt pour la génération d'images
        
        **2. 🎨 DALL-E 3 (Génération d'images)**
        - Crée des images uniques basées sur vos histoires
        - Plusieurs formats et qualités disponibles
        - Génération haute résolution
        
        **3. 👁️ Vision GPT-4 (Description d'images)**
        - Analyse et décrit les images générées
        - Fournit des descriptions détaillées et créatives
        - Complète le cycle créatif
        
        #### 🔄 Workflow :
        1. **Saisie** : Entrez votre idée d'histoire
        2. **Amélioration** : L'IA enrichit votre histoire
        3. **Visualisation** : DALL-E crée une image
        4. **Description** : L'IA décrit l'image générée
        5. **Sauvegarde** : Exportez votre création complète
        
        #### 💡 Conseils d'utilisation :
        - Soyez créatif dans vos idées initiales
        - N'hésitez pas à modifier le prompt avant génération
        - Testez différents paramètres d'image
        - Explorez les descriptions pour enrichir vos histoires
        
        #### 🎯 Cas d'usage :
        - **Créateurs de contenu** : Générer des visuels pour vos histoires
        - **Écrivains** : Visualiser vos scènes et personnages
        - **Éducateurs** : Créer du matériel pédagogique illustré
        - **Artistes** : Explorer de nouvelles idées créatives
        """)
        
        st.markdown("---")
        st.markdown("### 🔧 Technologies utilisées")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🤖 OpenAI API**
            - GPT-4 pour l'amélioration de texte
            - DALL-E 3 pour la génération d'images
            - GPT-4 Vision pour l'analyse d'images
            """)
        
        with col2:
            st.markdown("""
            **🎨 Interface**
            - Streamlit pour l'interface utilisateur
            - PIL pour le traitement d'images
            - Requests pour les téléchargements
            """)

else:
    # Message d'information si pas de clé API
    st.info("🔑 Veuillez entrer une clé API OpenAI valide pour utiliser le générateur d'histoires visuelles.")
    
    st.markdown("### 🎭 Présentation du Projet")
    st.markdown("""
    Ce **Générateur d'Histoires Visuelles** combine plusieurs technologies d'OpenAI pour créer une expérience créative unique :
    
    #### 🌟 Fonctionnalités principales :
    
    **📝 Amélioration d'histoires**
    - Entrez une idée simple
    - L'IA la transforme en histoire riche et détaillée
    - Optimisation automatique pour la génération d'images
    
    **🎨 Génération d'images**
    - Création d'images uniques avec DALL-E 3
    - Plusieurs formats et qualités
    - Basé sur votre histoire améliorée
    
    **👁️ Description d'images**
    - Analyse automatique des images générées
    - Descriptions créatives et détaillées
    - Retour narratif sur votre création
    
    **🖼️ Galerie complète**
    - Visualisation de toutes vos créations
    - Export en différents formats
    - Sauvegarde de l'ensemble du processus créatif
    
    #### 🚀 Pour commencer :
    1. Obtenez une clé API sur [platform.openai.com](https://platform.openai.com/api-keys)
    2. Entrez votre clé dans le champ ci-dessus
    3. Commencez à créer vos histoires visuelles !
    """)

# Sidebar avec informations
with st.sidebar:
    st.markdown("### 🎨 Générateur d'Histoires")
    st.markdown("""
    **Workflow créatif :**
    1. 💭 Idée originale
    2. 📝 Amélioration IA
    3. 🎨 Génération d'image
    4. 👁️ Description visuelle
    5. 🖼️ Galerie complète
    """)
    
    st.markdown("### 🛠️ Outils utilisés")
    st.markdown("""
    - **GPT-4** : Amélioration de texte
    - **DALL-E 3** : Génération d'images
    - **GPT-4 Vision** : Description d'images
    - **Streamlit** : Interface utilisateur
    """)
    
    # Statut de la connexion API
    st.markdown("### 🔌 Statut de l'API")
    if client:
        st.success("Connecté ✅")
    else:
        st.error("Non connecté ❌")
    
    # Informations sur la session
    if "improved_story" in st.session_state:
        st.markdown("### 📊 Session actuelle")
        st.success("✅ Histoire créée")
        
        if "generated_image" in st.session_state:
            st.success("✅ Image générée")
        
        if "image_description" in st.session_state:
            st.success("✅ Description créée")

# Style CSS personnalisé
st.markdown("""
<style>
    .stTextInput > div > div > input[type="password"] {
        font-family: monospace;
    }
    
    .creation-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    
    .workflow-step {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)