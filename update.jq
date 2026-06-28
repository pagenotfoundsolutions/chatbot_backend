.items |= map(.models |= map(
  if .model_key == "o1" then .capabilities = ["stream", "reasoning", "vision", "tools", "json"]
  elif .model_key == "o3-mini" then .capabilities = ["stream", "reasoning", "tools", "json"]
  elif .model_key == "gpt-4o" or .model_key == "gpt-4o-mini" then .capabilities = ["stream", "vision", "tools", "json"]
  elif .model_key == "gpt-3.5-turbo" then .capabilities = ["stream", "tools", "json"]
  elif .model_key | startswith("claude") then .capabilities = ["stream", "vision", "tools", "json"]
  elif .model_key == "gemini-3-deep-think" then .capabilities = ["stream", "vision", "tools", "json", "reasoning"]
  elif .model_key | startswith("gemini") then .capabilities = ["stream", "vision", "tools", "json"]
  elif .model_key == "deepseek-r1" or .model_key == "deepseek-ai/DeepSeek-R1" then .capabilities = ["stream", "reasoning"]
  elif .model_key == "llama3.1" or .model_key == "meta/llama-3.1-70b-instruct" then .capabilities = ["stream", "tools", "json"]
  elif .model_key == "HuggingFaceH4/zephyr-7b-beta" then .capabilities = ["stream", "json"]
  elif .model_key == "nvidia/nemotron-3-ultra-550b-a55b" then .capabilities = ["stream", "tools", "json", "reasoning"]
  elif .model_key == "minimaxai/minimax-m3" then .capabilities = ["stream", "vision", "json", "reasoning"]
  else .
  end
))
