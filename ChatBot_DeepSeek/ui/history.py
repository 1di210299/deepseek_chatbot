import streamlit as st
import uuid
from services.storage_service import (
    list_conversations, 
    load_conversation, 
    save_conversation, 
    delete_conversation
)

def render_history_management():
    """Renderiza la interfaz para gestionar el historial de conversaciones."""
    st.header("Conversation History")
    
    # --- Sección: Crear nueva conversación ---
    st.subheader("Start a New Conversation")
    new_name = st.text_input("Conversation Name", key="new_convo_name")
    
    if st.button("Create New Conversation"):
        current_id = st.session_state.conversation_id
        if st.session_state.messages and st.session_state.autosave:
            save_conversation(current_id, st.session_state.messages)
        
        # Crear una nueva conversación y asignar el nombre
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state["conversation_name"] = new_name if new_name else "(unnamed)"
        st.rerun()
    
    # --- Sección: Conversación actual ---
    st.subheader("Current Conversation")
    col1, col2 = st.columns([2, 1])
    current_id = st.session_state.conversation_id
    
    with col1:
        st.info(f"Conversation ID: {current_id}")
        autosave = st.toggle(
            "Autosave Conversation", 
            value=st.session_state.autosave,
            help="Automatically save conversation after each message"
        )
        if autosave != st.session_state.autosave:
            st.session_state.autosave = autosave
    
    with col2:
        if st.button("Save Conversation", use_container_width=True):
            success = save_conversation(current_id, st.session_state.messages)
            if success:
                st.success("Conversation saved successfully!")
            else:
                st.error("Failed to save conversation")
    
    # --- Sección: Listar conversaciones guardadas ---
    st.subheader("Saved Conversations")
    conversations = list_conversations()
    
    if conversations:
        for i, conv in enumerate(conversations):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Name:** {conv['name']}")
                    st.write(f"**ID:** {conv['id']}")
                    st.write(f"Last updated: {conv['last_updated']}")
                    st.write(f"Messages: {conv['message_count']}")
                with col2:
                    if st.button("Load", key=f"load_{i}", use_container_width=True):
                        messages = load_conversation(conv['id'])
                        if messages is not None:
                            if st.session_state.messages and st.session_state.autosave:
                                save_conversation(current_id, st.session_state.messages)
                            st.session_state.conversation_id = conv['id']
                            st.session_state.messages = messages
                            st.rerun()
                        else:
                            st.error("Failed to load conversation")
                    if st.button("Delete", key=f"delete_{i}", use_container_width=True):
                        success = delete_conversation(conv['id'])
                        if success:
                            st.success("Conversation deleted")
                            st.rerun()
                        else:
                            st.error("Failed to delete conversation")
    else:
        st.info("No saved conversations found")
