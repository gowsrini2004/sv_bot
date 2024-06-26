import os
from neo4j import GraphDatabase
from langchain.chat_models import AzureChatOpenAI

# Set up the Azure OpenAI Chat model
llm = AzureChatOpenAI(
    openai_api_version='2024-02-15-preview',
    deployment_name='gpt-4o',
    temperature=0,
    openai_api_key='671a912f57384b4c957d2e6f126b1487',
    openai_api_base="https://iawake.openai.azure.com/"
)

NEO4J_URI = "neo4j+s://968f8227.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "KmeGE29jpmzj2q4m3TfBD1kwBK8ES4j7ieguOENnhgE"

# Create a connection to the Neo4j database
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))


def graph_rag(prompt):
    def get_from_gpt(messages):
        ai_message = llm.invoke(messages)
        return ai_message.content

    def execute_cypher_query(query):
        def run_query(driver, query):
            with driver.session() as session:
                result = session.run(query)
                return [record.data() for record in result]

        result = run_query(driver, query)
        return result

    def from_neo4j():
        def get_all_nodes(driver):
            query = """
            MATCH (n)
            RETURN elementId(n) as nodeId, labels(n) as labels, properties(n) as properties
            """
            with driver.session() as session:
                result = session.run(query)
                return [record.data() for record in result]

        def get_all_relationships(driver):
            query = """
            MATCH ()-[r]->()
            RETURN elementId(r) as relationshipId, type(r) as type, properties(r) as properties, 
                   elementId(startNode(r)) as startNodeId, elementId(endNode(r)) as endNodeId
            """
            with driver.session() as session:
                result = session.run(query)
                return [record.data() for record in result]

        # Fetch all nodes and relationships
        nodes = get_all_nodes(driver)
        relationships = get_all_relationships(driver)

        # Combine nodes and relationships into a single variable
        graph_data = {
            "nodes": nodes,
            "relationships": relationships
        }

        return graph_data

    # Fetch the graph data
    graph_data = from_neo4j()

    # Construct the message to send to the LLM
    message = f"{prompt}, write the Cypher query to find this from my Neo4j graph with context with below nodes and relations, with return statement, {graph_data}"

    # Get the Cypher query from GPT
    cypher_query_response = get_from_gpt(message)

    # Extract the Cypher query from the response
    cypher_query = ""
    inside_code_block = False
    for line in cypher_query_response.split('\n'):
        if line.strip().startswith("```cypher"):
            inside_code_block = True
            continue
        if line.strip().startswith("```"):
            inside_code_block = False
            continue
        if inside_code_block:
            cypher_query += line + "\n"

    cypher_query = cypher_query.strip()

    # Execute the Cypher query and print the result
    result = execute_cypher_query(cypher_query)

    message = f"now make this into a meaningful sentence, Question given by user: {prompt}, Cypher output got from graph: {result}"
    response = get_from_gpt(message)
    driver.close()
    return response