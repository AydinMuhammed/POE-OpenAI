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

# Configuration sécurisée de l'API OpenAI
def initialize_openai_client():
    """Initialise le client OpenAI de manière sécurisée"""
    try:
        # Récupération de la clé API depuis les secrets Streamlit
        api_key = st.secrets.get("OPENAI_API_KEY")
        
        if not api_key:
            st.error("❌ Clé API OpenAI non trouvée dans les secrets Streamlit")
            st.stop()
        
        # Initialisation du client OpenAI
        client = OpenAI(api_key=api_key)
        return client
    
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation du client OpenAI: {str(e)}")
        st.stop()

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

# Initialisation du client OpenAI
client = initialize_openai_client()

# Initialisation de l'état de session pour l'historique
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

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

# Sidebar avec informations
with st.sidebar:
    st.markdown("### ℹ️ Informations")
    st.markdown("""
    **Modèle:** GPT-3.5-turbo
    
    **Fonctionnalités:**
    - 💬 Conversation en temps réel
    - 🧠 Mémoire de conversation
    - 🔒 Sécurisation des clés API
    - 🗑️ Effacement de l'historique
    
    **Utilisation:**
    1. Tapez votre question dans le champ de saisie
    2. Appuyez sur Entrée ou cliquez sur envoyer
    3. L'assistant vous répondra instantanément
    """)
    
    # Statistiques de la conversation
    if st.session_state.messages:
        st.markdown("### 📊 Statistiques")
        user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
        assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        
        st.metric("Messages utilisateur", user_messages)
        st.metric("Réponses assistant", assistant_messages)

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
</style>
""", unsafe_allow_html=True)