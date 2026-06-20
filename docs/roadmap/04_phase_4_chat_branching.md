# Phase 4: Non-Linear Chat Branching (Graph Nodes)

## 🎯 Goal
Move away from traditional linear chat architectures (Array of Messages) to a Directed Acyclic Graph (DAG) or Tree structure. This is the architecture used by top-tier apps like ChatGPT, enabling users to edit past messages or regenerate responses without losing the original conversation context.

## 🛠 Features

1. **Tree-Based Message Storage**
   - A `Message` entity will no longer just belong to a `Conversation`. It will have a `parent_message_id`.
   - The "Conversation" represents the entire tree.
   - The "Current View" of a conversation is determined by walking back from the active leaf node to the root.

2. **Message Editing & Branching**
   - If a user scrolls up and edits Message #3, the system does **not** `UPDATE` Message #3.
   - Instead, it creates a new Message #3b, whose parent is Message #2. 
   - A new AI response (Message #4b) is generated as a child of #3b.
   - The UI provides `< 1 / 2 >` arrows on Message #3 so the user can swipe between the original branch and the new edited branch.

3. **Regeneration**
   - If a user clicks "Regenerate" on an AI response, the system creates a new sibling node to the AI response, keeping the user's prompt as the parent.

4. **Branch Deletion**
   - Users can prune specific branches they no longer want, cascading soft-deletes down that specific branch path.

## 🗄️ Database Changes
- Add `parent_message_id UUID REFERENCES messages(id)` to the `messages` table.
- Modify `list_messages` query to traverse the graph (e.g., using Recursive CTEs in PostgreSQL or by tracking the active `leaf_node_id` in the `conversations` table).
