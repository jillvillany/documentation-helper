from dotenv import load_dotenv
load_dotenv()
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore


def run_llm(query:str, index_name:str):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)
    
    qa = create_retrieval_chain(
        docsearch.as_retriever(), combine_docs_chain=stuff_documents_chain
    )
    
    result = qa.invoke({"input": query})
    
    return result


if __name__ == "__main__":
    res = run_llm("what is lcel?", "langchain-doc-index")
    print()
    for doc in res["context"]: print(f"\n{doc.page_content}")
    print(res["answer"])