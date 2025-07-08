import streamlit as st
import os
from openai import OpenAI

# Configuration de la page
st.set_page_config(
    page_title="Chatbot OpenAI",
    page_icon="🤖",
    layout="wide"
)

# Titre de la page
st.title("🤖 Chatbot OpenAI")
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

# Fonction pour envoyer une requête au chatbot
def get_chatbot_response(client, user_input, conversation_history):
    """Génère une réponse du chatbot"""
    try:
        # Préparation des messages avec l'historique
        messages = [
            {"role": "system", "content": "Tu es un assistant IA serviable et amical. Réponds de manière claire et concise."}
        ]
        
        # Ajout de l'historique de conversation
        for message in conversation_history:
            messages.append(message)
        
        # Ajout du nouveau message utilisateur
        messages.append({"role": "user", "content": user_input})
        
        # Appel à l'API OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ Erreur lors de la génération de la réponse: {str(e)}"

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

# Initialisation de l'état de session pour l'historique
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# Interface du chatbot (seulement si la clé API est valide)
if client:
    st.markdown("---")
    
    # Interface utilisateur
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("💬 Conversation")

    with col2:
        if st.button("🗑️ Effacer la conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.rerun()

    # Affichage de l'historique des messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Zone de saisie utilisateur
    user_input = st.chat_input("Tapez votre message ici...")

    if user_input:
        # Ajout du message utilisateur à l'affichage
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Affichage du message utilisateur
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Génération et affichage de la réponse
        with st.chat_message("assistant"):
            with st.spinner("🤔 Réflexion en cours..."):
                response = get_chatbot_response(client, user_input, st.session_state.conversation_history)
            
            st.markdown(response)
        
        # Ajout des messages à l'historique
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    # Message d'information si pas de clé API
    st.info("🔑 Veuillez entrer une clé API OpenAI valide pour utiliser le chatbot.")
    
    st.markdown("### 📋 Instructions d'utilisation")
    st.markdown("""
    1. **Obtenez une clé API** sur [platform.openai.com](https://platform.openai.com/api-keys)
    2. **Entrez votre clé** dans le champ ci-dessus
    3. **Attendez la validation** (vérification automatique)
    4. **Commencez à chatter** avec l'assistant IA
    
    ⚠️ **Note de sécurité:** Votre clé API n'est pas stockée et reste privée à votre session.
    """)

# Sidebar avec informations
with st.sidebar:
    st.markdown("### ℹ️ Informations")
    st.markdown("""
    **Modèle:** GPT-3.5-turbo
    
    **Fonctionnalités:**
    - 💬 Conversation en temps réel
    - 🧠 Mémoire de conversation
    - 🔑 Saisie sécurisée de clé API
    - 🗑️ Effacement de l'historique
    
    **Sécurité:**
    - Clé API non stockée
    - Validation automatique
    - Session privée
    """)
    
    # Statistiques de la conversation
    if st.session_state.messages:
        st.markdown("### 📊 Statistiques")
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.metric("Messages utilisateur", user_messages)
        st.metric("Réponses assistant", assistant_messages)
    
    # Statut de la connexion API
    st.markdown("### 🔌 Statut de l'API")
    if client:
        st.success("Connecté ✅")
    else:
        st.error("Non connecté ❌")

# Style CSS personnalisé
st.markdown("""
<style>
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    
    .stChatInputContainer {
        border-top: 2px solid #e6e9ef;
        padding-top: 20px;
    }
    
    .stTextInput > div > div > input[type="password"] {
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)