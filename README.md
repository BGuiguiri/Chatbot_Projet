# 🎓 ISE, Assistant AI

> Assistant intelligent dédié au concours ISE — organisé par le CAPESA en Afrique.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://votre-app.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/licence-MIT-green)

---

## 📌 À propos

**ISE, Assistant AI** est une application web conversationnelle qui permet à tout candidat de poser des questions sur le concours **ISE (Ingénieur Statisticien Économiste)** et d'obtenir des réponses claires, précises et instantanées.

L'application s'appuie sur une base de connaissances structurée (`faq_ise.csv`) et un modèle de langage (LLM) via **OpenRouter** pour formuler des réponses naturelles en français.

---

## ✨ Fonctionnalités

- 💬 **Chat conversationnel** — posez vos questions en langage naturel
- 📚 **Base de connaissances ISE** — réponses fondées sur une FAQ officielle structurée
- 🤖 **IA générative** — reformulation intelligente via OpenRouter
- 🗂️ **Historique de conversation** — contexte maintenu sur plusieurs échanges
- 📝 **Journal des échanges** — sauvegarde automatique dans `chat_log.csv`
- 📱 **Interface responsive** — accessible sur mobile et desktop

---

## 🚀 Démo en ligne

👉 [Accéder à l'application](https://votre-app.streamlit.app)

---

## 🛠️ Stack technique

| Composant | Technologie |
|---|---|
| Interface | [Streamlit](https://streamlit.io) |
| LLM | [OpenRouter](https://openrouter.ai) (`openrouter/auto`) |
| Langue | Python 3.10+ |
| Base de données | CSV (`faq_ise.csv`) |
| Déploiement | Streamlit Cloud |

---

## ⚙️ Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-username/ise-assistant-ai.git
cd ise-assistant-ai

# 2. Installer les dépendances
pip install streamlit

# 3. Ajouter la clé API
# Créez le fichier .streamlit/secrets.toml et ajoutez :
# OPENROUTER_API_KEY = "votre_clé_ici"

# 4. Lancer l'application
streamlit run app.py
```

---

## 🔑 Configuration

Créez un fichier `.streamlit/secrets.toml` à la racine du projet :

```toml
OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxxxxxx"
```

> ⚠️ Ne committez jamais ce fichier sur GitHub. Ajoutez-le à votre `.gitignore`.

---

## 📁 Structure du projet

```
ise-assistant-ai/
├── app.py              # Application principale
├── faq_ise.csv         # Base de connaissances ISE
├── chat_log.csv        # Journal des conversations (généré automatiquement)
├── .streamlit/
│   └── secrets.toml    # Clé API (non versionné)
└── README.md
```

---

## 🙋 Public cible

Cette application s'adresse au **grand public** souhaitant se renseigner sur le concours ISE : étudiants, familles, curieux ou futurs candidats.

---

## 📄 Licence

Ce projet est sous licence **MIT** — libre d'utilisation et de modification.

---

<p align="center">Fait avec ❤️ pour les candidats au concours ISE · CAPESA</p>
