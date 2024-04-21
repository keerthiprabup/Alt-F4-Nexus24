import streamlit as st
from rag_llama2 import rag

st.title("Saheli")

question = st.text_input("Hey, how are you?")

if question:
    response = rag(question)
    st.markdown(response)
