from neo4j import GraphDatabase
import networkx as nx
import time
from pyvis.network import Network
import os  # Import os for file operations
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # To automatically manage ChromeDriver

# Define the default Cypher query
default_cypher = "MATCH (n) RETURN n"

# Define connection details
uri = "neo4j+s://968f8227.databases.neo4j.io"
username = "neo4j"
password = "KmeGE29jpmzj2q4m3TfBD1kwBK8ES4j7ieguOENnhgE"

def fetch_graph(cypher: str = default_cypher):
    # Create a driver instance
    driver = GraphDatabase.driver(uri, auth=(username, password))

    def get_relationships(tx):
        result = tx.run("MATCH (n)-[r]->(m) RETURN n, r, m")
        relationships = []
        for record in result:
            relationships.append((record['n'].id, record['m'].id, record['r'].type))
        return relationships

    # Create a session
    with driver.session() as session:
        # Run the Cypher query to get nodes
        result = session.run(cypher)

        # Convert the Neo4j result to NetworkX graph
        G = nx.DiGraph()
        for record in result:
            node = record['n']
            node_id = node.get('id')  # Fetch the 'id' property
            # Add the node to the graph with the 'id' as the label
            G.add_node(node.id, label=node_id)

        # Get relationships
        with driver.session() as session:
            relationships = session.execute_read(get_relationships)
            for source, target, rel_type in relationships:
                G.add_edge(source, target, label=rel_type)

    return G

def create_pyvis_network(G):
    # Define the HTML file name
    html_file = 'graph.html'

    # Delete the old HTML file if it exists
    if os.path.exists(html_file):
        os.remove(html_file)

    # Create a Network object
    net = Network(notebook=False, height='100vh', width='100vw', bgcolor='#f0f0f0', font_color='white', directed=True)

    # Add nodes and edges to the Network object
    for node, data in G.nodes(data=True):
        net.add_node(node, label=data['label'], color={'background': 'black', 'border': '#0074D9'}, borderWidth=2, size=20, shape='circle',
                     font=dict(size=14, color='white', face='bold'))

    for source, target, data in G.edges(data=True):
        net.add_edge(source, target, label=f"{data.get('label', '')}", color='#888888', arrows='to', font=dict(size=20, color='black'))

    # Set the physics layout to be more dynamic and fit the graph into the page
    net.force_atlas_2based()
    net.show_buttons(filter_=['physics'])

    # Save the Network as an HTML file
    net.save_graph(html_file)

    # Debug: Print the HTML file path to check if it is correct
    print(f"HTML file saved as: {html_file}")

    return html_file

def open_html_in_chrome(html_file):
    # Set up Chrome options for full screen mode
    options = Options()
    options.add_argument('--start-maximized')  # Open Chrome in full screen
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    # Initialize the Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Ensure the file path is correct
    file_path = f'file://{os.path.abspath(html_file)}'
    print(f"Opening file path: {file_path}")  # Debug: Print the file path
    driver.get(file_path)

    # Wait for the graph to load by checking if a specific element (e.g., the graph container) is present
    try:
        # Wait until the graph container div is present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#network'))  # Ensure `#network` div is loaded
        )

        # Explicit wait to ensure the graph has fully rendered
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return window.getComputedStyle(document.querySelector('#network')).display") == 'block'
        )
    except Exception as e:
        print(f"Error waiting for the graph to load: {e}")

    # Keep the browser open for 10 minutes
    time.sleep(600)  # Sleep for 600 seconds (10 minutes)

def main(cypher: str = default_cypher):
    G = fetch_graph(cypher)
    html_file = create_pyvis_network(G)
    open_html_in_chrome(html_file)

# Call the function to display the graph
if __name__ == "__main__":
    main()