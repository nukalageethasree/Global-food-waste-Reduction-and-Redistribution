"""AI Chat Assistant page — powered by HuggingFace via backend."""
import streamlit as st
from utils.api import api_post

SUGGESTIONS = [
    "What food listings are expiring soon?",
    "How can I reduce food waste at my restaurant?",
    "What's my current impact on reducing food waste?",
    "How does the AI matching system work?",
    "Tips for creating better food listings",
    "How do I approve a food request?",
]

def show_chat():
    st.markdown("""
    <div class="hero-banner">
      <h1>🤖 AI Chat Assistant</h1>
      <p>Powered by HuggingFace (Mistral-7B) — Ask anything about food waste reduction, listings, and the platform.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Init chat history ──────────────────────────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state.chat_history:
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": "👋 Hi! I'm FoodShare AI, powered by HuggingFace. I can help you find food donations, reduce waste, and navigate the platform. How can I help you today?"
        }]

    # ── Chat layout ────────────────────────────────────────────────────────
    col_chat, col_sidebar = st.columns([3, 1])

    with col_chat:
        # Display chat history
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-end;margin:6px 0;">
                  <div class="chat-user">{msg['content']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex;justify-content:flex-start;margin:6px 0;">
                  <div class="chat-ai">🤖 {msg['content']}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Input area ───────────────────────────────────────────────────────
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Ask FoodShare AI…",
                placeholder="Type your message here…",
                label_visibility="collapsed"
            )
            send_col, clear_col = st.columns([4, 1])
            with send_col:
                send = st.form_submit_button("Send ➤", use_container_width=True, type="primary")
            with clear_col:
                clear = st.form_submit_button("Clear", use_container_width=True)

        if clear:
            st.session_state.chat_history = [{
                "role": "assistant",
                "content": "Chat cleared! How can I help you today?"
            }]
            st.rerun()

        if send and user_input.strip():
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Call backend AI
            history_for_api = [
                {"role": m["role"] if m["role"] != "assistant" else "assistant",
                 "content": m["content"]}
                for m in st.session_state.chat_history[:-1]
            ]

            with st.spinner("FoodShare AI is thinking…"):
                data, code = api_post("/dashboard/chat", {
                    "message": user_input,
                    "history": history_for_api[-8:]
                })

            if code == 200:
                reply = data.get("reply", "I couldn't generate a response. Please try again.")
            else:
                reply = "⚠️ I'm having trouble connecting to the AI. Make sure your HuggingFace token is configured."

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

    with col_sidebar:
        st.markdown("#### 💬 Quick Questions")
        for i, suggestion in enumerate(SUGGESTIONS):
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": suggestion})
                with st.spinner("Thinking…"):
                    data, code = api_post("/dashboard/chat", {
                        "message": suggestion,
                        "history": st.session_state.chat_history[-6:]
                    })
                reply = data.get("reply","") if code == 200 else "⚠️ Connection error."
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

        st.markdown("---")
        st.markdown("#### 🤖 About This AI")
        st.markdown("""
        <div class="ai-box">
        <p>Powered by <strong>HuggingFace</strong><br>
        Model: <strong>Mistral-7B-Instruct</strong><br><br>
        This AI is trained to help with:<br>
        • Food waste reduction tips<br>
        • Platform navigation<br>
        • Donation best practices<br>
        • Impact insights
        </p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"**Messages:** {len(st.session_state.chat_history)}")
