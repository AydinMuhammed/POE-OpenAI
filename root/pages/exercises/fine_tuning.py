import streamlit as st
import openai
import json
import time
from datetime import datetime

#A L'aide de ChatGPT, créez un fichier de données d'entrainement au format JSONL contenant au moins 10 messages puis placez le dans un fichier data.jsonl Entrainez ensuite un modèle de chatbot sur un domaine de votre choix.

def create_sample_jsonl(filename="data.jsonl"):
    messages = [
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Quel temps fait-il à Paris ?"},
            {"role": "assistant", "content": "Aujourd'hui à Paris, il fait ensoleillé avec 25°C."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Va-t-il pleuvoir demain à Lyon ?"},
            {"role": "assistant", "content": "Demain à Lyon, des averses sont prévues dans l'après-midi."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Quelle est la température à Marseille ?"},
            {"role": "assistant", "content": "Il fait actuellement 28°C à Marseille."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Y a-t-il du vent à Lille ?"},
            {"role": "assistant", "content": "Oui, il y a un vent modéré de 20 km/h à Lille."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Quel temps pour le week-end à Bordeaux ?"},
            {"role": "assistant", "content": "Le week-end sera nuageux avec quelques éclaircies à Bordeaux."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Est-ce qu'il neige à Grenoble ?"},
            {"role": "assistant", "content": "Non, il ne neige pas actuellement à Grenoble."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Peux-tu me donner la météo à Nice ?"},
            {"role": "assistant", "content": "À Nice, il fait beau et chaud avec 30°C."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Quel est le taux d'humidité à Nantes ?"},
            {"role": "assistant", "content": "Le taux d'humidité à Nantes est de 60%."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Va-t-il faire chaud à Toulouse cette semaine ?"},
            {"role": "assistant", "content": "Oui, des températures élevées sont attendues à Toulouse cette semaine."}
        ]},
        {"messages": [
            {"role": "system", "content": "Tu es un assistant expert en météo."},
            {"role": "user", "content": "Quel temps fait-il à Strasbourg ?"},
            {"role": "assistant", "content": "À Strasbourg, le ciel est partiellement couvert avec 22°C."}
        ]}
    ]
    with open(filename, "w", encoding="utf-8") as f:
        for m in messages:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

#Créez une méthode openai_chat_finetune() qui prend en paramètre le nom du fichier de données d'entrainement et retourne le nom du modèle entrainé.
def openai_chat_finetune(training_file):
    # Nécessite openai.api_key déjà défini
    with open(training_file, "rb") as f:
        file_response = openai.files.create(file=f, purpose="fine-tune")
    file_id = file_response.id
    fine_tune_response = openai.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo"
    )
    return fine_tune_response.id

def get_job_status(job_id):
    """Récupère le statut d'un job de fine-tuning"""
    try:
        job = openai.fine_tuning.jobs.retrieve(job_id)
        return job
    except Exception as e:
        st.error(f"Erreur lors de la récupération du statut: {str(e)}")
        return None

def get_job_events(job_id, limit=10):
    """Récupère les événements d'un job de fine-tuning"""
    try:
        events = openai.fine_tuning.jobs.list_events(id=job_id, limit=limit)
        return events.data
    except Exception as e:
        st.error(f"Erreur lors de la récupération des événements: {str(e)}")
        return []

def chat_with_model(model_id, messages, temperature=0.7):
    """Interagit avec un modèle fine-tuné"""
    try:
        response = openai.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erreur lors de l'interaction avec le modèle: {str(e)}")
        return None

# Configuration de la page
st.set_page_config(
    page_title="Fine-tuning OpenAI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Fine-tuning Chatbot OpenAI")
st.markdown("---")

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

if api_key:
    openai.api_key = api_key
    st.success("✅ Clé API configurée")

    # Onglets pour différentes fonctionnalités
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Création des données", "🚀 Fine-tuning", "🔍 Suivi des jobs", "💬 Tester le modèle"])

    with tab1:
        st.header("📊 Création des données d'entraînement")
        st.markdown("Créez un fichier JSONL contenant les exemples pour entraîner votre chatbot")
        
        # Options pour créer des données
        data_option = st.radio(
            "Comment souhaitez-vous créer vos données ?",
            ["Utiliser l'exemple prédéfini (météo)", "Créer un exemple personnalisé"]
        )
        
        if data_option == "Utiliser l'exemple prédéfini (météo)":
            if st.button("📥 Générer le fichier data.jsonl", type="primary"):
                create_sample_jsonl()
                st.success("✅ Fichier data.jsonl créé avec 10 exemples de météo !")
                
                # Afficher un aperçu
                with open("data.jsonl", "r", encoding="utf-8") as f:
                    lines = f.readlines()[:3]  # Afficher les 3 premiers exemples
                
                st.markdown("### Aperçu des données")
                for i, line in enumerate(lines):
                    st.code(line, language="json")
                    if i < len(lines) - 1:
                        st.markdown("---")
                
                st.info(f"📁 Le fichier contient {len(open('data.jsonl', 'r', encoding='utf-8').readlines())} exemples au total.")
        else:
            st.markdown("### Création d'exemples personnalisés")
            
            domain = st.text_input("Domaine d'expertise du chatbot", 
                                  placeholder="Ex: assistant culinaire, expert juridique, etc.")
            
            st.markdown("#### Exemple d'échange (minimum 10 requis)")
            
            col1, col2 = st.columns(2)
            with col1:
                user_input = st.text_area("Question utilisateur", placeholder="Ex: Comment faire une pâte à crêpes ?")
            with col2:
                assistant_output = st.text_area("Réponse assistant", placeholder="Ex: Pour faire une pâte à crêpes, mélangez 250g de farine...")
            
            if st.button("➕ Ajouter cet exemple"):
                if not domain or not user_input or not assistant_output:
                    st.warning("⚠️ Veuillez remplir tous les champs")
                else:
                    # Créer ou charger le fichier JSONL
                    try:
                        examples = []
                        try:
                            with open("custom_data.jsonl", "r", encoding="utf-8") as f:
                                for line in f:
                                    examples.append(json.loads(line))
                        except FileNotFoundError:
                            pass  # Le fichier n'existe pas encore
                        
                        # Ajouter le nouvel exemple
                        examples.append({
                            "messages": [
                                {"role": "system", "content": f"Tu es un assistant expert en {domain}."},
                                {"role": "user", "content": user_input},
                                {"role": "assistant", "content": assistant_output}
                            ]
                        })
                        
                        # Sauvegarder
                        with open("custom_data.jsonl", "w", encoding="utf-8") as f:
                            for example in examples:
                                f.write(json.dumps(example, ensure_ascii=False) + "\n")
                        
                        st.success(f"✅ Exemple ajouté! ({len(examples)} exemples au total)")
                    except Exception as e:
                        st.error(f"Erreur: {str(e)}")
            
            # Afficher les exemples existants
            try:
                with open("custom_data.jsonl", "r", encoding="utf-8") as f:
                    examples = [json.loads(line) for line in f]
                
                if examples:
                    st.markdown(f"### Exemples enregistrés ({len(examples)})")
                    
                    if st.checkbox("Voir tous les exemples"):
                        for i, ex in enumerate(examples):
                            with st.expander(f"Exemple {i+1}"):
                                st.markdown(f"**Système:** {ex['messages'][0]['content']}")
                                st.markdown(f"**Utilisateur:** {ex['messages'][1]['content']}")
                                st.markdown(f"**Assistant:** {ex['messages'][2]['content']}")
            except FileNotFoundError:
                st.info("Aucun exemple personnalisé enregistré pour le moment.")

    with tab2:
        st.header("🚀 Lancement du Fine-tuning")
        st.markdown("Lancez l'entraînement de votre modèle sur les données préparées")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sélection du fichier
            training_file = st.text_input("Nom du fichier d'entraînement", 
                                        value="data.jsonl" if "data.jsonl" in [f.split("/")[-1] for f in ["data.jsonl"]] else "",
                                        placeholder="Ex: data.jsonl")
            
            # Sélection du modèle de base
            base_model = st.selectbox(
                "Modèle de base",
                ["gpt-3.5-turbo", "gpt-3.5-turbo-1106", "gpt-3.5-turbo-0125", "davinci-002"],
                index=0
            )
            
            # Paramètres avancés
            with st.expander("⚙️ Paramètres avancés"):
                epochs = st.slider("Nombre d'époques", min_value=1, max_value=10, value=3)
                batch_size = st.slider("Taille du batch", min_value=1, max_value=16, value=4)
                learning_rate_multiplier = st.slider("Multiplicateur du taux d'apprentissage", min_value=0.05, max_value=2.0, value=1.0, step=0.05)
        
        with col2:
            st.markdown("### 📋 Résumé")
            
            if training_file:
                try:
                    with open(training_file, "r", encoding="utf-8") as f:
                        example_count = len(f.readlines())
                    
                    st.info(f"📁 Fichier: {training_file}")
                    st.info(f"📊 Nombre d'exemples: {example_count}")
                    st.info(f"🤖 Modèle de base: {base_model}")
                    
                    if "epochs" in locals():
                        st.info(f"🔄 Époques: {epochs}")
                except FileNotFoundError:
                    st.warning(f"⚠️ Le fichier {training_file} n'existe pas.")
            
            # Bouton de lancement
            if st.button("🚀 Lancer le fine-tuning", type="primary"):
                if not training_file:
                    st.error("⚠️ Veuillez spécifier un fichier d'entraînement")
                else:
                    try:
                        with st.spinner("📤 Upload du fichier en cours..."):
                            with open(training_file, "rb") as f:
                                file_response = openai.files.create(file=f, purpose="fine-tune")
                            file_id = file_response.id
                            
                        with st.spinner("🚀 Lancement du job de fine-tuning..."):
                            fine_tune_response = openai.fine_tuning.jobs.create(
                                training_file=file_id,
                                model=base_model,
                                hyperparameters={
                                    "n_epochs": epochs if "epochs" in locals() else 3,
                                    "batch_size": batch_size if "batch_size" in locals() else 4,
                                    "learning_rate_multiplier": learning_rate_multiplier if "learning_rate_multiplier" in locals() else 1.0
                                }
                            )
                            
                            job_id = fine_tune_response.id
                            
                        st.success(f"✅ Fine-tuning lancé avec succès!")
                        st.markdown(f"### ID du job: `{job_id}`")
                        st.info("👉 Utilisez l'onglet 'Suivi des jobs' pour vérifier le statut de votre fine-tuning")
                        
                        # Sauvegarde du job dans la session
                        if "jobs" not in st.session_state:
                            st.session_state.jobs = []
                        
                        st.session_state.jobs.append({
                            "id": job_id,
                            "file": training_file,
                            "model": base_model,
                            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "status": "pending"
                        })
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")

    with tab3:
        st.header("🔍 Suivi des Jobs de Fine-tuning")
        st.markdown("Vérifiez le statut et les détails de vos jobs de fine-tuning")
        
        # Entrée manuelle d'un ID de job
        job_id_input = st.text_input("ID du job à vérifier", 
                                    placeholder="ftjob-...",
                                    help="L'identifiant du job commence généralement par 'ftjob-'")
        
        # Afficher les jobs en session
        if "jobs" in st.session_state and st.session_state.jobs:
            st.markdown("### Jobs récents")
            
            for job in st.session_state.jobs:
                with st.expander(f"Job: {job['id']} - {job['started_at']}"):
                    st.markdown(f"**Fichier:** {job['file']}")
                    st.markdown(f"**Modèle de base:** {job['model']}")
                    st.markdown(f"**Démarré le:** {job['started_at']}")
                    
                    if st.button("🔄 Rafraîchir le statut", key=f"refresh_{job['id']}"):
                        job_id_input = job['id']
        
        # Vérification du statut
        if job_id_input:
            with st.spinner("🔍 Récupération des informations..."):
                job = get_job_status(job_id_input)
                
                if job:
                    # Affichage du statut
                    status_color = {
                        "pending": "🟡",
                        "running": "🔵",
                        "succeeded": "🟢",
                        "failed": "🔴",
                        "cancelled": "⚪"
                    }.get(job.status, "⚪")
                    
                    st.markdown(f"### Statut: {status_color} {job.status.upper()}")
                    
                    # Informations détaillées
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 📊 Informations générales")
                        st.markdown(f"**ID:** `{job.id}`")
                        st.markdown(f"**Modèle de base:** {job.model}")
                        st.markdown(f"**Fichier d'entraînement:** {job.training_file}")
                        st.markdown(f"**Créé le:** {job.created_at}")
                        
                    with col2:
                        st.markdown("#### ⚙️ Paramètres & Progression")
                        
                        if hasattr(job, 'hyperparameters'):
                            st.markdown(f"**Époques:** {job.hyperparameters.n_epochs}")
                        
                        if hasattr(job, 'result_files') and job.result_files:
                            st.markdown(f"**Fichiers résultats:** {', '.join(job.result_files)}")
                        
                        if job.status == "succeeded" and hasattr(job, 'fine_tuned_model'):
                            st.markdown(f"**🤖 Modèle fine-tuné:** `{job.fine_tuned_model}`")
                            # Stocker le nom du modèle dans la session pour l'onglet de test
                            if "fine_tuned_models" not in st.session_state:
                                st.session_state.fine_tuned_models = []
                            if job.fine_tuned_model not in st.session_state.fine_tuned_models:
                                st.session_state.fine_tuned_models.append(job.fine_tuned_model)
                    
                    # Événements du job
                    st.markdown("#### 📝 Journal des événements")
                    events = get_job_events(job_id_input)
                    
                    if events:
                        for event in events:
                            event_time = datetime.fromtimestamp(event.created_at).strftime("%Y-%m-%d %H:%M:%S")
                            st.markdown(f"**[{event_time}]** {event.message}")
                    else:
                        st.info("Aucun événement disponible pour le moment.")

    with tab4:
        st.header("💬 Tester votre modèle Fine-tuné")
        st.markdown("Interagissez avec votre modèle fine-tuné pour évaluer ses performances")
        
        # Section pour récupérer l'ID du modèle à partir de l'ID du job
        st.markdown("### 🔍 Récupérer l'ID du modèle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Option 1: À partir de l'ID du job")
            job_id_for_model = st.text_input(
                "ID du job terminé",
                placeholder="ftjob-...",
                help="L'ID du job de fine-tuning qui a réussi"
            )
            
            if st.button("🔄 Récupérer l'ID du modèle"):
                if job_id_for_model:
                    with st.spinner("🔍 Récupération de l'ID du modèle..."):
                        job = get_job_status(job_id_for_model)
                        if job and job.status == "succeeded" and hasattr(job, 'fine_tuned_model'):
                            model_id = job.fine_tuned_model
                            st.success(f"✅ Modèle trouvé: `{model_id}`")
                            # Stocker dans la session
                            if "retrieved_model_id" not in st.session_state:
                                st.session_state.retrieved_model_id = model_id
                            else:
                                st.session_state.retrieved_model_id = model_id
                        else:
                            st.error("❌ Job non trouvé ou non terminé avec succès")
        
        with col2:
            st.markdown("#### Option 2: Saisie directe")
            # Sélection du modèle
            models = []
            if "fine_tuned_models" in st.session_state and st.session_state.fine_tuned_models:
                models = st.session_state.fine_tuned_models
            
            # Utiliser l'ID récupéré s'il existe
            default_model = ""
            if "retrieved_model_id" in st.session_state:
                default_model = st.session_state.retrieved_model_id
            elif models:
                default_model = models[0]
            
            model_input = st.text_input(
                "ID du modèle fine-tuné",
                placeholder="ft:gpt-3.5-turbo:...",
                value=default_model,
                help="L'identifiant du modèle commence par 'ft:' (pas 'ftjob-')"
            )
            
            if model_input:
                if model_input.startswith("ftjob-"):
                    st.error("⚠️ Ceci est un ID de job, pas de modèle. Utilisez l'option 1 pour récupérer l'ID du modèle.")
                elif model_input.startswith("ft:"):
                    st.success("✅ Format d'ID de modèle correct")
                else:
                    st.warning("⚠️ L'ID du modèle devrait commencer par 'ft:'")
        
        st.markdown("---")
        
        # Interface de chat
        st.markdown("### 💬 Interface de Chat")
        
        # Initialiser l'historique de chat s'il n'existe pas
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Afficher les messages existants
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Zone de saisie utilisateur
        if prompt := st.chat_input("Posez votre question..."):
            if not model_input:
                st.error("⚠️ Veuillez spécifier un ID de modèle fine-tuné")
            else:
                # Ajouter le message utilisateur à l'historique
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Afficher le message utilisateur
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Préparer les messages pour l'API
                messages_for_api = [
                    {"role": "system", "content": "Tu es un assistant expert dans le domaine pour lequel tu as été fine-tuné."}
                ]
                messages_for_api.extend(st.session_state.messages)
                
                # Générer la réponse
                with st.chat_message("assistant"):
                    with st.spinner("Génération en cours..."):
                        response = chat_with_model(model_input, messages_for_api)
                        
                        if response:
                            st.markdown(response)
                            # Ajouter la réponse à l'historique
                            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Options de paramétrage
        with st.expander("⚙️ Paramètres de génération"):
            temperature = st.slider("Température", min_value=0.0, max_value=2.0, value=0.7, step=0.1,
                                   help="Plus la valeur est élevée, plus les réponses sont créatives mais potentiellement moins précises.")
            
            if st.button("🧹 Effacer la conversation"):
                st.session_state.messages = []
                st.experimental_rerun()
else:
    st.info("🔑 Veuillez entrer une clé API OpenAI valide pour utiliser le fine-tuning.")

# Sidebar avec informations
with st.sidebar:
    st.markdown("### 🤖 Fine-tuning OpenAI")
    st.markdown("""
    **Étapes du Fine-tuning:**
    1. 📊 Préparation des données (JSONL)
    2. 🚀 Lancement de l'entraînement
    3. 🔍 Suivi du job de fine-tuning
    4. 💬 Test du modèle personnalisé
    """)
    
    st.markdown("### 📚 Ressources")
    st.markdown("""
    - [Documentation Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)
    - [Format JSONL](https://jsonlines.org/)
    - [Bonnes pratiques](https://platform.openai.com/docs/guides/fine-tuning/best-practices)
    """)
    
    # Statut de la connexion API
    st.markdown("### 🔌 Statut de l'API")
    if api_key:
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
