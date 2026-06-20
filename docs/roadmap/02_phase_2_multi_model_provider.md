# Phase 2: Multi-Model & Multi-Provider Ecosystem

## 🎯 Goal
To abstract the LLM execution layer, allowing the system to seamlessly route requests across multiple AI providers (OpenAI, Anthropic, Google, Groq, etc.) and allow users/system to select from a rich directory of available models based on capability, cost, and speed.

## 🛠 Features

1. **Provider Management**
   - Store and securely manage API keys for various providers.
   - Standardize input/output schemas so the domain logic doesn't care if it's talking to Claude or GPT.

2. **Model Registry & Selection**
   - Users can select a specific model for a conversation.
   - Dynamic UI that reads from the database to show what models are available, their capabilities, and context limits.

3. **Fallback & Routing Logic**
   - If a provider goes down or rate-limits, automatically route the request to a fallback model of equivalent capability.

## 🗄️ Database Schema: `llm_models`

This table serves as the ultimate source of truth for the router and the UI.

```sql
CREATE TABLE llm_models (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES llm_providers(id) ON DELETE CASCADE,
    
    model_key VARCHAR UNIQUE NOT NULL, -- e.g., 'gpt-4o', 'claude-3-opus-20240229'
    display_name VARCHAR NOT NULL,     -- e.g., 'GPT-4o', 'Claude 3 Opus'
    description TEXT,

    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    is_default BOOLEAN DEFAULT FALSE,
    is_deprecated BOOLEAN DEFAULT FALSE,

    -- Model Type
    model_type VARCHAR NOT NULL, -- ENUM('chat', 'reasoning', 'embedding', 'image', 'audio', 'multimodal')

    -- Context Limits
    max_input_tokens INT,
    max_output_tokens INT,
    max_context_window INT,

    -- Generation Defaults
    default_temperature DECIMAL(3,2),
    default_top_p DECIMAL(3,2),
    default_frequency_penalty DECIMAL(3,2),
    default_presence_penalty DECIMAL(3,2),

    -- Capabilities (Booleans)
    supports_tools BOOLEAN DEFAULT FALSE,
    supports_parallel_tools BOOLEAN DEFAULT FALSE,
    supports_structured_output BOOLEAN DEFAULT FALSE,
    supports_json BOOLEAN DEFAULT FALSE,
    supports_stream BOOLEAN DEFAULT TRUE,
    supports_vision BOOLEAN DEFAULT FALSE,
    supports_image_generation BOOLEAN DEFAULT FALSE,
    supports_audio_input BOOLEAN DEFAULT FALSE,
    supports_audio_output BOOLEAN DEFAULT FALSE,
    supports_embeddings BOOLEAN DEFAULT FALSE,
    supports_reasoning BOOLEAN DEFAULT FALSE,
    supports_system_prompt BOOLEAN DEFAULT TRUE,
    supports_web_search BOOLEAN DEFAULT FALSE,
    supports_file_upload BOOLEAN DEFAULT FALSE,
    supports_pdf BOOLEAN DEFAULT FALSE,
    supports_function_call BOOLEAN DEFAULT FALSE,
    supports_seed BOOLEAN DEFAULT FALSE,
    supports_response_format BOOLEAN DEFAULT FALSE,
    supports_cache BOOLEAN DEFAULT FALSE,
    supports_citations BOOLEAN DEFAULT FALSE,
    supports_multimodal BOOLEAN DEFAULT FALSE,

    -- Performance
    typical_latency_ms INT,
    speed_tier VARCHAR, -- e.g., 'fast', 'balanced', 'complex'

    -- Pricing (per 1 Million tokens)
    input_price_per_million DECIMAL(10,4),
    output_price_per_million DECIMAL(10,4),
    cache_price_per_million DECIMAL(10,4),

    -- Routing
    priority INT DEFAULT 0,
    fallback_model_id UUID REFERENCES llm_models(id),

    -- API Mapping
    provider_model_name VARCHAR NOT NULL,
    api_version VARCHAR,
    endpoint VARCHAR,

    -- Metadata
    extra JSONB,

    -- Standard Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);
```
