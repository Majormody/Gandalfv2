import os

from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_MODEL_NAME = "openai/gpt-oss-20b"
RAGAS_API_KEY= os.environ["RAGAS_API_KEY"]
CHROMADB_API_KEY= os.environ["CHROMADB_API_KEY"]
CHROMADB_TENANT = "c1f513be-1804-4c0d-b1a6-a79cca748c84"
CHROMADB_DATABASE= "GANDALF_DATABASE"
NUMBER_OF_TEXT_CHUNKS = 3
NUMBER_OF_TABLE_CHUNKS = 4