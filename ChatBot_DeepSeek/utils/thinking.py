import re
from typing import Tuple, Optional

def extract_thinking(text: str) -> Tuple[Optional[str], str]:
    """
    Extract thinking section from text using <think> tags.
    
    Args:
        text: Text that may contain thinking tags
        
    Returns:
        Tuple of (thinking_content, clean_text)
    """
    # If text is None or empty, return None, empty string
    if not text:
        return None, ""
    
    # Pattern to match <think> tags and their content
    pattern = r'<think>(.*?)</think>'
    
    # Find all thinking sections
    thinking_matches = re.findall(pattern, text, re.DOTALL)
    
    if not thinking_matches:
        return None, text.strip()
    
    # Combine all thinking sections if multiple exist
    thinking_content = "\n".join(thinking_matches).strip()
    
    # Only return thinking content if it's not empty and has substantial content
    if not thinking_content or len(thinking_content.strip()) < 10:
        return None, text.strip()
    
    # Remove thinking sections from the text
    clean_text = re.sub(pattern, '', text, flags=re.DOTALL)
    
    # Remove extra whitespace that might be left
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
    clean_text = clean_text.strip()
    
    return thinking_content, clean_text

def format_message_with_thinking(message: str) -> str:
    """
    Format a message to properly display thinking sections.
    
    Args:
        message: Raw message that may contain thinking tags
        
    Returns:
        Formatted message with thinking sections styled differently
    """
    thinking, clean_text = extract_thinking(message)
    
    if thinking:
        # Return the formatted message with thinking section
        # The actual formatting will be done in the UI
        return {
            "thinking": thinking,
            "content": clean_text
        }
    else:
        # Return just the original content if no thinking section
        return {
            "thinking": None,
            "content": message
        }