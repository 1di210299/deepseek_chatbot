import streamlit as st
from config.settings import WELCOME_MESSAGE, INSTRUCTIONS

def render_instructions():
    """
    Display welcome message and instructions for new users
    """
    st.info(WELCOME_MESSAGE)
    st.markdown(INSTRUCTIONS)