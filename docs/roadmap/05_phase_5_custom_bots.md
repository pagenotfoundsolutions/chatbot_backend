# Phase 5: Custom Bots & System Personas

## 🎯 Goal
Transform the chat application into an AI Agent Platform. Allow users to define their own custom Assistants (Bots) that are pre-configured for specific tasks, similar to "Custom GPTs" or Anthropic's "Projects".

## 🛠 Features

1. **System Bots (Native Personas)**
   - Global bots provided by the platform.
   - Examples: "Code Assistant" (pre-configured with execute_bash and execute_python tools), "Copywriter", "Data Analyst".

2. **User Custom Bots (Bot Builder)**
   - Users can create and configure their own bots.
   - **Configuration Options**:
     - `Bot Name` and `Avatar`.
     - `System Prompt`: Detailed instructions dictating the bot's behavior and personality.
     - `Default Model`: Tie the bot to a specific model from the `llm_models` table (e.g., Claude 3.5 Sonnet for coding).
     - `Enabled Tools`: Select specific tools from the Phase 3 tool registry (e.g., allow this bot to read GitHub but not send Emails).
     - `Knowledge Base`: Attach specific RAG documents (PDFs, text files) that this bot will always search before answering.

3. **Bot Sharing & Discovery (Optional Expansion)**
   - Allow users to toggle custom bots from `private` to `public` or `workspace_shared`.

## 🗄️ Database Entities
- `Bot`: Stores the bot configuration (`id`, `owner_id`, `name`, `system_prompt`, `model_id`, `is_public`).
- `BotTools`: Many-to-many junction table mapping which tools a bot is allowed to use.
- `BotKnowledgeBase`: Maps which files/vector namespaces are attached to the bot.
- `Conversation` modification: Add `bot_id` to indicate which bot is handling the conversation thread.
