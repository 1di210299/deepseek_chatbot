import streamlit as st
from services.ollama_service import get_available_models
from utils.helpers import get_model_index
from config.settings import (
    SIDEBAR_HEADER, 
    SIDEBAR_FOOTER, 
    DEFAULT_TEMPERATURE,
    CLEAR_BUTTON_TEXT,
    NO_MODELS_ERROR,
    MODEL_INSTALL_INSTRUCTION,
    CONNECTION_ERROR,
    DEFAULT_MODEL
)

def render_sidebar():
    """Render the sidebar with model selection and other settings"""
    with st.sidebar:
        st.header(SIDEBAR_HEADER)
        
        # Model selection
        try:
            model_names = get_available_models()
            
            # Always ensure the default model is in the list
            if DEFAULT_MODEL not in model_names:
                model_names.append(DEFAULT_MODEL)
            
            # Get current model index
            current_model_index = get_model_index(model_names, st.session_state.model)
            
            # Model selection dropdown
            selected_model = st.selectbox(
                "Select a model",
                options=model_names,
                index=current_model_index
            )
            st.session_state.model = selected_model
            
            if len(model_names) == 1 and model_names[0] == DEFAULT_MODEL:
                st.info(f"Using model: {DEFAULT_MODEL}")
                st.info("If you have other models installed, they should appear here.")
        except Exception as e:
            st.error(f"Error connecting to Ollama: {e}")
            st.error(CONNECTION_ERROR)
            st.error(f"Using DeepSeek model: {DEFAULT_MODEL}")
            st.session_state.model = DEFAULT_MODEL
        
        # Temperature slider
        temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=2.0, 
            value=DEFAULT_TEMPERATURE, 
            step=0.1
        )
        st.session_state.temperature = temperature
        
        # Clear conversation button
        if st.button(CLEAR_BUTTON_TEXT):
            st.session_state.messages = []
            st.rerun()
        
        # Footer
        st.markdown("---")
        st.markdown(SIDEBAR_FOOTER)