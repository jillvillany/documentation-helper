import os
from dotenv import load_dotenv
load_dotenv()
import time
import documentation_helper.utils as utils
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


def ingest_docs():
    start = time.time()
    
    def metadata_func(record: dict, metadata: dict) -> dict:
        # change source to url from the json fp and remove unneeded seq_num for what item in json fp it's from
        return {"source": record.get("url")}
    
    loader = JSONLoader(
        file_path='output/doc_sample.json',
        jq_schema=".docs[]",
        content_key="page_content",
        metadata_func=metadata_func
    )

    raw_docs = loader.load()
    
    print(f"Loaded {len(raw_docs)} docs")
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(raw_docs)

    print(f"Going to add {len(documents)} to Pinecone")
    embeddings = OpenAIEmbeddings()
    PineconeVectorStore.from_documents(documents, embeddings, index_name="langchain-sample")
    print("Complete!")
    
    end = time.time()
    hours, minutes, seconds = utils.convert_seconds(end - start)
    print(f"Ingested {len(documents)} docs in {hours}h {minutes}m {seconds}s")


if __name__ == "__main__":
    ingest_docs()