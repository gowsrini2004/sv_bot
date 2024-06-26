import streamlit as st
from text_to_graph import text_to_graph
from graph_qa_chain import graph_qa_chain
from graph_rag import graph_rag

def main():
    # Initialize session state variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.session_state.page = 'login'
        st.session_state.username = None  # Initialize username variable
        st.session_state.messages = []  # Initialize messages for graph_qa_chain page
        st.session_state.method_type = None

    # Navigation
    if st.session_state.page == 'login':
        login_page()
    elif st.session_state.page == 'user':
        user_page()
    elif st.session_state.page == 'admin':
        admin_page()
    elif st.session_state.page == 'letter_input':
        letter_input_page()
    elif st.session_state.page == 'sv_bot':
        sv_bot()

def login_page():
    st.title("Login Page")

    # Username and password inputs
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "user" and password == "user":
            st.session_state.authenticated = True
            st.session_state.user_type = 'user'
            st.session_state.username = username  # Store username in session state
            st.session_state.page = 'user'
            st.experimental_rerun()
        elif username == "admin" and password == "admin":
            st.session_state.authenticated = True
            st.session_state.user_type = 'admin'
            st.session_state.username = username  # Store username in session state
            st.session_state.page = 'admin'
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def user_page():
    st.title("User Page")

    # Display username
    st.write(f"Logged in as: {st.session_state.username}")

    # Example user-specific content
    st.write("Welcome, user!")

    # Only GraphCypherQAChain button for user
    if st.button("GraphCypherQAChain"):
        st.session_state.method_type = 'GraphCypherQAChain'
        st.session_state.page = 'sv_bot'
        st.experimental_rerun()

    # Logout button at the bottom of the page
    if st.button("Logout", key='user_logout'):
        logout()

def admin_page():
    st.title("Admin Page")

    # Display username
    st.write(f"Logged in as: {st.session_state.username}")

    # Horizontal layout for buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("QAChain+RetrivalQA", key='qa_chain_retrieval_qa'):
            st.session_state.method_type = 'QAChain+RetrivalQA'
            st.session_state.page = 'sv_bot'
            st.experimental_rerun()
    with col2:
        if st.button("GraphCypherQAChain", key='graph_cypher_qa_chain'):
            st.session_state.method_type = 'GraphCypherQAChain'
            st.session_state.page = 'sv_bot'
            st.experimental_rerun()
    with col3:
        if st.button("GraphRAG", key='graph_rag'):
            st.session_state.method_type = 'GraphRAG'
            st.session_state.page = 'sv_bot'
            st.experimental_rerun()

    if st.button("Enter Letter", key='enter_letter'):
        st.session_state.page = 'letter_input'
        st.experimental_rerun()
    if st.button("Go to User Page", key='go_to_user'):
        st.session_state.page = 'user'
        st.experimental_rerun()

    # Logout button at the bottom of the page
    if st.button("Logout", key='admin_logout'):
        logout()

def letter_input_page():
    st.title("Enter Letter")
    st.write("Please enter the Letter text below:")

    st.session_state.long_input = st.text_area("Letter", height=300)  # Increase the height here

    if st.button("Submit"):
        # Display a temporary success message
        success_message = st.empty()
        with st.spinner("Creating graph..."):
            result = text_to_graph(st.session_state.long_input)  # Call the external function
            success_message.success("Graph created successfully.")
        # Redirect back to admin page after graph creation
        st.session_state.page = 'admin'
        st.experimental_rerun()

    if st.button("Back to Admin Page"):
        st.session_state.page = 'admin'
        st.experimental_rerun()

def sv_bot():


    # Dynamic title based on the button clicked
    st.title(st.session_state.method_type)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What is up?")

    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner('Processing...'):
            if st.session_state.method_type == "GraphCypherQAChain":
                response = graph_qa_chain(prompt)
            elif st.session_state.method_type == "GraphRAG":
                response = graph_rag(prompt)
            elif st.session_state.method_type == "QAChain+RetrivalQA":
                response = "No Link"
            else:
                response = "No Link"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    # Navigation back to user or admin page
    if st.button("Go Back"):
        if st.session_state.user_type == "user":
            st.session_state.page = 'user'
            st.session_state.messages = []
        elif st.session_state.user_type == "admin":
            st.session_state.page = 'admin'
            st.session_state.messages = []
        st.experimental_rerun()

def logout():
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.page = 'login'
    st.experimental_rerun()

if __name__ == "__main__":
    main()