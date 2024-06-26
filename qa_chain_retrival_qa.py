from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain_community.chat_models import AzureChatOpenAI
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain.schema import Document
# from langchain.vectorstores import Neo4jVector


# Set Neo4j credentials and Azure OpenAI API details
NEO4J_URI = "neo4j+s://968f8227.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "KmeGE29jpmzj2q4m3TfBD1kwBK8ES4j7ieguOENnhgE"

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    api_key="671a912f57384b4c957d2e6f126b1487",
    azure_endpoint="https://iawake.openai.azure.com/",
    openai_api_version="2024-02-15-preview",
)

llm = AzureChatOpenAI(
    openai_api_version='2024-02-15-preview',
    deployment_name='gpt-4o',
    temperature=0,
    openai_api_key='671a912f57384b4c957d2e6f126b1487',
    openai_api_base="https://iawake.openai.azure.com/"
)
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
print(graph)

with open('letters.txt', 'r', encoding='utf-8') as file:
    raw_text = file.read()

document = Document(page_content=raw_text)

text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
documents = text_splitter.split_documents([document])

# for doc in documents:
#     print(doc.page_content)

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

