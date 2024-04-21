from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader, PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.embeddings import OllamaEmbeddings, HuggingFaceEmbeddings, HuggingFaceBgeEmbeddings
from langchain_community.llms import Ollama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage
from langchain.chains import (
    RetrievalQA,
    create_retrieval_chain,
    create_history_aware_retriever,
    ConversationChain,
)
from langchain.memory import ConversationBufferMemory,ConversationSummaryMemory
import bs4
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community import embeddings
import streamlit as st
import  numpy as np
import streamlit as st


def rag(question):
    model = Ollama(model="llama2")

    huggingface_embeddings=HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device':'cpu'},
        encode_kwargs={'normalize_embeddings':True}

    )

    huggingface_embeddings.embed_query

    loader=PyPDFDirectoryLoader("C://Users//ajana//OneDrive//Desktop//local-model//New folder//Mental")

    documents=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

    final_documents=text_splitter.split_documents(documents)



    # conversation = ConversationChain(
    #     llm=model, verbose=True, memory=ConversationBufferMemory()
    # )

    prompt_template = """
                        SPEAK EMPATHETICALLY
                        you are my best friend and a person i can trust with all my feelings, you need to guide me though my mentalailment with an open mind
                        help me succeed in life and help  me become a better person, helpme upgarde to a better lifestyle, and take care of an anxious person like myself.
                        Your job is to use the following context to answer questions about a how to take care of the anxious person.
                        CONSIDER DATA FROM OUR PREVIOUS CONVERSATION
                        The context provided are from academic researches and are highly reliable.
                        The context is in a particular format but you SHOULD NOT mimic the style.
                        Always answer the question using normal language with emotion and sentiment.
                        START HAVING A CONVERSATION WITH ME.
                        “limit your response to 20 words” .
                        Context: {context}

                        """

    vectorstore=FAISS.from_documents(final_documents[:200],huggingface_embeddings)


        # prompt=PromptTemplate(template=template,input_variables=["context","question"])
        # prompt_string = prompt.render(context="", question=question)

    retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":3})

    prompt=PromptTemplate(template=prompt_template,input_variables=["context","question"])

    retrievalQA=RetrievalQA.from_chain_type(
        llm=model,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt":prompt}
    )


    result = retrievalQA.invoke({"query": question})
    # print(result['result'])
    return result['result']


