"""
This script uses the Julep API to create an AI agent, load and process documents,
generate a Python script based on a given task, and create a pull request on GitHub.

It demonstrates the use of LangChain for document processing and the Julep API for
AI-assisted code generation.
"""

from julep import Client
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from prompts import SYSTEM_PROMPT, PRE_GENERATION_PROMPT
from github_pr import develyn_raise_pr
from config import *
import os

def create_agent(client):
    """Create and return a Julep agent."""
    about = SYSTEM_PROMPT.format(company=COMPANY, project=PROJECT, project_description=PROJECT_DESCRIPTION)
    return client.agents.create(name=AGENT_NAME, about=about, model=AGENT_MODEL, metadata={"name": AGENT_NAME})

def load_and_split_documents():
    """Load documents from URLs and split them into chunks."""
    docs = WebBaseLoader(DOCUMENT_URLS).load()
    return RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100).split_documents(docs)

def create_document_chunks(client, agent_id, splits):
    """Create document chunks in Julep for the agent."""
    for i, split in enumerate(splits):
        client.docs.create(
            agent_id=agent_id,
            doc={
                "title": "Developer Relation Agent to help you generate high quality cookbooks and tutorials",
                "content": split.page_content,
                "metadata": {"chunk": i, **split.metadata},
            }
        )

def generate_code(client, agent_id):
    """Generate code using the Julep API."""
    session = client.sessions.create(agent_id=agent_id, situation=AGENT_SITUATION, metadata={"agent_id": agent_id})
    response = client.sessions.chat(
        session_id=session.id,
        messages=[{"role": "user", "content": PRE_GENERATION_PROMPT.format(project=PROJECT, task=TASK)}],
        max_tokens=4096
    )
    return response.response[0][0].content.split("```python")[1].split("```")[0].strip(), response.doc_ids

def main():
    client = Client(api_key=os.environ.get("JULEP_API_KEY"), base_url=os.environ.get("JULEP_API_URL"))
    
    agent = create_agent(client)
    splits = load_and_split_documents()
    create_document_chunks(client, agent.id, splits)
    
    python_code, doc_ids = generate_code(client, agent.id)
    
    with open(OUTPUT_FILE, "w") as f:
        f.write(python_code)
    
    print(f"{python_code}\n\nDocs used: {doc_ids}")
    print(develyn_raise_pr())

if __name__ == "__main__":
    main()