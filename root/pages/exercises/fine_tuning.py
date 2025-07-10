import streamlit as st
import openai
import json

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

st.title("Fine-tuning Chatbot OpenAI")

api_key = st.text_input("Entrez votre clé OpenAI API :", type="password")

if api_key:
    openai.api_key = api_key
    if st.button("Créer un exemple de fichier d'entraînement (data.jsonl)"):
        create_sample_jsonl()
        st.success("Fichier data.jsonl créé avec 10 exemples !")
    training_file = st.text_input("Nom du fichier d'entraînement (ex: data.jsonl)")
    if st.button("Lancer le fine-tuning") and training_file:
        try:
            job_id = openai_chat_finetune(training_file)
            st.success(f"Fine-tuning lancé ! ID du job : {job_id}")
        except Exception as e:
            st.error(f"Erreur : {e}")
else:
    st.info("Veuillez entrer votre clé API pour continuer.")
