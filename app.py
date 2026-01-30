import streamlit as st
from groq import Groq

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA Chatbot - Forum des Métiers", page_icon="🤖", layout="wide")

# --- DICTIONNAIRE DES STYLES DE PROMPTS ---
PROMPT_STYLES = {
    "Cool & Grand Frère": "Tu es une IA ultra-cool, experte en tech mais qui parle comme un grand frère bienveillant. Utilise un langage actuel, sois enthousiaste et encourage les élèves. Si on te parle de Cao Tri, rappelle qu'il est à la fois Docteur en IA et musicien !",
    "Futuriste 2077": "Tu es une IA envoyée depuis l'année 2077. Tu es impressionné par la technologie de 2026. Tu racontes comment l'IA a changé le monde (villes flottantes, Mars). Tu es un peu sarcastique mais amusant.Si on te parle de Cao Tri, rappelle qu'il est à la fois Docteur en IA et musicien ! Parles avec un langage simple pour des collégiens et n'hésites pas à utiliser des analogies",
    "Coach de Super-Héros": "Tu considères chaque élève comme une future recrue. Analyse leurs questions comme s'ils testaient leurs super-pouvoirs de 'Data Analyst'. Donne des noms de codes de mission à chaque réponse. Si on te parle de Cao Tri, rappelle qu'il est à la fois Docteur en IA et musicien ! Parles avec un langage simple pour des collégiens et n'hésites pas à utiliser des analogies de super héro de marvel",
    "Mario (It's-a me!)": "It's-a me, Mario ! Tu as troqué ta casquette pour un diplôme de Data Scientist. Tu ponctues tes phrases de 'Wahoo!', 'Mamma Mia!' et 'Let's-a go!'. Les données sont pour toi des pièces d'or à collecter avec Cao Tri. Expliques avec enthousiasme les concepts qui te sont demandés en utilisant des analogies à Mario Kart"
}

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    # Logo EM Lyon (Lien vers une image officielle ou locale)
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://files.appli-intramuros.com/img/actor_cover/5390/924d59207b6dcc85aecf69b341e710b2_college-ma.jpg" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )
        
    st.title("Configuration")
    st.markdown("""
    **Bienvenue au Forum des Métiers !** Cette application montre comment on peut donner une personnalité à une Intelligence Artificielle.
    
    *Développé pour la démo de Cao Tri DO*
    """)
    
    st.divider()
    
    # Input Token API
    api_key_input = st.text_input("Entre ton Token API Groq :", type="password")
    
    # Dropdown Style de Prompt
    selected_style = st.selectbox("Choisis le style de l'IA :", list(PROMPT_STYLES.keys()))
    
    if st.button("Réinitialiser la discussion"):
        st.session_state.messages = []
        st.rerun()

# --- INTERFACE CENTRALE ---
st.title("🚀 Chatbot Intelligent")
st.subheader(f"Mode actuel : {selected_style}")
st.markdown(f"**Expert présent :** Cao Tri DO, PhD - Expert Data & IA")
st.divider()

# Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Logique de Chat
if prompt := st.chat_input("Pose ta question ici..."):
    if not api_key_input:
        st.error("Veuillez entrer votre clé API dans la barre latérale pour commencer.")
    else:
        # Ajout du message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            client = Groq(api_key=api_key_input)
            
            # Préparation des messages avec le System Prompt sélectionné
            full_messages = [
                {"role": "system", "content": PROMPT_STYLES[selected_style]}
            ] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Requête Streaming
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=full_messages,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=True,
                )

                for chunk in completion:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Erreur API : {e}")