from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain_core.documents import Document

with open('letters.txt', 'r',encoding="utf-8") as file:
    text = file.read()

NEO4J_URI = "neo4j+s://968f8227.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "KmeGE29jpmzj2q4m3TfBD1kwBK8ES4j7ieguOENnhgE"
documents = [Document(page_content=text)]

embeddings = AzureOpenAIEmbeddings(
model="text-embedding-ada-002",
api_key="671a912f57384b4c957d2e6f126b1487",
azure_endpoint="https://iawake.openai.azure.com/",
openai_api_version="2024-02-15-preview",
)

vector_index = Neo4jVector.from_existing_graph(
    url = NEO4J_URI,
    username = NEO4J_USERNAME,
    password = NEO4J_PASSWORD,
    embedding=embeddings,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

query = "Who is alasinga"
results = vector_index.similarity_search(query, k=5)
print(results[0].page_content)