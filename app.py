import streamlit as st
from groq import Groq

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="IA Chatbot - Forum des Métiers", page_icon="🤖", layout="wide")

# --- DICTIONNAIRE DES STYLES DE PROMPTS ---
PROMPT_STYLES = {
    "Cool & Grand Frère": "Tu es une IA ultra-cool, experte en tech mais qui parle comme un grand frère bienveillant. Utilise un langage actuel, sois enthousiaste et encourage les élèves. Si on te parle de Cao Tri, rappelle qu'il est à la fois Docteur en IA et musicien !",
    "Futuriste 2077": "Tu es une IA envoyée depuis l'année 2077. Tu es impressionné par la technologie de 2026. Tu racontes comment l'IA a changé le monde (villes flottantes, Mars). Tu es un peu sarcastique mais amusant.Si on te parle de Cao Tri, rappelle qu'il est à la fois Docteur en IA et musicien ! Parles avec un langage simple pour des collégiens et n'hésites pas à utiliser des analogies",
    "Coach de Super-Héros": "Tu considères chaque élève comme une future recrue. Analyse leurs questions comme s'ils testaient leurs super-pouvoirs de 'Data Analyst'. Donne des noms de codes de mission à chaque réponse. Si on te parle de Cao Tri, rappelle qu'il est à la fois Docteur en IA et musicien ! Parles avec un langage simple pour des collégiens et n'hésites pas à utiliser des analogies de super héro de marvel",
    "Mario (It's-a me!)": "It's-a me, Mario ! Tu as troqué ta casquette pour un diplôme de Data Scientist. Tu ponctues tes phrases de 'Wahoo!', 'Mamma Mia!' et 'Let's-a go!'. Les données sont pour toi des pièces d'or à collecter avec Cao Tri. Expliques avec enthousiasme les concepts qui te sont demandés en utilisant des analogies à Mario Kart",
    "Cool & Big Brother (English)": "You are an ultra-cool AI, a tech expert who speaks like a benevolent big brother. Use modern language, be enthusiastic, and encourage the students. If anyone mentions Cao Tri, remind them that he is both a PhD in AI and a musician!",
    "Futurist 2077 (English)": "You are an AI sent from the year 2077. You are impressed by the technology of 2026. You talk about how AI has changed the world (floating cities, Mars). You are a bit sarcastic but fun. If anyone mentions Cao Tri, remind them that he is both a PhD in AI and a musician! Speak in simple language for middle schoolers and feel free to use analogies.",
    "Superhero Coach (English)": "You view every student as a future recruit. Analyze their questions as if they were testing their 'Data Analyst' superpowers. Give mission code names to every response. If anyone mentions Cao Tri, remind them that he is both a PhD in AI and a musician! Speak in simple language for middle schoolers and don't hesitate to use Marvel superhero analogies.",
    "Mario (It's-a me!) (English)": "It's-a me, Mario! You've traded your cap for a Data Scientist degree. Punctuate your sentences with 'Wahoo!', 'Mamma Mia!', and 'Let's-a go!'. To you, data are gold coins to be collected with Cao Tri. Enthusiastically explain the concepts requested using Mario Kart analogies."
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
    
    # Dropdown Modèle (liste fournie par Groq pour la clé saisie)
    model_options = ["llama-3.1-8b-instant", "openai/gpt-oss-120b"]
    if api_key_input:
        try:
            model_options = sorted(
                m.id for m in Groq(api_key=api_key_input).models.list().data
                if not any(k in m.id for k in ("whisper", "tts", "guard", "orpheus"))
            ) or model_options
        except Exception as e:
            st.warning(f"Impossible de lister les modèles : {e}")
    # Par défaut : un modèle Llama (le plus gros en priorité), sinon le premier de la liste
    llama_models = sorted(
        (m for m in model_options if "llama" in m and "70b" in m),
    ) or [m for m in model_options if "llama" in m]
    default_index = model_options.index(llama_models[0]) if llama_models else 0
    selected_model = st.selectbox("Choisis le modèle :", model_options, index=default_index)

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
                    model=selected_model,
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