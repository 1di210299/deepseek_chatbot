import streamlit as st
import os
import uuid
from ui.sidebar import render_sidebar  # Asegúrate de que render_sidebar() no ejecute comandos a nivel global
from ui.chat import render_chat_interface
from ui.instructions import render_instructions
from ui.history import render_history_management
from config.settings import APP_TITLE, APP_DESCRIPTION, PAGE_ICON
from services.storage_service import load_conversation, save_conversation

# Esta llamada debe ser la primera instrucción de Streamlit en el script
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=PAGE_ICON,
    layout="wide"
)

# Crear directorios si no existen (opcional)
os.makedirs('config', exist_ok=True)
os.makedirs('services', exist_ok=True)
os.makedirs('utils', exist_ok=True)
os.makedirs('ui', exist_ok=True)

def init_app():
    """Inicializa variables y configura la sesión."""
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    
    if "messages" not in st.session_state:
        messages = load_conversation(st.session_state.conversation_id)
        st.session_state.messages = messages if messages else []
    
    if "model" not in st.session_state:
        st.session_state.model = "deepseek-r1:14b"
        
    if "show_thinking" not in st.session_state:
        st.session_state.show_thinking = True
        
    if "autosave" not in st.session_state:
        st.session_state.autosave = True

def main():
    init_app()
    
    st.title(APP_TITLE)
    st.markdown(APP_DESCRIPTION)
    
    # --- Navegación en la barra lateral ---
    st.sidebar.title("Navigation")
    # Llama a render_sidebar() si lo deseas (asegúrate de que no ejecute comandos de Streamlit en el nivel global)
    page = st.sidebar.radio("Go to", ["Chat", "History Management"])
    
    if page == "Chat":
        st.header("Chat")
        render_chat_interface()  # Aquí se llama la interfaz de chat
        if not st.session_state.messages:
            render_instructions()
    elif page == "History Management":
        st.header("History Management")
        render_history_management()
    
    # Guardar conversación si autosave está habilitado
    if st.session_state.autosave and st.session_state.messages:
        save_conversation(st.session_state.conversation_id, st.session_state.messages)

if __name__ == "__main__":
    main()
