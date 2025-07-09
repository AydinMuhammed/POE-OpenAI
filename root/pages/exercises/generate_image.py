import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI

# Configuration de la page
st.set_page_config(
    page_title="Générateur d'Images DALL-E",
    page_icon="🎨",
    layout="wide"
)

# Titre de la page
st.title("🎨 Générateur d'Images DALL-E Avancé")
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

def openai_create_image(client, prompt: str):
    """Génère une image avec DALL-E à partir d'un prompt textuel"""
    try:
        # Appel à l'API DALL-E avec la nouvelle syntaxe
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        
        # Récupération de l'URL de l'image générée
        image_url = response.data[0].url
        
        # Téléchargement de l'image depuis l'URL
        image_response = requests.get(image_url)
        
        # Conversion de l'image en format PIL
        image = Image.open(BytesIO(image_response.content))
        
        return image
        
    except Exception as e:
        st.error(f"Erreur lors de la génération de l'image: {str(e)}")
        return None

def openai_create_image_variation(client, image_file, prompt: str = ""):
    """Crée une variante d'une image existante en fonction d'un prompt"""
    try:
        # Si pas de prompt, utiliser l'API de variation classique
        if not prompt or prompt.strip() == "":
            return create_simple_variation(client, image_file)
        
        # Avec prompt: utiliser l'API d'édition d'images
        return create_variation_with_prompt(client, image_file, prompt)
        
    except Exception as e:
        st.error(f"Erreur lors de la création de la variante: {str(e)}")
        return None

def create_simple_variation(client, image_file):
    """Crée une variation simple sans prompt"""
    try:
        # Conversion de l'image en format requis pour l'API
        if hasattr(image_file, 'read'):
            # Si c'est un fichier uploadé par Streamlit
            image_file.seek(0)  # Réinitialiser le pointeur du fichier
            image = Image.open(image_file)
        else:
            # Si c'est déjà une image PIL
            image = image_file
        
        # Conversion en RGBA si nécessaire, puis en RGB
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionner l'image si nécessaire
        valid_sizes = [(256, 256), (512, 512), (1024, 1024)]
        current_size = image.size
        
        if current_size not in valid_sizes:
            if max(current_size) <= 256:
                target_size = (256, 256)
            elif max(current_size) <= 512:
                target_size = (512, 512)
            else:
                target_size = (1024, 1024)
            
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            new_image = Image.new('RGB', target_size, (255, 255, 255))
            paste_x = (target_size[0] - image.size[0]) // 2
            paste_y = (target_size[1] - image.size[1]) // 2
            new_image.paste(image, (paste_x, paste_y))
            image = new_image
        
        # Convertir en bytes PNG avec type MIME correct
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Vérifier la taille du fichier
        if len(img_buffer.getvalue()) > 4 * 1024 * 1024:
            st.error("❌ L'image est trop volumineuse. Elle doit faire moins de 4MB.")
            return None
        
        # Créer un fichier avec le bon type MIME pour l'API
        image_file_for_api = BytesIO(img_buffer.getvalue())
        image_file_for_api.name = 'image.png'  # Spécifier le nom avec extension PNG
        
        # Appel à l'API de variation
        response = client.images.create_variation(
            image=image_file_for_api,
            n=1,
            size=f"{image.size[0]}x{image.size[1]}"
        )
        
        # Récupération de l'URL de la variante
        variation_url = response.data[0].url
        variation_response = requests.get(variation_url)
        variation_image = Image.open(BytesIO(variation_response.content))
        
        return variation_image
        
    except Exception as e:
        st.error(f"Erreur lors de la création de la variation simple: {str(e)}")
        return None

def create_variation_with_prompt(client, image_file, prompt: str):
    """Crée une variation avec prompt en utilisant l'API d'édition"""
    try:
        # Conversion de l'image en format requis
        if hasattr(image_file, 'read'):
            image_file.seek(0)
            image = Image.open(image_file)
        else:
            image = image_file
        
        # Conversion en RGBA si nécessaire, puis en RGB
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[-1])
            else:
                background.paste(image)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionner si nécessaire
        valid_sizes = [(256, 256), (512, 512), (1024, 1024)]
        current_size = image.size
        
        if current_size not in valid_sizes:
            if max(current_size) <= 256:
                target_size = (256, 256)
            elif max(current_size) <= 512:
                target_size = (512, 512)
            else:
                target_size = (1024, 1024)
            
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            new_image = Image.new('RGB', target_size, (255, 255, 255))
            paste_x = (target_size[0] - image.size[0]) // 2
            paste_y = (target_size[1] - image.size[1]) // 2
            new_image.paste(image, (paste_x, paste_y))
            image = new_image
        
        # Créer un masque transparent (pour édition globale)
        mask = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        # Convertir en bytes avec type MIME correct
        img_buffer = BytesIO()
        image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        mask_buffer = BytesIO()
        mask.save(mask_buffer, format='PNG')
        mask_buffer.seek(0)
        
        # Vérifier la taille
        if len(img_buffer.getvalue()) > 4 * 1024 * 1024:
            st.error("❌ L'image est trop volumineuse.")
            return None
        
        # Créer un fichier avec le bon type MIME
        image_file_for_api = BytesIO(img_buffer.getvalue())
        image_file_for_api.name = 'image.png'  # Spécifier le nom avec extension
        
        mask_file_for_api = BytesIO(mask_buffer.getvalue())
        mask_file_for_api.name = 'mask.png'  # Spécifier le nom avec extension
        
        # Utiliser l'API d'édition avec un prompt
        response = client.images.edit(
            image=image_file_for_api,
            mask=mask_file_for_api,
            prompt=f"Transform this image: {prompt}",
            n=1,
            size=f"{image.size[0]}x{image.size[1]}"
        )
        
        # Récupération de l'URLs
        edited_url = response.data[0].url
        edited_response = requests.get(edited_url)
        edited_image = Image.open(BytesIO(edited_response.content))
        
        return edited_image
        
    except Exception as e:
        # Si l'édition ne fonctionne pas, fallback vers une nouvelle génération
        st.warning(f"⚠️ Édition impossible: {str(e)}")
        st.info("🔄 Génération d'une nouvelle image basée sur le prompt...")
        
        # Créer un prompt enrichi basé sur l'image existante
        enhanced_prompt = f"Create an image inspired by the uploaded image with these modifications: {prompt}"
        
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                n=1,
                size="1024x1024"
            )
            
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            generated_image = Image.open(BytesIO(image_response.content))
            
            return generated_image
            
        except Exception as e2:
            st.error(f"❌ Erreur lors de la génération alternative: {str(e2)}")
            return None

def generate_prompt_with_chatgpt(client, user_text: str):
    """Génère un prompt amélioré pour DALL-E en utilisant ChatGPT"""
    try:
        # Prompt système pour optimiser la génération
        system_prompt = """Tu es un expert en génération de prompts pour DALL-E. 
        Ton rôle est de transformer un texte simple en un prompt détaillé et créatif pour générer une image de haute qualité.
        
        Règles importantes:
        - Ajoute des détails visuels spécifiques
        - Mentionne le style artistique
        - Décris l'éclairage et l'ambiance
        - Précise les couleurs et la composition
        - Limite-toi à 1000 caractères maximum
        - Réponds uniquement avec le prompt amélioré, sans explication"""
        
        # Appel à l'API ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Améliore ce texte en prompt pour DALL-E: {user_text}"}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        # Récupération du prompt amélioré
        enhanced_prompt = response.choices[0].message.content.strip()
        
        return enhanced_prompt
        
    except Exception as e:
        st.error(f"Erreur lors de la génération du prompt: {str(e)}")
        return user_text  # Retourne le texte original en cas d'erreur

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
    tab1, tab2, tab3 = st.tabs(["🎨 Génération", "🔄 Variations", "✨ Prompt Amélioré"])

    with tab1:
        st.header("Génération d'image classique")
        
        prompt = st.text_input("Décrivez l'image que vous voulez générer:")
        
        if st.button("Générer l'image", key="generate"):
            if prompt:
                with st.spinner("Génération en cours..."):
                    image = openai_create_image(client, prompt)
                
                if image:
                    st.image(image, caption=f"Image générée: {prompt}")
                    
                    # Sauvegarder l'image dans la session pour les variations
                    st.session_state.generated_image = image
                    st.success("Image générée avec succès ! Vous pouvez maintenant créer des variations dans l'onglet 'Variations'.")
            else:
                st.warning("Veuillez entrer une description.")

    with tab2:
        st.header("Créer des variations d'image")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Image source")
            
            # Option 1: Utiliser l'image générée précédemment
            if 'generated_image' in st.session_state:
                if st.button("Utiliser l'image générée précédemment"):
                    st.session_state.variation_source = st.session_state.generated_image
                    st.image(st.session_state.generated_image, caption="Image sélectionnée")
            
            # Option 2: Uploader une nouvelle image
            uploaded_file = st.file_uploader(
                "Ou uploadez une image (PNG uniquement)", 
                type=['png'],
                help="L'image doit être au format PNG et faire moins de 4MB pour que la variation fonctionne correctement"
            )
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Image uploadée")
                st.session_state.variation_source = uploaded_file
        
        with col2:
            st.subheader("Créer une variation")
            
            if 'variation_source' in st.session_state:
                variation_prompt = st.text_area(
                    "Prompt pour la variation (optionnel):",
                    placeholder="Ex: make it more colorful, add a sunset background, change the style to watercolor...",
                    help="Décrivez les modifications souhaitées. Laissez vide pour une variation créative libre.",
                    height=100
                )
                
                # Options avancées
                with st.expander("⚙️ Options de variation"):
                    variation_type = st.radio(
                        "Type de variation:",
                        ["Variation libre (sans prompt)", "Variation avec prompt", "Génération inspirée"],
                        help="""
                        - Variation libre: Crée une version similaire sans modifications spécifiques
                        - Variation avec prompt: Tente d'appliquer vos modifications (expérimental)
                        - Génération inspirée: Crée une nouvelle image basée sur la vôtre et le prompt
                        """
                    )
                
                if st.button("Créer une variation", key="variation"):
                    with st.spinner("Création de la variation..."):
                        if variation_type == "Variation libre (sans prompt)":
                            variation = create_simple_variation(client, st.session_state.variation_source)
                        elif variation_type == "Génération inspirée":
                            if variation_prompt:
                                enhanced_prompt = f"Create an image inspired by the uploaded image with these characteristics: {variation_prompt}"
                                variation = openai_create_image(client, enhanced_prompt)
                            else:
                                variation = create_simple_variation(client, st.session_state.variation_source)
                        else:  # Variation avec prompt
                            variation = openai_create_image_variation(
                                client,
                                st.session_state.variation_source, 
                                variation_prompt
                            )
                    
                    if variation:
                        st.image(variation, caption="Variation créée")
                        
                        # Sauvegarder la variation
                        st.session_state.generated_image = variation
                        st.success("Variation créée ! Vous pouvez créer d'autres variations à partir de cette image.")
            else:
                st.info("Sélectionnez d'abord une image source")
        
        # Informations sur les variations
        with st.expander("ℹ️ À propos des variations"):
            st.markdown("""
            **Types de variations disponibles :**
            
            **🎨 Variation libre**
            - Crée des images similaires avec des différences créatives
            - Conserve le style et la composition générale
            - Aucun prompt requis
            
            **✏️ Variation avec prompt**
            - Tente d'appliquer vos modifications à l'image
            - Utilise l'API d'édition quand possible
            - Peut avoir des résultats variables
            
            **🚀 Génération inspirée**
            - Crée une nouvelle image basée sur la vôtre
            - Combine l'inspiration visuelle avec votre prompt
            - Résultats plus prévisibles
            
            **Limitations :**
            - Tailles: 256x256, 512x512, 1024x1024
            - Formats: PNG uniquement (pour les uploads)
            - Taille max: 4MB
            
            **⚠️ Important :** Pour uploader une image et créer des variations, utilisez uniquement le format PNG. Les autres formats peuvent causer des erreurs.
            """)

    with tab3:
        st.header("Génération avec prompt amélioré")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Texte simple")
            user_text = st.text_area(
                "Décrivez simplement ce que vous voulez:",
                placeholder="Exemple: un chat dans un jardin",
                height=100
            )
            
            if st.button("Améliorer le prompt", key="enhance"):
                if user_text:
                    with st.spinner("Amélioration du prompt..."):
                        enhanced_prompt = generate_prompt_with_chatgpt(client, user_text)
                    
                    st.session_state.enhanced_prompt = enhanced_prompt
                    st.success("Prompt amélioré généré !")
                else:
                    st.warning("Veuillez entrer un texte à améliorer.")
        
        with col2:
            st.subheader("Prompt amélioré")
            
            if 'enhanced_prompt' in st.session_state:
                enhanced_prompt = st.text_area(
                    "Prompt amélioré (vous pouvez le modifier):",
                    value=st.session_state.enhanced_prompt,
                    height=100
                )
                
                if st.button("Générer avec le prompt amélioré", key="generate_enhanced"):
                    with st.spinner("Génération avec prompt amélioré..."):
                        image = openai_create_image(client, enhanced_prompt)
                    
                    if image:
                        st.image(image, caption="Image générée avec prompt amélioré")
                        
                        # Comparaison
                        st.markdown("---")
                        st.markdown("**Comparaison:**")
                        col_orig, col_enh = st.columns(2)
                        with col_orig:
                            st.text_area("Texte original:", value=user_text, height=60, disabled=True)
                        with col_enh:
                            st.text_area("Prompt amélioré:", value=enhanced_prompt, height=60, disabled=True)
            else:
                st.info("Générez d'abord un prompt amélioré dans la colonne de gauche")

else:
    # Message d'information si pas de clé API
    st.info("🔑 Veuillez entrer une clé API OpenAI valide pour utiliser le générateur d'images.")
    
    st.markdown("### 📋 Instructions d'utilisation")
    st.markdown("""
    1. **Obtenez une clé API** sur [platform.openai.com](https://platform.openai.com/api-keys)
    2. **Entrez votre clé** dans le champ ci-dessus
    3. **Attendez la validation** (vérification automatique)
    4. **Commencez à générer** vos images avec DALL-E
    
    ⚠️ **Note de sécurité:** Votre clé API n'est pas stockée et reste privée à votre session.
    """)

# Sidebar avec informations
with st.sidebar:
    st.markdown("### ℹ️ Fonctionnalités")
    st.markdown("""
    **🎨 Génération classique**
    - Créez des images à partir de prompts
    
    **🔄 Variations d'image**
    - Créez des variations d'images existantes
    - Utilisez vos images générées ou uploadées
    
    **✨ Prompt amélioré**
    - Laissez ChatGPT améliorer vos descriptions
    - Obtenez des résultats plus détaillés
    """)
    
    st.markdown("### 💡 Conseils")
    st.markdown("""
    - Soyez spécifique dans vos descriptions
    - Mentionnez le style artistique
    - Décrivez l'éclairage et les couleurs
    - Utilisez des mots-clés visuels
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
</style>
""", unsafe_allow_html=True)