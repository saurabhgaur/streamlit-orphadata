"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message

from langchain.chains import ConversationChain
from langchain.llms import OpenAI

from langchain.agents import create_csv_agent
from langchain.llms import OpenAI


def load_agent():
    """Logic for loading the chain you want to use should go here."""
    agent = create_csv_agent(OpenAI(temperature=0), "./Orphanet-en_product4.csv", verbose=True)

    llm = OpenAI(temperature=0)
    return agent

agent = load_agent()

# From here down is all the StreamLit UI.
st.set_page_config(page_title="RGDs Search", page_icon=":robot:")
st.header("RGDs Search")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text


user_input = get_text()

if user_input:
    output = agent.run(user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
