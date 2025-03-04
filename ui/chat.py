import streamlit as st
import time
import re
from services.ollama_service import generate_chat_response
from utils.helpers import format_error_message
import base64
import os

def encode_image_to_base64(image_path):
    """Convierte la imagen local en un string codificado en Base64."""
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode("utf-8")

def get_avatar(image_path, fallback_url, mime_type='png'):
    """
    Retorna el string Base64 si la imagen existe localmente, o la URL de respaldo si no.
    
    :param image_path: Ruta local de la imagen.
    :param fallback_url: URL pública para usar en caso de que la imagen no exista localmente.
    :param mime_type: Tipo de imagen ('png', 'jpeg', etc.).
    """
    if os.path.exists(image_path):
        encoded = encode_image_to_base64(image_path)
        return f"data:image/{mime_type};base64,{encoded}"
    else:
        return fallback_url

def render_chat_interface():
    """Muestra el historial y el campo de entrada al final."""
    render_chat_messages()
    
    user_input = st.chat_input("Pregunta algo...")
    if user_input:
        handle_user_input(user_input)

def render_chat_messages():
    """
    Recorre st.session_state.messages y muestra los mensajes con un avatar personalizado para cada rol.
    """
    # Rutas locales de las imágenes
    user_image_path = "images/user.png"
    assistant_image_path = "images/deepseek.jpeg"

    # URLs de respaldo en caso de que las imágenes locales no existan (deben ser públicas)
    fallback_user_url = "https://via.placeholder.com/150?text=User"
    fallback_assistant_url = "https://via.placeholder.com/150?text=Assistant"

    # Obtén el avatar usando la función get_avatar (local si existe, sino fallback)
    user_avatar_url = get_avatar(user_image_path, fallback_user_url, mime_type='png')
    assistant_avatar_url = get_avatar(assistant_image_path, fallback_assistant_url, mime_type='jpeg')

    # Inicializa el historial de mensajes si aún no existe
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "user", "content": "Hola, chatbot."},
            {"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte hoy?"}
        ]

    # Recorre y muestra cada mensaje, asignando el avatar correspondiente
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg.get("content", "")
        thinking = msg.get("thinking", "")

        avatar_url = assistant_avatar_url if role == "assistant" else user_avatar_url

        with st.chat_message(role, avatar=avatar_url):
            # Si es el asistente y tiene contenido de "pensamiento", se muestra en un recuadro especial
            if role == "assistant" and thinking and st.session_state.get("show_thinking", True):
                st.markdown(
                    f"""
                    <div style="background:#1E293B; color:#fff; padding:10px; margin-bottom:5px; 
                                border-left:4px solid #3B82F6; border-radius:4px;">
                        <strong>💭 Pensamiento:</strong><br/>
                        {thinking}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(content, unsafe_allow_html=True)

def handle_user_input(prompt):
    """
    Añade el mensaje del usuario al historial y genera la respuesta del asistente.
    """
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    generate_assistant_response()

def generate_assistant_response():
    """
    Llama a Ollama en modo streaming y separa en tiempo real lo que esté entre <think> y </think>.
    """
    with st.chat_message("assistant"):
        normal_placeholder = st.empty()   # Para el texto normal
        think_placeholder = st.empty()    # Para el recuadro de pensamiento
        
        try:
            temperature = getattr(st.session_state, "temperature", 0.7)
            stream = generate_chat_response(
                model=st.session_state.model,
                messages=st.session_state.messages,
                temperature=temperature,
                stream=True
            )
            
            # Procesa la respuesta en streaming, separando el texto normal de lo que está en <think>...</think>
            final_text, final_thinking = process_streamed_response(
                stream,
                normal_placeholder,
                think_placeholder
            )
            
            # Almacena la respuesta en el historial
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_text,
                "thinking": final_thinking
            })
            
        except Exception as e:
            error_message = format_error_message(e)
            normal_placeholder.error(error_message)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Ocurrió un error: {error_message}",
                "thinking": ""
            })

def process_streamed_response(stream, normal_placeholder, think_placeholder):
    """
    Procesa la respuesta en streaming, separando el contenido normal del bloque <think>... </think>.
    
    Retorna:
      final_text: Texto final sin el contenido de <think>.
      final_thinking: Contenido acumulado de los bloques <think>.
    """
    final_text = ""
    final_thinking = ""
    normal_text = ""
    thinking_text = ""
    inside_think = False

    for chunk in stream:
        if not chunk or 'message' not in chunk or 'content' not in chunk['message']:
            continue
        
        content_chunk = chunk['message']['content']
        i = 0
        while i < len(content_chunk):
            if not inside_think:
                # Buscar apertura de <think>
                idx_open = content_chunk.find('<think>', i)
                if idx_open == -1:
                    normal_text += content_chunk[i:]
                    i = len(content_chunk)
                else:
                    normal_text += content_chunk[i:idx_open]
                    inside_think = True
                    i = idx_open + len('<think>')
            else:
                # Dentro de <think>, buscar el cierre </think>
                idx_close = content_chunk.find('</think>', i)
                if idx_close == -1:
                    thinking_text += content_chunk[i:]
                    i = len(content_chunk)
                else:
                    thinking_text += content_chunk[i:idx_close]
                    inside_think = False
                    i = idx_close + len('</think>')
        
        # Actualiza la visualización en tiempo real
        normal_placeholder.markdown(normal_text + "▌", unsafe_allow_html=True)
        if inside_think:
            think_placeholder.markdown(
                f"""
                <div style="background:#1E293B; color:#fff; padding:10px; margin-bottom:5px;
                            border-left:4px solid #3B82F6; border-radius:4px;">
                    <strong>💭 Pensamiento (en vivo):</strong><br/>
                    {thinking_text}▌
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if thinking_text:
                think_placeholder.markdown(
                    f"""
                    <div style="background:#1E293B; color:#fff; padding:10px; margin-bottom:5px;
                                border-left:4px solid #3B82F6; border-radius:4px;">
                        <strong>💭 Pensamiento:</strong><br/>
                        {thinking_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        time.sleep(0.01)  # Pausa para simular el streaming
    
    # Finaliza la actualización
    normal_placeholder.markdown(normal_text, unsafe_allow_html=True)
    if inside_think:
        think_placeholder.markdown(
            f"""
            <div style="background:#1E293B; color:#fff; padding:10px; margin-bottom:5px;
                        border-left:4px solid #3B82F6; border-radius:4px;">
                <strong>💭 Pensamiento (sin cerrar):</strong><br/>
                {thinking_text}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if thinking_text:
            think_placeholder.markdown(
                f"""
                <div style="background:#1E293B; color:#fff; padding:10px; margin-bottom:5px;
                            border-left:4px solid #3B82F6; border-radius:4px;">
                    <strong>💭 Pensamiento:</strong><br/>
                    {thinking_text}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    final_text = normal_text
    final_thinking = thinking_text
    return final_text, final_thinking
