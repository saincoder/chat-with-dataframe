import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama

# Streamlit web app configuration
st.set_page_config(
    page_title="DataFrame Chat",
    page_icon="💬",
    layout="centered"
)

# Developer Information



def read_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

# Streamlit page title
st.title("🤖 DataFrame ChatBot - Ollama")
st.write("Developer Shahid Hussain")

# Initialize chat history in Streamlit session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize DataFrame in session state
if "df" not in st.session_state:
    st.session_state.df = None

# File upload widget
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file:
    st.session_state.df = read_data(uploaded_file)
    st.write("DataFrame Preview:")
    st.dataframe(st.session_state.df.head())

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Enter your prompt.✨")

if user_prompt:
    # Add user's message to chat history and display it
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Load the LLM
    llm = ChatOllama(model="gemma:2b", temperature=0)

    # Create a Pandas DataFrame agent
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        st.session_state.df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )

    # Prepare the messages for the agent
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    # Get the response from the agent
    response = pandas_df_agent.invoke(messages)
    assistant_response = response["output"]

    # Add the assistant's response to chat history and display it
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
