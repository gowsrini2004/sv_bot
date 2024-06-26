import os
import re
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import AzureChatOpenAI

# transforming documents
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer



def text_to_graph(text):
    file_path = "letters.txt"
    with open(file_path, 'a',encoding="utf-8") as file:
        file.write(text)
        file.write("\n\n")
    api_key = "c7bd04c72ba64ed8b4c5e5519b178e92"
    azure_endpoint = "https://azure-openai-llingam-prod.openai.azure.com/"
    api_version = '2024-02-01'

    NEO4J_URI = "neo4j+s://968f8227.databases.neo4j.io"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "KmeGE29jpmzj2q4m3TfBD1kwBK8ES4j7ieguOENnhgE"

    # Initialize the Neo4jGraph with correct parameters
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

    llm = AzureChatOpenAI(
        model="gpt-4",
        azure_deployment="gpt-4",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=api_version,
        temperature=0.0
    )

    # Initialize the LLMTransformer model
    llm_transformer = LLMGraphTransformer(llm=llm)

    documents = [Document(page_content=text)]
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    # print(f"Nodes: {graph_documents[0].nodes}")
    # print(f"Relationships: {graph_documents[0].relationships}")

    try:
        graph.add_graph_documents(
            graph_documents,
            baseEntityLabel=True,
            include_source=True
        )
        print("Graph created successfully.")
    except Exception as e:
        print(f"Error adding graph documents: {e}")