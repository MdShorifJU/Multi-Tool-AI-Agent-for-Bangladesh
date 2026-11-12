import streamlit as st
import logging
from agent import run_agent


# ==============================
# Logging Configuration
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="Bangladesh AI Agent",
    page_icon="🇧🇩",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ==============================
# Custom CSS (minimal, theme-aware)
# ==============================

st.markdown("""
<style>

    /* Hide Streamlit default chrome for a cleaner production look */
    #MainMenu, footer, .stDeployButton {
        visibility: hidden;
        display: none;
    }

    /* Consistent content width and spacing */
    .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    .app-title {
        text-align: center;
        font-size: 1.9rem;
        font-weight: 700;
        line-height: 1.2;
        margin: 0;
    }

    .app-subtitle {
        text-align: center;
        opacity: 0.6;
        font-size: 0.95rem;
        margin: 0.35rem 0 1.5rem 0;
    }

    .welcome-box {
        text-align: center;
        padding: 2.5rem 1.25rem;
        border-radius: 14px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        background-color: rgba(128, 128, 128, 0.05);
        margin-top: 1rem;
    }

    .welcome-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
    }

    .welcome-text {
        opacity: 0.65;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .stChatMessage {
        border-radius: 12px;
    }

    .sidebar-footer {
        opacity: 0.55;
        font-size: 0.8rem;
        line-height: 1.5;
    }

</style>
""", unsafe_allow_html=True)


# ==============================
# Session State
# ==============================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ==============================
# Sidebar
# ==============================

with st.sidebar:

    st.subheader("Bangladesh AI Agent")

    st.caption(
        "An AI-powered multi-tool assistant for Bangladesh."
    )

    st.divider()

    st.markdown("**Available Features**")

    st.markdown("""
    - Restaurant Information
    - Hospital Information
    - Institutional Information
    - General Knowledge
    """)

    st.divider()

    st.metric(
        "Questions Asked",
        len(st.session_state.chat_history)
    )

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.chat_history = []
        st.rerun()

    st.divider()

    st.markdown(
        '<div class="sidebar-footer">'
        'Powered by Groq · LangChain · SQLite · Streamlit'
        '</div>',
        unsafe_allow_html=True
    )


# ==============================
# Header
# ==============================

st.markdown(
    '<h1 class="app-title">Bangladesh AI Agent</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="app-subtitle">'
    'Your Intelligent Multi-Tool AI Assistant'
    '</p>',
    unsafe_allow_html=True
)


# ==============================
# Welcome Section
# ==============================

if not st.session_state.chat_history:

    st.markdown(
        '<div class="welcome-box">'
        '<div class="welcome-title">Hello! How can I help you?</div>'
        '<div class="welcome-text">'
        'Ask me about restaurants, hospitals, institutions, '
        'or general knowledge in Bangladesh.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ==============================
# Display Chat History
# ==============================

for chat in st.session_state.chat_history:

    with st.chat_message("user"):

        st.markdown(chat["question"])

    with st.chat_message("assistant"):

        st.markdown(chat["answer"])


# ==============================
# Chat Input
# ==============================

question = st.chat_input(
    "Ask anything about Bangladesh..."
)


# ==============================
# Process Question
# ==============================

if question:

    if question.strip():

        # Display User Message

        with st.chat_message("user"):

            st.markdown(question)

        # Generate AI Response

        try:

            logger.info("New question received.")

            with st.chat_message("assistant"):

                with st.spinner("AI Agent is thinking..."):

                    answer = run_agent(question.strip())

                if answer:

                    st.markdown(answer)

                    st.session_state.chat_history.append({
                        "question": question.strip(),
                        "answer": answer
                    })

                    logger.info(
                        "Answer generated successfully."
                    )

                else:

                    st.error(
                        "Unable to generate an answer. "
                        "Please try again."
                    )

        except Exception:

            logger.exception(
                "AI Agent execution failed."
            )

            st.error(
                "Something went wrong. "
                "Please try again later."
            )