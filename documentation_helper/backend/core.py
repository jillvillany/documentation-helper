from dotenv import load_dotenv
load_dotenv()
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain import hub
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.vectorstores import FAISS

# index_name = "langchain-doc-index"
# index_name = "langchain-old-doc-index"
# index_name = "lcel-text"

def run_llm(query:str, chat_history=[]):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name="langchain-old-doc-index", embedding=embeddings)
    # docsearch = FAISS.load_local(
    #     "faiss_index", embeddings, allow_dangerous_deserialization=True
    # )
    chat = ChatOpenAI(verbose=True, temperature=0)
    
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)
    
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware_retriever = create_history_aware_retriever(llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt)
    
    qa = create_retrieval_chain(
        history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )
    
    result = qa.invoke({"input": query, "chat_history": chat_history})
    formatted = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }
    
    return formatted


if __name__ == "__main__":
    res = run_llm("what is LCEL?")
    print()
    for doc in res["source_documents"]: print(f"\nDOCUMENT BREAK ----------\n{doc.page_content}")
    print(f"\n\n{res['result']}")