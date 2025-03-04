APP_TITLE = "🤖 DeepSeek Chatbot"
APP_DESCRIPTION = "Chat with your local DeepSeek model using Ollama"
PAGE_ICON = "🤖"

# Default model settings
DEFAULT_MODEL = "deepseek-r1:14b"
DEFAULT_TEMPERATURE = 0.7

# UI text
SIDEBAR_HEADER = "Settings"
SIDEBAR_FOOTER = "Made with Streamlit and Ollama"
CLEAR_BUTTON_TEXT = "Clear Conversation"
INPUT_PLACEHOLDER = "Ask something..."
NO_MODELS_ERROR = "No models found. Please install models with Ollama first."
MODEL_INSTALL_INSTRUCTION = "Try installing DeepSeek model with: ollama pull deepseek-r1:14b"
CONNECTION_ERROR = "Make sure the Ollama service is running."
WELCOME_MESSAGE = "👋 Start chatting with your local DeepSeek model!"

# Instructions text
INSTRUCTIONS = """
## Tips:
- Make sure Ollama is running on your machine
- This application is using the DeepSeek model: `deepseek-r1:14b`
- Adjust temperature for more creative or focused responses
- Your conversation history is maintained during the session
"""