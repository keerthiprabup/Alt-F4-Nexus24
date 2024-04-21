from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community import embeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders.pdf import PyPDFDirectoryLoader

model = Ollama(model="llama2")
## Langmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
if "LANGCHAIN_API_KEY" not in os.environ:
    os.environ["LANGCHAIN_API_KEY"] = "ls__39755c2f2a0444c2ae5e494392f32ec9"

loader = WebBaseLoader(
    web_paths=("https://en.wikipedia.org/wiki/Cristiano_Ronaldo",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OllamaEmbeddings())
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)



contextualize_template = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_template = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_template),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
   model, retriever, contextualize_template
)


template = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

{context}"""
prompt=ChatPromptTemplate.from_messages(
    [
        ("system",template),
        MessagesPlaceholder(variable_name="conversation")
        ("user","Question:{question}")
    ]
)

convo_chain = create_stuff_documents_chain(model, template)
rag_chain = create_retrieval_chain(history_aware_retriever, convo_chain)
chat_history = []
question = "who is ronaldo ?"
ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})
chat_history.extend([HumanMessage(content=question), ai_msg_1["answer"]])

second_question = "what is his networth?"
ai_msg_2 = rag_chain.invoke({"input": second_question, "chat_history": chat_history})

