# Phase 1: Basic Chatbot System

## 🎯 Goal
To establish a solid, production-ready foundation that allows a user to send a text message to the AI and receive a real-time streamed text response.

## 🛠 Features

1. **Robust Core Architecture**
   - **Hexagonal Architecture (Ports and Adapters)**: Strict separation of concerns (Domain, Application, Adapters).
   - **User Authentication**: Secure JWT-based login/signup flow.
   - **Profile Management**: User profile creation and updates.

2. **Linear Chat Flow**
   - Create new conversations with automatically generated titles.
   - Send User messages and receive Assistant messages.
   - Initial setup with a single, reliable fallback model (e.g., GPT-3.5 or GPT-4o-mini).

3. **Database & Persistence Optimizations**
   - **Global Soft Delete**: A foolproof SQLAlchemy event listener (`with_loader_criteria`) that ensures `deleted_at IS NULL` is injected into every query.
   - **Mandatory Pagination**: All list APIs (conversations, messages) enforce strict cursor/offset pagination to protect memory and bandwidth.
   - **Core Mixins**: Standardized `id` (UUID), `created_at`, `updated_at`, and `deleted_at` fields across all tables.

4. **Performance**
   - Optimized relationships (`noload` where appropriate) to avoid N+1 query problems.
   - Efficient appending of chat messages without hydrating massive historical lists.

## 📦 Data Entities Involved
- `AuthUser`
- `Profile`
- `Conversation`
- `Message` (Linear linked to Conversation)
