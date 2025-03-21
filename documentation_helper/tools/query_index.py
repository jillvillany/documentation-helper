import os
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# configure client
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

index = pc.Index("lcel-text")

query = "what is LCEL?"
xq = embeddings.embed_query(query)

res = index.query(vector=xq, top_k=5, include_metadata=True)
for match in res["matches"]: print(match)
print()