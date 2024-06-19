from dotenv import load_dotenv
import os

# load dotenv
load_dotenv()
# API keys
openai_api_key = os.getenv("OPENAI_API_KEY")