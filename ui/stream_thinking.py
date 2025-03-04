import streamlit as st
import time
import re

def render_thinking_in_realtime(stream, message_placeholder):
    """
    Procesa la respuesta en streaming separando el contenido visible y el pensamiento,
    y renderiza en tiempo real el bloque de pensamiento.
    Retorna una tupla: (visible_text, thinking_text)
    """
    full_response = ""
    visible_text = ""
    thinking_text = ""
    thinking_container = st.empty()
    
    for chunk in stream:
        if chunk and 'message' in chunk and 'content' in chunk['message']:
            content_chunk = chunk['message']['content']
            full_response += content_chunk
            
            # Buscar el bloque <think> en la respuesta completa
            match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
            if match:
                thinking_text = match.group(1).strip()
                thinking_container.markdown(
                    f"<div style='background-color: #1E293B; border-left: 4px solid #3B82F6; padding: 10px; border-radius: 4px;'>"
                    f"<span style='color: #3B82F6; font-weight: bold;'>💭 Pensando en vivo:</span><br/>"
                    f"<span style='color: #E2E8F0;'>{thinking_text}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                thinking_container.empty()
            
            # Eliminar el bloque <think> para obtener el contenido visible
            visible_text = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
            message_placeholder.markdown(visible_text + "▌")
            time.sleep(0.01)
    
    message_placeholder.markdown(visible_text)
    thinking_container.empty()
    
    return visible_text, thinking_text
