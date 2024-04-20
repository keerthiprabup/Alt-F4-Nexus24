from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.chains import RetrievalQA


DATA_PATH = "./PDFS"

model = Ollama(model="llama2")

def urlparser(urls):
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                    chunk_overlap=50,
                                                    length_function=len)
    
    all_splits = text_splitter.split_documents(docs_list)    
    faiss_db = FAISS.from_documents(all_splits, embeddings.OpenAIEmbeddings())

def pdfparser():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    pdfs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                    chunk_overlap=50,
                                                    length_function=len)
    all_splits = text_splitter.split_documents(pdfs)
    faiss_db = FAISS.from_documents(all_splits, embeddings.OpenAIEmbeddings())

def rag(question):
    
    template = """
                You are a professional expertise with acurate knowledge on mental health.
                Your job is to use the following context to answer questions about a how to take care of a mental patient.
                The context provided are from academic researches and are highly reliable. 
                Try to stick to the context as much as possible.
                The context is in a particular format but you should NOT mimic the style. 
                Always answer the question using normal language with emotion and sentiment.
                The user are people with possible mental conditions. So you can try to paraphrase the answer to make it more emotionally resonant to the user.
                At the end of your answer, include only the file name website link and page number of the source. For example: "Source: some_file.pdf,website.com,page 5".
                Context: {context}
                Chat history: {chat_history}
                Question: {question}
                Reply : 
                """
                
    pt = ChatPromptTemplate(template=template, input_variables=["context", "question"])
    # prompt_string = pt.render(context="", question=question, chat_history=chat_history)
    prompt_string = pt.render(context="", question=question) 

    
    rag = RetrievalQA.from_chain_type(
        llm=model,
        retriever=faiss_db.as_retriever(),
        memory=ConversationSummaryMemory(llm=Ollama(model=model)),
        chain_type_kwargs={"prompt": {"text": prompt_string}, "verbose": True}, 
    )
    
    # rag_chain = (
    # {"context": retriever    | format_docs, "question": RunnablePassthrough()}
    # | prompt
    # | llm
    # | StrOutputParser()
    # )
    response = rag.invoke(question)
    
    return response

question = "i have depression"
rag(question)
