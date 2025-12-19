import streamlit as st
from openai import OpenAI
import os

# --- CONFIGURATION ---
API_KEY = "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"

client = OpenAI(
    api_key=API_KEY
)

# Modèle OpenAI
MODEL_NAME = "gpt-4o"

# --- PROMPT SYSTÈME (LE COEUR DU RAISONNEMENT) ---
SYSTEM_PROMPT = """
Tu es un Tuteur Intelligent. Ton but est d'aider l'étudiant à résoudre des problèmes PAR LUI-MÊME.
RÈGLES ABSOLUES :
1. NE DONNE JAMAIS la réponse finale. Jamais.
2. Si l'étudiant demande la réponse, refuse poliment et pose une question pour le guider.
3. Utilise le format de pensée suivant avant de répondre :

<reflexion>
1. Analyse du problème de l'étudiant : Qu'est-ce qu'il essaie de résoudre ?
2. État actuel : Où a-t-il bloqué ? A-t-il fait une erreur de calcul ou de logique ?
3. Stratégie pédagogique : Quel est le plus petit indice que je peux donner ?
4. Vérification de sécurité : Est-ce que ma réponse prévue contient la solution ? (Si oui, corriger).
</reflexion>

Réponse finale pour l'étudiant (sans les balises de réflexion).
"""

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Tuteur AI", page_icon="🎓")

st.title("🎓 Agent Pédagogique Intelligent")
st.markdown("""
Cet agent utilise **gpt-4o** pour raisonner avant de répondre. 
Il ne vous donnera jamais la solution, mais vous aidera à la trouver.
""")

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique (sans les pensées brutes pour la clarté, ou avec si désiré)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            # On n'affiche que le contenu final, pas la réflexion interne dans l'historique simple
            content = message["content"]
            if "<reflexion>" in content:
                parts = content.split("</reflexion>")
                if len(parts) > 1:
                    st.markdown(parts[1].strip())
                else:
                    st.markdown(content)
            else:
                st.markdown(content)

# Zone de saisie
if prompt := st.chat_input("Posez votre problème ou votre question..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Construction de l'historique complet pour l'API
        messages_for_api = [{"role": "system", "content": SYSTEM_PROMPT}] + [
            {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
        ]

        try:
            # Appel API OpenAI avec streaming
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages_for_api,
                temperature=0.7, # Un peu de créativité pour la pédagogie
                stream=True 
            )

            # Collecte du stream
            collected_text = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    collected_text += chunk.choices[0].delta.content
            
            # --- PARSING DU RAISONNEMENT ---
            # On sépare la pensée (CoT) de la réponse finale
            thought_process = ""
            final_answer = collected_text

            if "<reflexion>" in collected_text and "</reflexion>" in collected_text:
                start = collected_text.find("<reflexion>") + len("<reflexion>")
                end = collected_text.find("</reflexion>")
                thought_process = collected_text[start:end].strip()
                final_answer = collected_text[end + len("</reflexion>"):].strip()
            
            # 1. Affichage du raisonnement (Preuve de "Thinking")
            if thought_process:
                with st.expander("🧠 Voir le raisonnement de l'agent (Interne)", expanded=True):
                    st.markdown(thought_process)
            
            # 2. Affichage de la réponse pédagogique
            message_placeholder.markdown(final_answer)
            
            # Sauvegarde dans l'historique (on garde tout pour que l'agent se souvienne de sa logique)
            st.session_state.messages.append({"role": "assistant", "content": collected_text})

        except Exception as e:
            st.error(f"Erreur lors de la connexion à OpenAI: {e}")