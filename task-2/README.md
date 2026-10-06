# Problem Statement 2

**Maha Mugesh Ananth**

## 1. Self-Rating

I would rate myself as follows:

| Area | Rating |
|---|---|
| LLM | B |
| Deep Learning | B |
| AI | B |
| Machine Learning | B |

I selected B because I have worked with these areas through coursework and projects, but I may still need guidance when I face a completely new or advanced problem. I would rather give an honest rating than overestimate my current level.

## 2. High-Level Architecture of an LLM Chatbot

A basic LLM chatbot can be divided into a few main components. The user first interacts with a chat interface. The request is sent to a backend/API layer, which manages the request and conversation. Conversation history can be maintained so that the model has the required context. The backend prepares the prompt and sends the request to the LLM. The generated response is then returned to the user.

`User → Chat Interface → Backend/API → Conversation & Context → LLM → Response → User`

For a chatbot that needs information from external documents, I would add a retrieval layer. Documents can be divided into smaller chunks, converted into embeddings, and stored in a vector database. When a user asks a question, relevant chunks can be retrieved and supplied to the LLM as context.

`Documents → Chunks → Embeddings → Vector Database → Relevant Results → LLM`

## 3. Vector Databases

A vector database stores embeddings, which are numerical representations of information. Instead of only matching exact words, vector search can find information that is semantically similar to a query.

For example, a company could build a chatbot that answers questions about its internal documents. The documents could be split into smaller chunks and converted into embeddings. These embeddings and related metadata can be stored in a vector database.

When a user asks a question, the question can also be converted into an embedding. The system searches for similar document chunks and retrieves the most relevant results. Those results are then provided to the LLM as context. This is a common Retrieval-Augmented Generation (RAG) approach.

**Vector database selected: Qdrant**

- Supports similarity search for embeddings.
- Supports metadata, useful for filtering retrieved information.
- Works well with RAG-based applications.
- Provides a Python client/API convenient for application development.

I have worked with Qdrant and RAG in one of my projects, so I am familiar with the basic workflow.

In a production system, I would also consider indexing, security, data size, latency, monitoring, backup and deployment requirements when selecting and operating a vector database.
