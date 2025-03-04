# DeepSeek Chatbot

A Streamlit application for chatting with your local DeepSeek models through Ollama.

## Features

- 💬 Chat with your local DeepSeek models
- 🧠 Maintains conversation history
- 🔄 Real-time streaming responses
- 🌡️ Adjustable temperature settings
- 📱 Responsive design
- 🔄 Model selection

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- DeepSeek model(s) installed in Ollama

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/deepseek-chatbot.git
cd deepseek-chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Make sure you have Ollama installed and at least one DeepSeek model:
```bash
ollama pull deepseek-r1:14b
```

## Running the Application

Start the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501

## Project Structure

```
deepseek-chatbot/
├── app.py                # Main application entry point
├── requirements.txt      # Project dependencies
├── README.md            # Project documentation
├── config/
│   └── settings.py      # Application settings and constants
├── services/
│   └── ollama_service.py # Ollama API interactions
├── utils/
│   └── helpers.py       # Utility functions
└── ui/
    ├── sidebar.py       # Sidebar components
    ├── chat.py          # Chat interface components
    └── instructions.py  # Information and instructions UI
```

## Customization

You can customize the application by modifying the settings in `config/settings.py`:

- Change the default model
- Adjust temperature settings
- Modify UI text and appearance

## License

MIT