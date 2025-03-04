import ollama
from typing import List, Dict, Any, Generator, Optional

def get_available_models() -> List[str]:
    """
    Get list of available models from Ollama.
    
    Returns:
        List of model names
    """
    try:
        models = ollama.list()
        # Print the raw response for debugging
        print(f"Ollama response: {models}")
        
        # Handle different response formats
        if isinstance(models, dict) and "models" in models:
            return [model["name"] for model in models["models"]]
        elif isinstance(models, list):
            return [model["name"] for model in models]
        elif isinstance(models, dict):
            # Fallback to adding your specific model
            return ["deepseek-r1:14b"]
        else:
            print(f"Unexpected response format: {type(models)}")
            return ["deepseek-r1:14b"]  # Fallback to your installed model
    except Exception as e:
        print(f"Error fetching models: {e}")
        # Even if there's an error, add your known model
        return ["deepseek-r1:14b"]

def convert_to_ollama_messages(streamlit_messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Convert Streamlit message format to Ollama format.
    
    Args:
        streamlit_messages: List of messages in Streamlit format
        
    Returns:
        List of messages in Ollama format
    """
    ollama_messages = []
    for msg in streamlit_messages:
        # Convert from Streamlit's format to Ollama's format
        role = "assistant" if msg["role"] == "assistant" else "user"
        ollama_messages.append({"role": role, "content": msg["content"]})
    return ollama_messages

def generate_chat_response(
    model: str, 
    messages: List[Dict[str, str]], 
    temperature: float = 0.7,
    stream: bool = True
) -> Generator[Dict[str, Any], None, None]:
    """
    Generate a chat response using Ollama.
    
    Args:
        model: Name of the model to use
        messages: List of conversation messages
        temperature: Response temperature (higher = more creative)
        stream: Whether to stream the response
        
    Returns:
        Generator yielding response chunks
    """
    ollama_messages = convert_to_ollama_messages(messages)
    
    # Check the Ollama version to determine the correct API parameters
    try:
        # Some versions of the Ollama library don't accept temperature in the chat method
        return ollama.chat(
            model=model,
            messages=ollama_messages,
            stream=stream,
            # Pass options dict instead of direct temperature parameter
            options={"temperature": temperature}
        )
    except TypeError as e:
        print(f"Falling back to basic chat without temperature: {e}")
        # Fallback to basic parameters if the above doesn't work
        return ollama.chat(
            model=model,
            messages=ollama_messages,
            stream=stream
        )

def generate_completion(
    model: str, 
    prompt: str, 
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False
) -> Dict[str, Any]:
    """
    Generate a text completion using Ollama.
    
    Args:
        model: Name of the model to use
        prompt: Text prompt
        temperature: Response temperature (higher = more creative)
        max_tokens: Maximum number of tokens to generate
        stream: Whether to stream the response
        
    Returns:
        Completion response
    """
    try:
        # First try with the options parameter
        options = {"temperature": temperature}
        if max_tokens:
            options["num_predict"] = max_tokens
            
        return ollama.generate(
            model=model,
            prompt=prompt,
            options=options,
            stream=stream
        )
    except TypeError:
        # Fallback to direct parameters if needed
        params = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        # Some versions might still accept these direct parameters
        try:
            params["temperature"] = temperature
            if max_tokens:
                params["max_tokens"] = max_tokens
                
            return ollama.generate(**params)
        except TypeError:
            # Last resort - just use the minimal required parameters
            return ollama.generate(
                model=model,
                prompt=prompt,
                stream=stream
            )