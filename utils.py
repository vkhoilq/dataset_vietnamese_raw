import os
from config import ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY

def set_api_key_config():
    
    if (os.environ.get("ANTHROPIC_API_KEY") is None):
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY

    if (os.environ.get("OPENAI_API_KEY") is None):
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    if (os.environ.get("GEMINI_API_KEY") is None):
        os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

if __name__ == "__main__":
    set_api_key_config()
    #print(os.environ["OPENAI_API_KEY"])
    #print(os.environ["ANTHROPIC_API_KEY"])