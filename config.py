import os

from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_MODEL_NAME = "openai/gpt-oss-20b"
RAGAS_API_KEY= os.environ["RAGAS_API_KEY"]
NUMBER_OF_TEXT_CHUNKS = 3
NUMBER_OF_TABLE_CHUNKS = 4