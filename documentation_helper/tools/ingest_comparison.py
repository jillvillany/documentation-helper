import os
from dotenv import load_dotenv
load_dotenv()
import time
from pinecone import Pinecone
import documentation_helper.utils as utils
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import TokenTextSplitter



def ingest_docs():
    def metadata_func(record: dict, metadata: dict) -> dict:
        # change source to url from the json fp and remove unneeded seq_num for what item in json fp it's from
        return {"source": record.get("url")}
    
    # delete existing records
    try:
        pc = Pinecone()
        pc.Index(name="lcel-md").delete(delete_all=True)
    except:
        pass
    
    try:
        pc.Index(name="lcel-text").delete(delete_all=True)
    except:
        pass
        
    options = [("output/lcel_md.json", "lcel-md"), ("output/lcel_text.json", "lcel-text")]
    
    for fp, index_name in options:
        start = time.time()
        
        loader = JSONLoader(
            file_path=fp,
            jq_schema=".docs[]",
            content_key="content",
            metadata_func=metadata_func
        )

        raw_docs = loader.load()
        
        print(f"Loaded {len(raw_docs)} docs")
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
        # text_splitter = TokenTextSplitter(chunk_size=200, chunk_overlap=10)
        documents = text_splitter.split_documents(raw_docs)

        print(f"Going to add {len(documents)} to Pinecone")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
        print("Complete!")
    
        end = time.time()
        hours, minutes, seconds = utils.convert_seconds(end - start)
        print(f"Ingested {len(documents)} docs in {hours}h {minutes}m {seconds}s")


if __name__ == "__main__":
    ingest_docs()