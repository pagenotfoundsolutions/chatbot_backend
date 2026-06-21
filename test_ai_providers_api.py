import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzMmZmZmIwZS04Y2ZjLTQ4ZmUtYWE5MC1hZjIxMGZiOGVhNmUiLCJleHAiOjE3ODI3NzY0MTIsInR5cGUiOiJhY2Nlc3MifQ.ub402wrier4fCb9vHjJTixghLQpT1exb_xV6fp9tvDQ"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def make_request(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    print(f"\n[{method}] {url}")
    
    req_data = None
    if data:
        req_data = json.dumps(data).encode("utf-8")
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            status = response.status
            parsed = json.loads(res_body)
            print(f"Status: {status}")
            return parsed
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code}")
        res_body = e.read().decode("utf-8")
        try:
            print(json.loads(res_body))
        except json.JSONDecodeError:
            print(res_body)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_api():
    print("=== TESTING ADMIN ENDPOINTS (CREATE) ===")
    
    # 1. Create OpenAI Provider
    openai_data = {
        "name": "openai",
        "display_name": "OpenAI",
        "description": "Provider of GPT models.",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": "sk-dummy-openai-key"
    }
    openai_res = make_request("POST", "/admin/ai-providers/", data=openai_data)
    if not openai_res or "data" not in openai_res:
        print("Failed to create provider.")
        return
    
    openai_id = openai_res["data"]["id"]
    print(f"Created OpenAI Provider with ID: {openai_id}")
    
    # 2. Create Anthropic Provider
    anthropic_data = {
        "name": "anthropic",
        "display_name": "Anthropic",
        "description": "Provider of Claude models.",
        "api_base_url": "https://api.anthropic.com/v1",
        "api_key": "sk-dummy-anthropic-key"
    }
    anthropic_res = make_request("POST", "/admin/ai-providers/", data=anthropic_data)
    anthropic_id = anthropic_res["data"]["id"]
    print(f"Created Anthropic Provider with ID: {anthropic_id}")

    # 3. Create Models for OpenAI
    gpt4o_data = {
        "provider_id": openai_id,
        "model_key": "gpt-4o",
        "display_name": "GPT-4o",
        "description": "OpenAI's fastest and most capable model.",
        "model_type": "text",
        "max_input_tokens": 128000,
        "max_output_tokens": 4096,
        "max_context_window": 128000,
        "supports_vision": True,
        "supports_tools": True,
        "supports_json": True
    }
    gpt4o_res = make_request("POST", "/admin/ai-providers/models", data=gpt4o_data)
    gpt4o_id = gpt4o_res["data"]["id"]
    print(f"Created GPT-4o Model with ID: {gpt4o_id}")

    # 4. Create Models for Anthropic
    sonnet_data = {
        "provider_id": anthropic_id,
        "model_key": "claude-3-5-sonnet",
        "display_name": "Claude 3.5 Sonnet",
        "description": "Anthropic's most intelligent model.",
        "model_type": "text",
        "max_input_tokens": 200000,
        "max_output_tokens": 8192,
        "max_context_window": 200000,
        "supports_vision": True,
        "supports_tools": True,
        "supports_json": True
    }
    sonnet_res = make_request("POST", "/admin/ai-providers/models", data=sonnet_data)
    sonnet_id = sonnet_res["data"]["id"]
    print(f"Created Claude 3.5 Sonnet Model with ID: {sonnet_id}")
    
    print("\n=== TESTING PUBLIC ENDPOINTS ===")
    
    # 5. List Providers
    list_providers_res = make_request("GET", "/ai/providers")
    
    # 6. List Models
    list_models_res = make_request("GET", "/ai/models")
    
    # 7. Get Specific Provider
    get_prov_res = make_request("GET", f"/ai/providers/{openai_id}")
    
    # 8. Get Specific Model
    get_mod_res = make_request("GET", f"/ai/models/{gpt4o_id}")
    
    print("\n=== TESTING ADMIN ENDPOINTS (UPDATE & DELETE) ===")
    
    # 9. Update Model
    update_mod_data = {
        "description": "UPDATED: OpenAI's fastest and most capable model (Updated via API)."
    }
    update_mod_res = make_request("PUT", f"/admin/ai-providers/models/{gpt4o_id}", data=update_mod_data)
    
    # 10. Update Provider
    update_prov_data = {
        "display_name": "OpenAI (Updated)"
    }
    update_prov_res = make_request("PUT", f"/admin/ai-providers/{openai_id}", data=update_prov_data)
    
    # 11. Delete the Anthropic provider and model to verify deletion
    print("Deleting Claude 3.5 Sonnet Model...")
    make_request("DELETE", f"/admin/ai-providers/models/{sonnet_id}")
    
    print("Deleting Anthropic Provider...")
    make_request("DELETE", f"/admin/ai-providers/{anthropic_id}")
    
    print("\n=== FINAL VERIFICATION ===")
    make_request("GET", "/ai/providers")
    make_request("GET", "/ai/models")
    print("Tests completed successfully.")

if __name__ == "__main__":
    test_api()
