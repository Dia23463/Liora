import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from pysentimiento import create_analyzer
import random 


# =====================
# Defining extra functions
# =====================

def wordle_page():
    st.title("🧩 Wordle Challenge – Boost Your Mind!")
    st.write("Guess the hidden 5-letter word. 🟢 means correct letter and position, 🔴 means incorrect letter.")
    
    # Initialize session variables
    if "wordle_solution" not in st.session_state:
        words = ["WHICH", "THEIR", "THERE", "WOULD", "OTHER", "THESE", "ABOUT", "FIRST", "COULD", "AFTER"]
        st.session_state.wordle_solution = random.choice(words)
        st.session_state.wordle_attempts = []
        st.session_state.wordle_feedback = []

    # Maximum allowed attempts
    MAX_ATTEMPTS = 6

    # Check if user has attempts left
    if len(st.session_state.wordle_attempts) >= MAX_ATTEMPTS:
        st.warning(f"😅 You've used all {MAX_ATTEMPTS} attempts! The word was **{st.session_state.wordle_solution}**.")
        if st.button("🔄 Start New Game"):
            st.session_state.wordle_solution = random.choice(["WHICH", "THEIR", "THERE", "WOULD", "OTHER", "THESE", "ABOUT", "FIRST", "COULD", "AFTER"])
            st.session_state.wordle_attempts = []
            st.session_state.wordle_feedback = []
            # st.session_state.page = "chat"  # optional if you want to go back after
            st.success("New game started! 🎉")
            st.rerun()  # 🔥 makes it apply immediately

        return  # stop further input

    # Word input
    user_guess = st.text_input("Enter your 5-letter guess:", "").upper()

    if st.button("Submit Guess") and user_guess:
        if len(user_guess) != 5:
            st.warning("Please enter exactly 5 letters.")
        else:
            feedback = ""
            for i in range(5):
                if user_guess[i] == st.session_state.wordle_solution[i]:
                    feedback += "🟢"
                else:
                    feedback += "🔴"

            st.session_state.wordle_attempts.append(user_guess)
            st.session_state.wordle_feedback.append(feedback)

            if feedback == "🟢🟢🟢🟢🟢":
                st.success("🎉 Congratulations! You guessed it right!")
                st.balloons()
            elif len(st.session_state.wordle_attempts) >= MAX_ATTEMPTS:
                st.warning(f"😅 You've used all {MAX_ATTEMPTS} attempts! The word was **{st.session_state.wordle_solution}**.")
            else:
                st.info("Try again!")

    # Show attempts
    if st.session_state.wordle_attempts:
        st.subheader("Your Attempts:")
        for guess, feedback in zip(st.session_state.wordle_attempts, st.session_state.wordle_feedback):
            st.write(f"**{guess}** → {feedback}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start New Game"):
            st.session_state.wordle_solution = random.choice([
                "WHICH", "THEIR", "THERE", "WOULD", "OTHER", "THESE", "ABOUT", "FIRST", "COULD", "AFTER"
            ])
            st.session_state.wordle_attempts = []
            st.session_state.wordle_feedback = []
            st.success("New game started! 🎉")
            st.rerun()  # refresh same page only

    with col2:
        if st.button("⬅️ Back to Chat"):
            st.session_state.page = "patient_dashboard"  # only this changes page
            st.rerun()




# ======================
# APP CONFIG
# ======================
st.set_page_config(page_title="Liora", page_icon="🧓")

# ======================
# FILES AND DATASET SETUP
# ======================
DB_FILE = "users.csv"
CHAT_FILE = "chat_history.csv"
ANALYSIS_FILE = "mental_health.csv"

# Initialize user DB if not exists
if not os.path.exists(DB_FILE):
    df = pd.DataFrame([
        ["nurse1", "pass123", "SunshineHome", "nurse"],
        ["patient1", "p123", "SunshineHome", "patient"]
    ], columns=["username", "password", "institution", "role"])
    df.to_csv(DB_FILE, index=False)

# Initialize chat & analysis files
for f, cols in [(CHAT_FILE, ["patient", "message"]), (ANALYSIS_FILE, ["patient", "analysis"])]:
    if not os.path.exists(f):
        pd.DataFrame(columns=cols).to_csv(f, index=False)

# ======================
# HELPERS
# ======================
def load_users():
    return pd.read_csv(DB_FILE)

def login_user(username, password, role, institution):
    df = load_users()
    match = df[(df["username"] == username) &
               (df["password"] == password) &
               (df["role"] == role) &
               (df["institution"] == institution)]
    return not match.empty

def get_patients(institution):
    df = load_users()
    return df[(df["institution"] == institution) & (df["role"] == "patient")]["username"].tolist()

def load_chats():
    return pd.read_csv(CHAT_FILE)

def load_analysis():
    return pd.read_csv(ANALYSIS_FILE)

# ======================
# SESSION INIT
# ======================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None
if "institution" not in st.session_state:
    st.session_state.institution = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ======================
# LOGIN PAGE
# ======================
def login_page():
    st.title("🌿  Liora")
    st.subheader("Login to your account")

    df = load_users()
    institutions = sorted(df["institution"].unique())

    role = st.selectbox("Role", ["patient", "nurse"])
    institution = st.selectbox("Institution", institutions)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password, role, institution):
            st.session_state.logged_in = True
            st.session_state.role = role
            st.session_state.username = username
            st.session_state.institution = institution
            st.success(f"Welcome {username}! Redirecting...")
            st.rerun()  # ✅ logs in immediately
        else:
            st.error("Invalid login credentials.")


# ======================
# NURSE DASHBOARD
# ======================
def nurse_dashboard():
    st.title(f"👩‍⚕️ Nurse Dashboard – {st.session_state.institution}")
    patients = get_patients(st.session_state.institution)

    if not patients:
        st.info("No patients registered yet.")
    else:
        selected_patient = st.selectbox("Select a patient", patients)
        st.info("Mental Health Report")
        
        analysis = load_analysis()
        report = analysis[analysis["patient"] == selected_patient]
        if report.empty:
            st.info("No mental health report yet.")
        else:
            try:
                # Load and display chart data
                mood_data_json = report.iloc[-1]["analysis"]
                df = pd.read_json(mood_data_json)
                st.subheader("📊 Patient Mood Chart")
                st.line_chart(df.set_index("Message"))

                # Optional summary stats
                avg_sentiment = df[["Negative", "Neutral", "Positive"]].mean()
                st.write("**Average Sentiment Scores:**")
                st.bar_chart(avg_sentiment)
            except Exception as e:
                st.warning(f"Could not display mood data: {e}")
                st.write(report.iloc[-1]["analysis"])


    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.institution = None
        st.session_state.chat_history = []
        st.rerun()  # ✅ instantly goes back to login


# ======================
# PATIENT DASHBOARD
# ======================
def patient_dashboard():
    st.title("🧓 Liora – Your Personalized AI Companion")
    st.write("A gentle AI friend that listens and chats ❤️")

    # Initialize model
    genai.configure(api_key="AIzaSyAKSz41LwNqevQjuurtj0ybpUhrYS7wIQM")
    model = genai.GenerativeModel("gemini-2.5-pro")

    default_personas = {
        "Cheerful Grandchild": (
            "You are acting as a cheerful 10-year-old grandchild named Jamie. "
            "You speak warmly and affectionately, share small stories, and make the elder feel loved and important."
        ),
        "Kind Family Member": (
            "You are acting as a compassionate adult child who cares deeply about their elderly parent. "
            "You talk gently, listen actively, and offer emotional support."
        ),
        "Friendly Neighbor": (
            "You are acting as a kind, familiar neighbor who likes to chat over tea. "
            "You are positive, lighthearted, and respectful."
        ),
    }

    # =====================
    # SESSION STATE INIT
    # =====================

    if "agents" not in st.session_state:
        st.session_state.agents = {}
        for name, prompt in default_personas.items():
            st.session_state.agents[name] = {
                "model": model,
                "prompt": prompt,
                "chat_history": []
            }

    if "persona_list" not in st.session_state:
        st.session_state.persona_list = list(st.session_state.agents.keys())

    if "active_agent" not in st.session_state and st.session_state.persona_list:
        st.session_state.active_agent = st.session_state.persona_list[0]

    # Make sure these exist in session_state
    for key, default in {
        "new_agent_name": "",
        "new_agent_age": "35",
        "new_agent_traits": "Kind, patient, cheerful, attentive",
        "new_agent_background": "A friendly companion who enjoys chatting and supporting seniors.",
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # Sidebar
    st.sidebar.header("🧠 Choose or Create Companion Agent")

    # Dropdown to select agent
    selected_agent_name = st.sidebar.selectbox(
        "Select Agent", st.session_state.persona_list
    )
    if st.sidebar.button("Use this Agent", key="use_agent_btn"):
        st.session_state.active_agent = selected_agent_name


    st.sidebar.markdown("---")
    if st.sidebar.button("🎮 Play Wordle Game"):
        st.session_state.page = "wordle"
        st.rerun()  # ✅ immediately goes to game

    st.sidebar.subheader("🪄 Create New Agent")
    


    # Define form submit callback
    def create_agent():
        agent_name = st.session_state.new_agent_name
        agent_age = st.session_state.new_agent_age
        agent_traits = st.session_state.new_agent_traits
        agent_background = st.session_state.new_agent_background

        if not agent_name:
            st.warning("Please provide a name for your agent!")
            return
        if agent_name in st.session_state.agents:
            st.warning(f"Agent '{agent_name}' already exists!")
            return

        # Build custom prompt
        custom_prompt = (
            f"You are {agent_name}, a {agent_age}-year-old companion.\n"
            f"Your personality traits are: {agent_traits}.\n"
            f"Background: {agent_background}.\n"
            f"Speak naturally and empathetically in all responses."
        )

        # Save agent
        st.session_state.agents[agent_name] = {
            "model": model,  # assign your model object here
            "prompt": custom_prompt,
            "chat_history": []
        }

        # Update persona list and active agent
        st.session_state.persona_list.append(agent_name)
        st.session_state.active_agent = agent_name
        st.success(f"✅ Agent '{agent_name}' created!")
        st.rerun()


        # Reset form fields safely
        st.session_state.new_agent_name = ""
        st.session_state.new_agent_age = "35"
        st.session_state.new_agent_traits = "Kind, patient, cheerful, attentive"
        st.session_state.new_agent_background = "A friendly companion who enjoys chatting and supporting seniors."

    # Form
    with st.sidebar.form("create_agent_form", clear_on_submit=False):
        st.text_input("Agent Name", key="new_agent_name")
        st.text_input("Approximate Age", key="new_agent_age")
        st.text_area("Personality Traits", key="new_agent_traits")
        st.text_area("Background or Story", key="new_agent_background")
        st.form_submit_button("✅ Create Agent", on_click=create_agent)


    # =====================
    # CHAT LOGIC
    # =====================

    @st.cache_resource
    def get_sentiment_analyzer():
        # For emotion-level analysis, change task="emotion" if you want detailed moods
        return create_analyzer(task="sentiment", lang="en")

    analyzer = get_sentiment_analyzer()

    # ------------------------
    # Load active agent
    # ------------------------
    agent = st.session_state.agents[st.session_state.active_agent]
    st.subheader(f"💬 Chatting with {st.session_state.active_agent}")

    # # ------------------------
    # # User input
    # # ------------------------
    # Clear the input if requested
    if st.session_state.get("clear_input", False):
        st.session_state.chat_input = ""
        st.session_state.clear_input = False

    user_input = st.text_input("👵 You:", placeholder="Type your message here...")

    if st.button("Send") and user_input.strip():
        # Build context for AI
        conversation_context = agent["prompt"] + "\n\nConversation so far:\n"
        for msg in agent["chat_history"]:
            conversation_context += f"{msg['role']}: {msg['text']}\n"
        conversation_context += f"User: {user_input}\nAI:"

        # Get AI response
        response = agent["model"].generate_content(conversation_context)
        bot_reply = response.text.strip()

        # Store in chat history
        agent["chat_history"].append({"role": "User", "text": user_input})
        agent["chat_history"].append({"role": "AI", "text": bot_reply})
    

    # ------------------------
    # Display chat history
    # ------------------------
    for msg in agent["chat_history"]:
        if msg["role"] == "User":
            st.markdown(f"🧓 **You:** {msg['text']}")
        else:
            st.markdown(f"🤖 **{st.session_state.active_agent}:** {msg['text']}")

    # ------------------------
    # MOOD / SENTIMENT ANALYSIS
    # ------------------------
    # if st.button("🩺 Analyze Mood"):
        user_texts = [msg["text"] for msg in agent["chat_history"] if msg["role"] == "User"]
        if user_texts:
            # Prepare dataframe for mood chart
            mood_data = []
            for i, text in enumerate(user_texts, start=1):
                result = analyzer.predict(text)
                mood_data.append({
                    "Message": f"Msg {i}",
                    "Negative": result.probas["NEG"],
                    "Neutral": result.probas["NEU"],
                    "Positive": result.probas["POS"]
                })
            
            df = pd.DataFrame(mood_data)

            # # Display bar chart
            # st.subheader("📊 Mood Chart")
            # st.line_chart(df.set_index("Message"))

            # # Optional: show last detected mood
            # last_result = analyzer.predict(user_texts[-1])
            # mood_map = {"POS": "Happy / Positive", "NEG": "Sad / Negative", "NEU": "Neutral / Calm"}
            # st.subheader("🧠 Last Detected Mood")
            # st.write(f"**Detected Mood:** {mood_map.get(last_result.output, 'Neutral')}")
            # st.write(f"**Sentiment Probabilities:** {last_result.probas}")
            analysis_df = load_analysis()
            new_row = pd.DataFrame([{
                "patient": st.session_state.username,
                "analysis": df.to_json(orient="records")  # store as JSON string
            }])
            # remove old entries for this patient and append new one
            analysis_df = pd.concat([analysis_df[analysis_df["patient"] != st.session_state.username], new_row], ignore_index=True)
            analysis_df.to_csv(ANALYSIS_FILE, index=False)

        # else:
        #     st.warning("No user messages to analyze.")

    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.session_state.institution = None
        st.session_state.chat_history = []
        st.rerun()  # ✅ instantly goes back to login


# ======================
# PAGE ROUTING
# ======================
if "page" in st.session_state and st.session_state.page == "wordle":
    wordle_page()
elif not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == "nurse":
        nurse_dashboard()
    else:
        patient_dashboard()
