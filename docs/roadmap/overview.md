# Chatbot Application Roadmap Overview

This document serves as the high-level roadmap and architectural vision for the Next-Gen Chatbot Application. The development process is broken down into **5 distinct phases**, moving from a foundational chat system to a highly advanced, extensible, multi-modal, tool-equipped, and customizable AI ecosystem.

## Phase Overview

### [Phase 1: Basic Chatbot System](./01_phase_1_basic_chatbot.md)
The foundation of the application. Establishes the core Hexagonal Architecture, user authentication, simple linear chat interactions, and strict database principles (like global soft-deletes and mandatory pagination). 

### [Phase 2: Multi-Model & Multi-Provider Integration](./02_phase_2_multi_model_provider.md)
Expansion from a single hardcoded LLM to a dynamic gateway supporting multiple providers (OpenAI, Anthropic, Gemini, Groq, etc.) and dozens of models. This phase introduces an extensive database schema to track model capabilities, context limits, pricing, and routing fallback logic.

### [Phase 3: RAG, Multimodal & Tool Support (MCP)](./03_phase_3_rag_and_tools.md)
The intelligence leap. Introduces Retrieval-Augmented Generation (RAG) for handling PDFs and images. Equips the bot with "hands and eyes" by integrating the Model Context Protocol (MCP) and a registry of 50+ specialized tools (Calculator, Web Search, Code Execution, Jira, etc.).

### [Phase 4: Non-Linear Chat Branching (Graph/Tree History)](./04_phase_4_chat_branching.md)
A massive upgrade to user experience. Moving away from linear arrays of messages, this phase transforms chat histories into Directed Acyclic Graphs (DAGs). Users can edit past messages or regenerate AI responses, splitting the conversation into multiple traversable alternate timelines (branches).

### [Phase 5: Custom Bots & System Personas](./05_phase_5_custom_bots.md)
The platform evolution. Allows users to create their own specialized "Bots" (similar to Custom GPTs). Users can configure a bot's name, system prompts, specific enabled tools, and attach personalized knowledge bases. The system will also provide highly tuned native "System Bots".

---
*Note: These documents do not contain code implementation, but rather the comprehensive blueprint, database models, and feature specifications required before execution begins.*
