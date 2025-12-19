# 🎓 Tuteur IA - Agent Raisonneur

## 📝 Présentation du Projet
Ce projet implémente un **Agent Intelligent Éducatif** via Streamlit, dont l'objectif est d'accompagner les étudiants dans la résolution de problèmes **sans jamais leur fournir la réponse finale**.

Contrairement à un chatbot classique (type ChatGPT standard), notre agent "réfléchit avant de parler". Il analyse la demande, identifie les blocages pédagogiques, et construit une stratégie pour guider l'élève par des questions.

## 🧠 Techniques de Raisonnement (Cœur du projet)

Conformément aux exigences du sujet, l'agent n'est pas une simple "boîte noire". Nous avons implémenté une architecture cognitive explicite combinant **Chain of Thought (CoT)** et **Self-Correction**.

### Le flux de pensée (Reasoning Loop) :
L'agent suit un processus strict en deux temps, invisible pour l'étudiant mais visible via le mode "Débug" de l'interface :

1.  **Chain of Thought (CoT) - Planification :**
    * L'agent commence par générer une section `<reflexion>`.
    * Il **analyse** l'entrée (le problème de l'élève).
    * Il **diagnostique** l'erreur (calcul, logique, compréhension).
    * Il **planifie** une stratégie (quel indice donner ?).

2.  **Self-Correction & Guardrails :**
    * Avant de répondre, l'agent effectue une **auto-critique** au sein de sa réflexion.
    * *Check de sécurité :* "Est-ce que ma réponse prévue contient la solution ?"
    * Si oui, il reformule pour ne donner qu'un indice partiel.

Ce processus garantit que la pédagogie reste active et que l'agent ne "hallucine" pas la réponse finale directement.

## 🛠️ Stack Technique

* **Langage :** Python 3.x
* **Interface Utilisateur :** [Streamlit](https://streamlit.io/) (pour l'interactivité et l'affichage des étapes de réflexion).
* **Modèle LLM :** **OpenAI (xAI)** via l'API.
* **Gestion API :** `openai` python library.

## 🚀 Installation et Lancement

Suivez ces étapes pour tester le projet sur votre machine.

### 1. Prérequis
Assurez-vous d'avoir Python installé.

### 2. Installation des dépendances
installez-les :
`pip install -r requirements.txt`

### 3. Lancer l'application
Exécutez la commande suivante dans votre terminal :
`streamlit run app.py`