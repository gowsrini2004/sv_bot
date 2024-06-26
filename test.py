default_cypher = "MATCH (s)-[r:!MENTIONS]->(t) RETURN s,r,t LIMIT 50"
def showGraph(cypher: str = default_cypher):
# create a neo4j session to run queries
    driver = GraphDatabase.driver(
    uri = os.environ["NEO4J_URI"],
    auth = (os.environ["NEO4J_USERNAME"],
    os.environ["NEO4J_PASSWORD"]))
    session = driver.session()
    widget = GraphWidget(graph = session.run(cypher).graph())
    widget.node_label_mapping = 'id'
    #display(widget)
    return widget

showGraph()