<<<<<<< HEAD
# document-reasoner
Its a python based document reasoner using python and qdrant making a local LLM RAG
=======
# Smart Document Reasoner

AI-powered desktop application for document analysis and Q&A using LLMs

## Features
- Multi-format document support (PDF, DOCX, XML, YML)
- Semantic search using Qdrant vector DB
- OpenAI GPT-4 and local LLM support (Mistral-7B)
- Conversation history tracking
- Cross-platform support

## 🛠️ Local Installation

### Prerequisites
- Python 3.10+
- Qdrant Server (Docker)
- OpenAI API key (optional)

### Steps
1. Clone repository:
   ```bash
   git clone https://github.com/yourusername/document-reasoner.git
   cd document-reasoner
   ```
2. Requirements: OpenAI API key, Windows(WSL) IP -> docker-compose.yml(Display settings) for my WSL.,  Used VcXsrv Windows X Server for connecting WSL docker to windows host screen.

3. Download Local LLM (in my case: Mistrlal)
```
   mkdir -p models && cd models
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
```
or you use GPT-4

4. docker UP
 ```
docker compose up --build
```
