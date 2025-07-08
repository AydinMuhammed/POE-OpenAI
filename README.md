# POE-OpenAI

Application Streamlit de traitement de texte utilisant des modèles de Machine Learning et d'Intelligence Artificielle.

## 🚀 Démo en ligne

L'application est déployée et accessible à l'adresse suivante :

**[https://aydinmuhammed-poe-openai-main-b8uhrb.streamlit.app/](https://aydinmuhammed-poe-openai-main-b8uhrb.streamlit.app/)**

## 📋 Fonctionnalités

- **Traitement de texte** avec NLTK (tokenisation, stemming, lemmatisation)
- **Traduction** anglais vers français
- **Extraction d'entités nommées**
- **Analyse de sentiment**
- **Extraction d'embeddings** avec BERT
- **Génération de texte** avec GPT-2
- **Interface interactive** avec Streamlit

## 🛠️ Technologies utilisées

- **Python 3.13**
- **Streamlit** - Interface utilisateur
- **Transformers (Hugging Face)** - Modèles de NLP
- **PyTorch** - Framework de deep learning
- **NLTK** - Traitement de texte
- **OpenAI** - API d'intelligence artificielle

## 📁 Structure du projet

```
POE-OpenAI/
├── main.py                 # Point d'entrée de l'application Streamlit
├── TextProcessor.py        # Classe de traitement de texte
├── Processing.py           # Classe de base pour le preprocessing
├── requirements.txt        # Dépendances Python
├── root/
│   └── pages/
│       ├── demos/          # Pages de démonstration
│       └── exercises/      # Pages d'exercices
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

4. Lancer l'application :
```bash
streamlit run main.py
```

## 📄 Licence

Ce projet est développé dans le cadre d'une formation POE (Préparation Opérationnelle à l'Emploi).