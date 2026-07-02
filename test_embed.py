import os
import sys
# Load .env.dev
from dotenv import load_dotenv
load_dotenv('env/.env.dev')

from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
try:
    client = NVIDIAEmbeddings(
        model="nvidia/nv-embedcode-7b-v1", 
        api_key=os.environ.get("NVIDIA_API_KEY", ""), 
        truncate="NONE"
    )
    emb = client.embed_query("test")
    print("Dimension:", len(emb))
except Exception as e:
    print("Error:", e)
