import time
from typing import Optional

def slow_text_display(text: str, delay: float = 0.01) -> str:
    """
    Helper function to simulate slower text display for streaming.
    
    Args:
        text: Text to display
        delay: Delay between characters in seconds
        
    Returns:
        The original text (after delay)
    """
    time.sleep(delay)
    return text

def get_model_index(model_list: list, current_model: str) -> int:
    """
    Get the index of the current model in the model list.
    
    Args:
        model_list: List of available models
        current_model: Current model name
        
    Returns:
        Index of the current model or 0 if not found
    """
    return model_list.index(current_model) if current_model in model_list else 0

def extract_chunk_content(chunk: dict) -> Optional[str]:
    """
    Extract content from a response chunk.
    
    Args:
        chunk: Response chunk from Ollama
        
    Returns:
        Extracted content or None if not found
    """
    if chunk and 'message' in chunk and 'content' in chunk['message']:
        return chunk['message']['content']
    return None

def format_error_message(error: Exception) -> str:
    """
    Format an error message for display.
    
    Args:
        error: Exception object
        
    Returns:
        Formatted error message
    """
    return f"Error: {type(error).__name__} - {str(error)}"