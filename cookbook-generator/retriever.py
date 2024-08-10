from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_together.embeddings import TogetherEmbeddings

embeddings = TogetherEmbeddings(model="togethercomputer/m2-bert-80M-8k-retrieval")

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
print("Scraped documents:", len(docs_list))
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=512, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

# Add to vectorDB
print("Adding to vectorstore")
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embeddings,
)
print("Added to vectorstore")
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
question = "few shot?"
docs = retriever.get_relevant_documents(question)
print(docs)
for d in docs:
    print(d.page_content)
doc_txt = docs[1].page_content
print(doc_txt)