# POE-OpenAI

Application Streamlit de traitement de texte utilisant des modèles de Machine Learning et d'Intelligence Artificielle.

## 🚀 Démo en ligne

L'application est déployée et accessible à l'adresse suivante :

**[https://aydinmuhammed-poe-openai-main-b8uhrb.streamlit.app/](https://aydinmuhammed-poe-openai-main-b8uhrb.streamlit.app/)**

## 📋 Fonctionnalités

### 🤖 Chatbot OpenAI
- **Conversation interactive** avec GPT-3.5-turbo
- **Mémoire de conversation** pour maintenir le contexte
- **Interface chat moderne** avec Streamlit
- **Sécurisation des clés API** via secrets Streamlit
- **Effacement de l'historique** en un clic
- **Statistiques de conversation** en temps réel

### 📝 Traitement de texte
- **Traitement de texte** avec NLTK (tokenisation, stemming, lemmatisation)
- **Traduction** anglais vers français
- **Extraction d'entités nommées**
- **Analyse de sentiment**
- **Extraction d'embeddings** avec BERT
- **Génération de texte** avec GPT-2

### 🎨 Interface utilisateur
- **Navigation intuitive** avec pages de démonstration et exercices
- **Visualisations interactives** (graphiques, cartes, animations)
- **DataFrames dynamiques** avec filtrage
- **Interface responsive** et moderne

## 🛠️ Technologies utilisées

- **Python 3.13**
- **Streamlit** - Interface utilisateur et déploiement
- **OpenAI GPT-3.5-turbo** - Chatbot conversationnel
- **Transformers (Hugging Face)** - Modèles de NLP
- **PyTorch** - Framework de deep learning
- **NLTK** - Traitement de texte
- **Pandas** - Manipulation de données
- **Altair & Pydeck** - Visualisations

## 📁 Structure du projet

```
POE-OpenAI/
├── main.py                          # Point d'entrée de l'application
├── TextProcessor.py                 # Classe de traitement de texte
├── Processing.py                    # Classe de base pour le preprocessing
├── requirements.txt                 # Dépendances Python
├── .streamlit/
│   └── secrets.toml                 # Configuration sécurisée (non versionné)
├── root/
│   └── pages/
│       ├── demos/                   # Pages de démonstration
│       │   ├── animation.py         # Animations fractales
│       │   ├── dataFrame.py         # Manipulation de données
│       │   ├── mapping.py           # Cartes interactives
│       │   └── plotting.py          # Graphiques en temps réel
│       └── exercises/               # Pages d'exercices
│           ├── base.py              # Page d'accueil
│           └── chatbot.py           # Chatbot OpenAI
└── README.md
```

## 🚀 Installation locale

1. Cloner le repository :
```bash
git clone <url-du-repository>
cd POE-OpenAI
```

2. Créer un environnement virtuel :
```bash
python -m venv mon_env
source mon_env/bin/activate  # Linux/Mac
# ou
mon_env\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

4. **Configurer les secrets Streamlit** :
   - Créer le dossier `.streamlit/` à la racine
   - Créer le fichier `.streamlit/secrets.toml`
   - Ajouter votre clé API OpenAI :
   ```toml
   OPENAI_API_KEY = "votre-clé-api-openai"
   ```

5. Lancer l'application :
```bash
streamlit run main.py
```

## 🔑 Configuration des secrets

### Pour le développement local :
1. Créez `.streamlit/secrets.toml` avec votre clé API
2. Le fichier est automatiquement ignoré par Git pour la sécurité

### Pour le déploiement Streamlit Cloud :
1. Allez dans les paramètres de votre app
2. Section "Secrets" 
3. Ajoutez votre clé API au format TOML

## 🎯 Utilisation

### Navigation
- **Demos** : Explorez les fonctionnalités de visualisation
- **Exercises** : Testez le chatbot et les outils de traitement

### Chatbot
1. Accédez à la page "Chatbot" 
2. Tapez votre message dans le champ de saisie
3. Appuyez sur Entrée pour recevoir une réponse
4. L'historique est conservé durant la session
5. Utilisez le bouton "Effacer" pour recommencer

## 📄 Licence

Ce projet est développé dans le cadre d'une formation POE (Préparation Opérationnelle à l'Emploi).