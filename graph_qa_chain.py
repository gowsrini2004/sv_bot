from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import AzureChatOpenAI
def graph_qa_chain(prompt):
    api_key = "c7bd04c72ba64ed8b4c5e5519b178e92"
    azure_endpoint = "https://azure-openai-llingam-prod.openai.azure.com/"
    api_version = '2024-02-01'

    # Neo4j connection parameters
    NEO4J_URI = "neo4j+s://968f8227.databases.neo4j.io"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "KmeGE29jpmzj2q4m3TfBD1kwBK8ES4j7ieguOENnhgE"
    graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)

    llm = AzureChatOpenAI(
        model="gpt-4",
        azure_deployment="gpt-4",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=api_version,
        temperature=0.0
    )
    chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
    query = {"query": prompt}
    ai_message = chain.invoke(query)
    response = ai_message["result"]
    return  response