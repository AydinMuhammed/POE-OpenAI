# POE-OpenAI

Application Streamlit de traitement de texte utilisant des modèles de Machine Learning et d'Intelligence Artificielle.

## 🚀 Démo en ligne

L'application est déployée et accessible à l'adresse suivante :

**[https://aydinmuhammed-poe-openai-main-b8uhrb.streamlit.app/](https://aydinmuhammed-poe-openai-main-b8uhrb.streamlit.app/)**

## 🆕 Nouvelles Fonctionnalités

### Version 2.0 - Juillet 2025
- **🎨 Projet Final - Générateur d'Histoires Visuelles** : Workflow créatif complet combinant amélioration d'histoires, génération d'images et analyse visuelle
- **🤖 Fine-tuning de Modèles** : Interface complète pour créer, entraîner et tester vos propres modèles GPT personnalisés
- **🎵 Traitement Audio Avancé** : Transcription, traduction et synthèse vocale avec Whisper et TTS
- **👁️ Analyse d'Images** : Description automatique d'images avec GPT-4 Vision
- **🎨 Génération d'Images DALL-E 3** : Création d'images haute qualité avec paramètres avancés
- **🔄 Mise à jour Streamlit 1.46.1** : Compatibilité avec les dernières fonctionnalités et améliorations UI

## 📋 Fonctionnalités

### 🤖 Chatbot OpenAI
- **Conversation interactive** avec GPT-3.5-turbo et GPT-4
- **Mémoire de conversation** pour maintenir le contexte
- **Interface chat moderne** avec Streamlit
- **Sécurisation des clés API** via champ de saisie sécurisé
- **Effacement de l'historique** en un clic
- **Statistiques de conversation** en temps réel

### 🎨 Génération d'Images DALL-E
- **Génération d'images** avec DALL-E 3
- **Personnalisation des paramètres** (taille, qualité)
- **Téléchargement d'images** générées
- **Interface intuitive** pour la création artistique

### 👁️ Analyse d'Images GPT-4 Vision
- **Description automatique** d'images avec GPT-4o
- **Analyse détaillée** du contenu visuel
- **Intégration seamless** avec la génération d'images

### 🎵 Traitement Audio OpenAI
- **Transcription audio** avec Whisper (99+ langues)
- **Traduction multilingue** automatique
- **Text-to-Speech** avec 6 voix différentes
- **Support multi-formats** (MP3, WAV, M4A, OGG, FLAC)
- **Qualité configurable** (standard et HD)

### 🤖 Fine-tuning de Modèles
- **Création de datasets** d'entraînement au format JSONL
- **Fine-tuning GPT-3.5-turbo** personnalisé
- **Suivi des jobs** de fine-tuning en temps réel
- **Test des modèles** fine-tunés via interface de chat
- **Gestion complète** du cycle de vie des modèles

### 🎭 Projet Final - Générateur d'Histoires Visuelles
- **Amélioration d'histoires** avec GPT-4
- **Génération d'images** basée sur les histoires (DALL-E 3)
- **Description d'images** générées (GPT-4 Vision)
- **Workflow créatif complet** de l'idée à l'image
- **Galerie de créations** avec export
- **Filtrage de contenu** pour DALL-E

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
- **Système d'onglets** pour une navigation optimisée

## 🛠️ Technologies utilisées

- **Python 3.13**
- **Streamlit 1.46.1** - Interface utilisateur et déploiement
- **OpenAI API 1.93.1** - Suite complète d'outils IA
  - **GPT-3.5-turbo & GPT-4** - Chatbot conversationnel et amélioration de texte
  - **DALL-E 3** - Génération d'images
  - **GPT-4o (Vision)** - Analyse et description d'images
  - **Whisper** - Transcription et traduction audio
  - **Text-to-Speech** - Synthèse vocale
- **Transformers (Hugging Face)** - Modèles de NLP
- **PyTorch** - Framework de deep learning
- **NLTK** - Traitement de texte
- **Pandas** - Manipulation de données
- **Altair & Pydeck** - Visualisations
- **PIL (Pillow)** - Traitement d'images
- **Requests** - Téléchargement de contenu
- **Base64** - Encodage d'images

## 📁 Structure du projet

```
POE-OpenAI/
├── main.py                          # Point d'entrée de l'application
├── TextProcessor.py                 # Classe de traitement de texte
├── Processing.py                    # Classe de base pour le preprocessing
├── requirements.txt                 # Dépendances Python
├── data.jsonl                       # Données d'entraînement pour fine-tuning
├── QA_bot.csv                       # Dataset de questions-réponses
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
│           ├── chatbot.py           # Chatbot OpenAI
│           ├── generate_image.py    # Génération d'images DALL-E
│           ├── image_description.py # Analyse d'images GPT-4 Vision
│           ├── transcription_audio.py # Traitement audio complet
│           ├── fine_tuning.py       # Fine-tuning de modèles
│           └── final_project.py     # Générateur d'histoires visuelles
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

### Générateur d'Histoires Visuelles (Projet Final)
1. Saisissez une idée d'histoire dans le champ de texte
2. Laissez GPT-4 améliorer et enrichir votre histoire
3. Générez une image illustrant votre histoire avec DALL-E 3
4. Obtenez une description détaillée de l'image générée
5. Exportez vos créations depuis la galerie

### Fine-tuning de Modèles
1. Créez un dataset d'entraînement au format JSONL
2. Lancez un job de fine-tuning sur GPT-3.5-turbo
3. Suivez l'évolution de l'entraînement en temps réel
4. Testez votre modèle personnalisé via l'interface de chat

## 🔧 Améliorations Techniques

### Corrections et Optimisations
- **Migration vers `st.rerun()`** : Remplacement de `st.experimental_rerun()` pour compatibilité Streamlit 1.46.1
- **Gestion d'État Améliorée** : Meilleure persistance des données entre les interactions
- **Filtrage de Contenu DALL-E** : Nettoyage automatique des prompts pour éviter les erreurs de génération
- **Validation des Clés API** : Vérification en temps réel de la validité des clés OpenAI
- **Gestion des Erreurs Robuste** : Messages d'erreur explicites et récupération automatique
- **Interface Utilisateur Modernisée** : Utilisation des dernières fonctionnalités Streamlit (onglets, expandeurs, colonnes)

### Optimisations de Performance
- **Mise en Cache Intelligente** : Réduction des appels API redondants
- **Compression d'Images** : Optimisation des images pour un chargement plus rapide
- **Gestion Mémoire** : Nettoyage automatique des ressources temporaires

## 📄 Licence

Ce projet est développé dans le cadre d'une formation POE (Préparation Opérationnelle à l'Emploi).