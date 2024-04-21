import streamlit as st
from rag_llama2 import rag

st.title("Saheli")

class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


if 'session' not in st.session_state:
    st.session_state.session = SessionState(conversation_history=[])

def format_conversation():
    markdown_text = "<div class='chat-container'>"
    for item in st.session_state.session.conversation_history:
        if item[0] == 'User':
            markdown_text += f"<div class='user-message'><b>You:</b> {item[1]}</div>"
        else:
            markdown_text += f"<div class='saheli-message'><b>Saheli:</b> {item[1]}</div>"
    markdown_text += "</div>"
    return markdown_text

st.markdown("""<style>
            .chat-container {
                height: 50vh;
                overflow-y: scroll;
                border: 1px solid #eaeaea;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            }
            .user-message {
                background-color: #DCF8C6;
                color: black;
                border-radius: 10px;
                padding: 8px 12px;
                margin: 6px 0;
                display: inline-block;
                max-width: 70%;
                clear: both;
                float: right;
            }
            .saheli-message {
                background-color: #EAE7E7;
                color: black;
                border-radius: 10px;
                padding: 8px 12px;
                margin: 6px 0;
                display: inline-block;
                max-width: 70%;
                clear: both;
                float: left;
            }
            </style>""", unsafe_allow_html=True)

st.markdown("<h2>Conversation History</h2>", unsafe_allow_html=True)
conversation_history = st.empty()
conversation_history.markdown(format_conversation(), unsafe_allow_html=True)


question = st.text_input("Type your message here", "")

if st.button("Send"):
    if question.strip():
        st.session_state.session.conversation_history.append(('User', question))
        response =  rag(question)
        st.session_state.session.conversation_history.append(('Saheli', response))
        conversation_history.markdown(format_conversation(), unsafe_allow_html=True)
