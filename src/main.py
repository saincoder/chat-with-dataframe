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
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    
    else:
        pd.read_excel(file)

# title
st.title('🤖 DataFrame Chatbot -Ollama')


# Initialize chat history in streamlit session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Initiate dataframe in session state
if "df" not in st.session_state:
    st.session_state.df = None


# file uploaded widget

file_uploaded = st.file_uploader("Choose a file:", type=["csv", "xlsx", "xls"])

if file_uploaded:
    st.session_state.df = read_data(file_uploaded)
    st.write('DataFrame Preview')
    st.dataframe(st.session_state.df.head())


# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


# Input field for user prompt
user_prompt = st.chat_input('Enter your prompt here')

# Add user prompts to chat history

if user_prompt:
    st.chat_message('user').markdown(user_prompt)
    st.session_state.chat_history.append({"role" : "user","content" : user_prompt})


# load the LLM
llm = ChatOllama(model='gemma:2b', temperature=0)
pandas_df_agent = create_pandas_dataframe_agent(
    llm,
    st.session_state.df,
    verbose=2,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    allow_dangerous_code=True
)