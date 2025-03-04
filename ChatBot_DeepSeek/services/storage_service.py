import json
import os
from typing import List, Dict, Any
from datetime import datetime
import streamlit as st

# Directorio para almacenar el historial de conversaciones
STORAGE_DIR = "conversation_history"

def ensure_storage_dir():
    """Asegura que exista el directorio de almacenamiento"""
    os.makedirs(STORAGE_DIR, exist_ok=True)

def get_conversation_filename(conversation_id: str) -> str:
    """Obtiene la ruta completa para el archivo de una conversación"""
    return os.path.join(STORAGE_DIR, f"conversation_{conversation_id}.json")

def save_conversation(conversation_id: str, messages: List[Dict[str, Any]]) -> bool:
    """
    Guarda el historial de una conversación en un archivo JSON.
    
    Args:
        conversation_id: Identificador único de la conversación.
        messages: Lista de diccionarios de mensajes.
        
    Returns:
        True si se guarda correctamente, False en caso contrario.
    """
    ensure_storage_dir()
    
    try:
        # Crear una copia de los mensajes para no modificar el original
        messages_copy = []
        for msg in messages:
            msg_copy = msg.copy()
            if isinstance(msg_copy.get("content"), dict):
                thinking = msg_copy["content"].get("thinking")
                content = msg_copy["content"].get("content")
                if thinking:
                    msg_copy["content"] = f"<think>{thinking}</think>\n\n{content}"
                else:
                    msg_copy["content"] = content
            messages_copy.append(msg_copy)
        
        # Agregar metadatos, incluyendo el nombre de la conversación
        conversation_data = {
            "id": conversation_id,
            "last_updated": datetime.now().isoformat(),
            "name": st.session_state.get("conversation_name", "(unnamed)"),
            "messages": messages_copy
        }
        
        with open(get_conversation_filename(conversation_id), 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving conversation: {e}")
        return False

def load_conversation(conversation_id: str) -> List[Dict[str, Any]]:
    """
    Carga el historial de una conversación desde un archivo JSON.
    
    Args:
        conversation_id: Identificador único de la conversación.
        
    Returns:
        Lista de diccionarios de mensajes o lista vacía si no existe.
    """
    filename = get_conversation_filename(conversation_id)
    
    if not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            conversation_data = json.load(f)
        # Actualiza el nombre de conversación en session_state
        st.session_state["conversation_name"] = conversation_data.get("name", "(unnamed)")
        return conversation_data.get("messages", [])
    except Exception as e:
        print(f"Error loading conversation: {e}")
        return []

def list_conversations() -> List[Dict[str, Any]]:
    """
    Lista todas las conversaciones guardadas con sus metadatos.
    
    Returns:
        Lista de diccionarios con la información de cada conversación.
    """
    ensure_storage_dir()
    conversations = []
    
    for filename in os.listdir(STORAGE_DIR):
        if filename.startswith("conversation_") and filename.endswith(".json"):
            try:
                with open(os.path.join(STORAGE_DIR, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    conversations.append({
                        "id": data.get("id", "unknown"),
                        "name": data.get("name", "(unnamed)"),
                        "last_updated": data.get("last_updated", "unknown"),
                        "message_count": len(data.get("messages", [])),
                        "filename": filename
                    })
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    conversations.sort(key=lambda x: x.get("last_updated", ""), reverse=True)
    return conversations

def delete_conversation(conversation_id: str) -> bool:
    """
    Elimina una conversación guardada.
    
    Args:
        conversation_id: Identificador único de la conversación.
        
    Returns:
        True si se eliminó correctamente, False en caso contrario.
    """
    filename = get_conversation_filename(conversation_id)
    
    if not os.path.exists(filename):
        return False
    
    try:
        os.remove(filename)
        return True
    except Exception as e:
        print(f"Error deleting conversation: {e}")
        return False
