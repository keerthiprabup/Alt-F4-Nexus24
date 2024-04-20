from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader

model1 = Ollama(model="mistral")
model2 = Ollama(model="llama2")

urls = open("./URL_list.txt")

# print(file.read())

def urlparser(urls):
    urls_list = urls.split(",")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                    chunk_overlap=50,
                                                    length_function=len)
    
    all_splits = text_splitter.split_documents(docs_list)    
    vector_db = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())
    
def pdfparser():
    loader = PyPDFDirectoryLoader(DATA_PATH)
    pdfs = loader.load()
    # print(f"Processed {len(pdfs)} pdf files")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, 
                                                    chunk_overlap=50,
                                                    length_function=len)
    all_splits = text_splitter.split_documents(pdfs)
    vector_db = Chroma.from_documents(documents=all_splits,embedding=GPT4AllEmbeddings())

def rag(urls, pdfs , question , chat_history):
    
    
    template = """
                You are a professional expertise with acurate knowledge on mental health.
                Your job is to use the following context to answer questions about a how to take care of a baby.
                The context provided are from academic researches and are highly reliable. 
                You should try to stick to the context as much as possible.
                The context is in a particular format but you should NOT mimic the style. 
                You should always answer the question using normal language with emotion and sentiment.
                The user are people with possible mental conditions. So you can try to paraphrase the answer to make it more emotionally resonant to the user.
                At the end of your answer, include only the file name website link and page number of the source. For example: "Source: some_file.pdf,website.com,page 5".
                Context: {context}
                Chat history: {chat_history}
                Question: {question}
                Here is the answer:
                """
                
    pt = PromptTemplate(template=template, input_variables=["context", "question"])
    prompt_str = pt(context="", question=question) 
    
    
    rag = RetrievalQA.from_chain_type(
        llm=model,
        retriever=vector_db.as_retriever(),
        memory=ConversationSummaryMemory(llm=Ollama(model="mistral")),
        chain_type_kwargs={"prompt": {"text": prompt_str}, "verbose": True}, 
    )
    
    
    response = rag.invoke(question)
    
    return response
