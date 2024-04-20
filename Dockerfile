FROM langchain/langchain

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY frontend.py .
COPY rag.py .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/

CMD streamlit run frontend.py --server.port=8501 --server.address=0.0.0.0 || sleep infinity