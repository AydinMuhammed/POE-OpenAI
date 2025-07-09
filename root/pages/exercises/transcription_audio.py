import streamlit as st
import requests
from io import BytesIO
from openai import OpenAI
import tempfile
import os

# Configuration de la page
st.set_page_config(
    page_title="Traitement Audio OpenAI",
    page_icon="🎵",
    layout="wide"
)

# Titre de la page
st.title("🎵 Traitement Audio avec OpenAI")
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

def openai_transcribe(client, audio_file):
    """
    Transcrit un fichier audio en texte
    
    Args:
        client: Client OpenAI initialisé
        audio_file: Fichier audio à transcrire
    
    Returns:
        str: Transcription du fichier audio
    """
    try:
        # Créer un fichier temporaire pour l'audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name
        
        # Ouvrir le fichier pour la transcription
        with open(tmp_file_path, "rb") as audio:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_file_path)
        
        return transcript.text
        
    except Exception as e:
        # Nettoyer le fichier temporaire en cas d'erreur
        if 'tmp_file_path' in locals():
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        st.error(f"❌ Erreur lors de la transcription: {str(e)}")
        return None

def openai_translate(client, audio_file, target_language="français"):
    """
    Traduit un fichier audio en texte dans une langue cible
    
    Args:
        client: Client OpenAI initialisé
        audio_file: Fichier audio à traduire
        target_language: Langue cible pour la traduction
    
    Returns:
        str: Traduction du fichier audio
    """
    try:
        # Créer un fichier temporaire pour l'audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_file_path = tmp_file.name
        
        # Ouvrir le fichier pour la traduction
        with open(tmp_file_path, "rb") as audio:
            translation = client.audio.translations.create(
                model="whisper-1",
                file=audio
            )
        
        # Nettoyer le fichier temporaire
        os.unlink(tmp_file_path)
        
        # Si on veut une autre langue que l'anglais, utiliser GPT pour traduire
        if target_language.lower() != "english" and target_language.lower() != "anglais":
            chat_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Tu es un traducteur expert. Traduis le texte suivant en {target_language}."},
                    {"role": "user", "content": translation.text}
                ],
                max_tokens=1000
            )
            return chat_response.choices[0].message.content
        
        return translation.text
        
    except Exception as e:
        # Nettoyer le fichier temporaire en cas d'erreur
        if 'tmp_file_path' in locals():
            try:
                os.unlink(tmp_file_path)
            except:
                pass
        st.error(f"❌ Erreur lors de la traduction: {str(e)}")
        return None

def text_to_speech(client, text, voice="alloy", model="tts-1"):
    """
    Convertit un texte en fichier audio
    
    Args:
        client: Client OpenAI initialisé
        text: Texte à convertir en audio
        voice: Voix à utiliser (alloy, echo, fable, onyx, nova, shimmer)
        model: Modèle TTS à utiliser (tts-1 ou tts-1-hd)
    
    Returns:
        bytes: Données audio générées
    """
    try:
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )
        
        return response.content
        
    except Exception as e:
        st.error(f"❌ Erreur lors de la génération audio: {str(e)}")
        return None

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
    tab1, tab2, tab3, tab4 = st.tabs(["🎤 Transcription", "🌍 Traduction Audio", "🔊 Text-to-Speech", "ℹ️ Informations"])

    with tab1:
        st.header("🎤 Transcription Audio")
        st.markdown("Convertissez vos fichiers audio en texte avec Whisper d'OpenAI")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Upload Audio")
            
            # Upload de fichier audio
            audio_file = st.file_uploader(
                "Choisissez un fichier audio à transcrire",
                type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
                help="Formats supportés: MP3, WAV, M4A, OGG, FLAC"
            )
            
            if audio_file:
                st.audio(audio_file, format='audio/mp3')
                st.info(f"Fichier: {audio_file.name} ({audio_file.size} bytes)")
        
        with col2:
            st.subheader("📝 Transcription")
            
            if audio_file:
                if st.button("🚀 Transcrire", key="transcribe", type="primary"):
                    audio_file.seek(0)  # Reset file pointer
                    with st.spinner("🔄 Transcription en cours..."):
                        transcription = openai_transcribe(client, audio_file)
                    
                    if transcription:
                        st.success("✅ Transcription terminée !")
                        st.markdown("### 📋 Résultat")
                        st.text_area("Transcription:", value=transcription, height=200, disabled=True)
                        
                        # Bouton de téléchargement
                        st.download_button(
                            label="📥 Télécharger la transcription",
                            data=transcription,
                            file_name="transcription.txt",
                            mime="text/plain"
                        )
            else:
                st.info("👆 Veuillez d'abord uploader un fichier audio")

    with tab2:
        st.header("🌍 Traduction Audio")
        st.markdown("Traduisez vos fichiers audio dans différentes langues")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📤 Upload Audio")
            
            # Upload de fichier audio pour traduction
            audio_file_translate = st.file_uploader(
                "Choisissez un fichier audio à traduire",
                type=['mp3', 'wav', 'm4a', 'ogg', 'flac'],
                help="Formats supportés: MP3, WAV, M4A, OGG, FLAC",
                key="translate_uploader"
            )
            
            if audio_file_translate:
                st.audio(audio_file_translate, format='audio/mp3')
                st.info(f"Fichier: {audio_file_translate.name} ({audio_file_translate.size} bytes)")
        
        with col2:
            st.subheader("🔄 Traduction")
            
            if audio_file_translate:
                # Choix de la langue cible
                target_lang = st.selectbox(
                    "Langue cible:",
                    ["français", "english", "español", "deutsch", "italiano", "português", "русский", "中文", "日本語"],
                    help="Choisissez la langue de traduction"
                )
                
                if st.button("🚀 Traduire", key="translate", type="primary"):
                    audio_file_translate.seek(0)  # Reset file pointer
                    with st.spinner("🔄 Traduction en cours..."):
                        translation = openai_translate(client, audio_file_translate, target_lang)
                    
                    if translation:
                        st.success("✅ Traduction terminée !")
                        st.markdown("### 📋 Résultat")
                        st.text_area("Traduction:", value=translation, height=200, disabled=True)
                        
                        # Bouton de téléchargement
                        st.download_button(
                            label="📥 Télécharger la traduction",
                            data=translation,
                            file_name=f"traduction_{target_lang}.txt",
                            mime="text/plain"
                        )
            else:
                st.info("👆 Veuillez d'abord uploader un fichier audio")

    with tab3:
        st.header("🔊 Text-to-Speech")
        st.markdown("Convertissez votre texte en audio avec les voix d'OpenAI")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Texte à convertir")
            
            # Zone de texte
            text_input = st.text_area(
                "Entrez le texte à convertir en audio:",
                placeholder="Tapez ou collez votre texte ici...",
                height=200
            )
            
            # Paramètres de génération
            st.subheader("⚙️ Paramètres")
            
            voice = st.selectbox(
                "Voix:",
                ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
                help="Choisissez la voix pour la génération audio"
            )
            
            model = st.selectbox(
                "Qualité:",
                ["tts-1", "tts-1-hd"],
                format_func=lambda x: "Standard (tts-1)" if x == "tts-1" else "Haute qualité (tts-1-hd)"
            )
        
        with col2:
            st.subheader("🎵 Génération Audio")
            
            if text_input.strip():
                if st.button("🚀 Générer l'audio", key="tts", type="primary"):
                    with st.spinner("🔄 Génération audio en cours..."):
                        audio_data = text_to_speech(client, text_input, voice, model)
                    
                    if audio_data:
                        st.success("✅ Audio généré !")
                        
                        # Lecture audio
                        st.audio(audio_data, format='audio/mp3')
                        
                        # Bouton de téléchargement
                        st.download_button(
                            label="📥 Télécharger l'audio",
                            data=audio_data,
                            file_name=f"audio_{voice}.mp3",
                            mime="audio/mp3"
                        )
                        
                        # Informations
                        st.info(f"🎵 Voix utilisée: {voice} | Modèle: {model}")
            else:
                st.info("👆 Veuillez d'abord entrer un texte")

    with tab4:
        st.header("ℹ️ Informations sur le Traitement Audio")
        
        st.markdown("""
        ### 🤖 Technologies utilisées
        
        **🎤 Whisper (Transcription & Traduction)**
        - Modèle de reconnaissance vocale d'OpenAI
        - Support de 99+ langues
        - Haute précision de transcription
        
        **🔊 Text-to-Speech (TTS)**
        - Génération audio haute qualité
        - 6 voix différentes disponibles
        - 2 niveaux de qualité
        
        ### 📋 Formats audio supportés
        
        **📤 Upload (Transcription/Traduction)**
        - MP3, WAV, M4A, OGG, FLAC
        - Taille maximale recommandée: 25MB
        
        **📥 Génération (TTS)**
        - Format de sortie: MP3
        - Qualité configurable
        
        ### 🎵 Voix disponibles (TTS)
        
        - **alloy** - Voix équilibrée et naturelle
        - **echo** - Voix masculine claire
        - **fable** - Voix expressive
        - **onyx** - Voix masculine profonde
        - **nova** - Voix féminine jeune
        - **shimmer** - Voix féminine douce
        
        ### 🌍 Langues supportées
        
        **Transcription & Traduction:**
        - Plus de 99 langues
        - Détection automatique de la langue source
        - Traduction vers le français, anglais, espagnol, etc.
        
        ### 💡 Conseils d'utilisation
        
        **📤 Pour de meilleurs résultats:**
        - Utilisez des fichiers audio de bonne qualité
        - Évitez les bruits de fond excessifs
        - Parlez clairement et distinctement
        
        **🔊 Pour Text-to-Speech:**
        - Limitez le texte à 4096 caractères max
        - Utilisez une ponctuation appropriée
        - Testez différentes voix pour trouver celle qui convient
        """)

else:
    # Message d'information si pas de clé API
    st.info("🔑 Veuillez entrer une clé API OpenAI valide pour utiliser le traitement audio.")
    
    st.markdown("### 📋 Instructions d'utilisation")
    st.markdown("""
    1. **Obtenez une clé API** sur [platform.openai.com](https://platform.openai.com/api-keys)
    2. **Entrez votre clé** dans le champ ci-dessus
    3. **Attendez la validation** (vérification automatique)
    4. **Choisissez une fonctionnalité** dans les onglets
    5. **Uploadez un fichier audio** ou entrez du texte selon la fonctionnalité
    
    ⚠️ **Note de sécurité:** Votre clé API n'est pas stockée et reste privée à votre session.
    """)

# Sidebar avec informations
with st.sidebar:
    st.markdown("### 🎵 Audio AI")
    st.markdown("""
    **Fonctionnalités:**
    - 🎤 Transcription audio
    - 🌍 Traduction multilingue
    - 🔊 Text-to-Speech
    - 📥 Téléchargement des résultats
    """)
    
    st.markdown("### ⚡ Avantages")
    st.markdown("""
    - Précision élevée
    - 99+ langues supportées
    - 6 voix TTS différentes
    - Interface intuitive
    - Traitement rapide
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
    
    .audio-info {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)
