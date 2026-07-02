import requests
import uuid
import json

base_url = "http://localhost:18100/api"

# We don't have auth, so we can't easily test without a token.
# Wait, can we bypass auth or get a token?
