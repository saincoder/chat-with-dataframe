import pandas as pd
import streamlit as st
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_ollama import ChatOllama


# streamlit web app configuration

st.set_page_config(
    page_icon="💭",
    page_title="DF chatbot",
    layout='centered'
)

# function for read the two different file
def read_data(file):
    if file.name.endwith('.csv'):
        return pd.read_csv(file)
    
    else:
        pd.read_excel(file)

# title
st.title('🤖 DataFrame Chatbot -Ollama')


# Initialize chat history in streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []