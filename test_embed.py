import os
import sys
# Load the unified local environment.
from dotenv import load_dotenv
load_dotenv('env/.env')

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
