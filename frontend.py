<<<<<<< HEAD
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
=======
>>>>>>> 3e7d843dd28c8d0fd7ef47734353d684b76d8bd5
import streamlit as st
from rag_llama2 import rag

st.title("Saheli")

question = st.text_input("Hey, how are you?")

<<<<<<< HEAD
if st.button("Query Documents"):
    with st.spinner('Processing ---'):
        answer = process_input(urls,question)
        st.text_area("Answer",value=answer,height=300,disabled=True)
        
>>>>>>> 988ba2e7162e9d8b22a6c543a46f35cd98e58879
=======
if question:
    response = rag(question)
    st.markdown(response)
>>>>>>> 3e7d843dd28c8d0fd7ef47734353d684b76d8bd5
