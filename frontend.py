<<<<<<< HEAD
import streamlit as st
from rag_llama2 import rag

st.title("Saheli")

question = st.text_input("Hey, how are you?")

if question:
    response = rag(question)
    st.markdown(response)
=======
from rag import rag
import streamlit as st

st.title("WebRAG with Ollama")
st.write("Enter URLs (line by line) and a question to query the documents.")

urls = st.text_area("Enter URL's seperated by new lines" , height = 200)
question = st.text_input("Question")

if st.button("Query Documents"):
    with st.spinner('Processing ---'):
        answer = process_input(urls,question)
        st.text_area("Answer",value=answer,height=300,disabled=True)
        
>>>>>>> 988ba2e7162e9d8b22a6c543a46f35cd98e58879
