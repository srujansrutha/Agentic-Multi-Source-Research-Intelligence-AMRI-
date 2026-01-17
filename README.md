# AMRI: Agentic Multi-Source Research Intelligence

**Production-Grade Hybrid RAG Platform with Semantic Caching**

## 🌟 Overview

AMRI is an autonomous research platform designed to bridge the gap between Corporate Internal Data and Real-Time Web Intelligence. Unlike standard chatbots, AMRI utilizes a stateful LangGraph workflow to orchestrate deep-dive research, cross-referencing private PDF uploads with live web search results.

It solves the "Cost vs. Latency" dilemma of Generative AI by implementing a Redis-powered Semantic Cache, reducing API costs by ~90% for recurring queries.

---

## 🔥 Key Features

### 1. 🧠 Hybrid RAG Architecture
- **Internal Context**: Ingests private PDFs into a local Qdrant vector store
- **External Intelligence**: Uses Tavily API to fetch real-time data, bypassing LLM knowledge cutoffs
- **Result**: Reports that synthesize "What the web says" with "What our internal files say"

### 2. ⚡ Semantic Caching (Redis)
- Standard caching matches exact strings; AMRI uses Vector Similarity Caching
- **Example**: If User A asks "AI Trends 2025" and User B asks "Future of AI in 2025," the system recognizes the semantic match and serves the cached report instantly (0.05s latency) without burning LLM tokens

### 3. 🛡️ Privacy & Sovereignty
- **Dual-Inference Engine**: Configurable via `.env`
- **Cloud**: Uses OpenAI GPT-4o for maximum performance
- **Local**: Switches to Ollama (Llama 3) for 100% data privacy within the corporate firewall

### 4. 📝 Source-Grounded Reporting
- Every claim in the final report is hyperlinked to its source URL
- Dedicated "References" section for verification

---

## 📁 Project Structure

```
AMRI/
├── backend/                        # FastAPI Microservice
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # API Routes & App definition
│   │   ├── models.py               # Pydantic Data Models (Request/Response)
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Environment variables (API Keys, Redis URL)
│   │   │   └── security.py         # API Key validation / Guardrails
│   │   ├── agent/                  # THE BRAIN (LangGraph)
│   │   │   ├── __init__.py
│   │   │   ├── graph.py            # StateGraph Workflow definition
│   │   │   ├── nodes.py            # Functions: search_node, rag_node, cache_node
│   │   │   └── state.py            # TypedDict State definition
│   │   └── services/               # External Tools & Services
│   │       ├── __init__.py
│   │       ├── redis_cache.py      # Redis Client for Semantic Caching
│   │       ├── vector_db.py        # Qdrant setup & PDF Ingestion logic
│   │       └── llm_factory.py      # Switcher: OpenAI (Cloud) <-> Ollama (Local)
│   ├── Dockerfile                  # Backend container build instructions
│   └── requirements.txt            # Python dependencies
│
├── frontend/                       # React + Vite UI
│   ├── public/                     # Static assets
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   │   ├── SearchBar.tsx       # Search input component
│   │   │   ├── ReportView.tsx      # Markdown report renderer
│   │   │   └── FileUpload.tsx      # Drag-and-drop PDF upload zone
│   │   ├── services/
│   │   │   └── api.ts              # Axios HTTP client for FastAPI
│   │   ├── App.tsx                 # Main UI layout
│   │   └── main.tsx                # React entry point
│   ├── Dockerfile                  # Frontend container build instructions
│   ├── package.json                # npm dependencies
│   ├── tsconfig.json               # TypeScript configuration
│   └── vite.config.ts              # Vite build configuration
│
├── data/                           # Persistent storage (Docker volumes)
│   ├── qdrant_db/                  # Vector store data files
│   └── redis_data/                 # Cache data
│
├── docker-compose.yml              # Container orchestration
├── .env                            # Environment secrets (OPENAI_API_KEY, TAVILY_API_KEY)
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                          User                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────▼──────┐
                    │   React   │
                    │ Frontend  │
                    └────┬──────┘
                         │ HTTP/WebSocket
        ┌────────────────▼────────────────┐
        │     FastAPI Backend             │
        │  ┌──────────────────────────┐   │
        │  │  Redis Semantic Cache    │   │
        │  └──────────────────────────┘   │
        │  ┌──────────────────────────┐   │
        │  │  LangGraph Orchestrator  │   │
        │  └──────┬───────────┬───────┘   │
        └─────────┼───────────┼───────────┘
                  │           │
        ┌─────────▼──┐   ┌────▼──────────┐
        │ Tavily API │   │ Qdrant Vector │
        │ (Web Data) │   │ Database (RAG)│
        └────────────┘   └────┬──────────┘
                              │
                        ┌─────▼──────┐
                        │ LLM Engine  │
                        │ OpenAI/     │
                        │ Ollama      │
                        └─────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| Orchestration | LangGraph | Managing agent state and cyclic workflows |
| Backend | FastAPI | High-performance, async Python API |
| Frontend | React + Vite | Responsive user interface |
| Vector Database | Qdrant | Vector storage for RAG |
| Caching | Redis | Semantic caching and session persistence |
| AI Models | GPT-4o / Llama 3 | Reasoning and generation |
| DevOps | Docker Compose | Container orchestration |

---

## 🚀 Quick Start Guide

### Prerequisites
- Docker & Docker Compose installed
- API Keys for:
  - **OpenAI** (for GPT-4o)
  - **Tavily** (for web search)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/AMRI-Research-Agent.git
cd AMRI-Research-Agent

# Set up Environment Variables
cp .env.example .env
# Edit .env and add:
# OPENAI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here
```

### Run with Docker (Recommended)

This command spins up the entire stack:
- **Backend**: Port 8000
- **Frontend**: Port 3000
- **Redis**: Port 6379

```bash
docker-compose up --build -d
```

### Access the Application

- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

---

## 👨‍💻 Developer Guide

### Key Files to Modify

| File | Purpose |
|------|---------|
| `backend/app/agent/graph.py` | LangGraph workflow orchestration |
| `backend/app/agent/nodes.py` | Individual agent node implementations |
| `backend/app/services/redis_cache.py` | Semantic caching logic |
| `backend/app/services/vector_db.py` | Qdrant vector database integration |
| `frontend/src/components/ReportView.tsx` | Report rendering component |
| `frontend/src/services/api.ts` | API client for backend communication |

### Running Locally (Without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

---

## 🔧 Environment Configuration

Create a `.env` file in the project root:

```env
# LLM Configuration
OPENAI_API_KEY=your_openai_key
LLM_PROVIDER=openai  # or 'ollama' for local inference

# Search API
TAVILY_API_KEY=your_tavily_key

# Database
REDIS_URL=redis://localhost:6379
QDRANT_URL=http://localhost:6333

# API Security
API_SECRET_KEY=your_secret_key
```

---

## 📚 Architecture Deep Dive

### LangGraph Workflow

The agent orchestrates research through a stateful graph:

1. **Query Input** → User submits research query
2. **Cache Check** → Vector similarity search in Redis
3. **Cache Hit** → Return cached report (instant)
4. **Cache Miss** → Execute workflow:
   - **Web Search Node** → Fetch real-time data via Tavily
   - **RAG Node** → Retrieve relevant PDF context from Qdrant
   - **Synthesis Node** → Generate comprehensive report via LLM
5. **Output** → Return report with source citations
6. **Cache Store** → Store embeddings for future queries

### Semantic Caching

- Converts queries to embeddings
- Performs vector similarity search in Redis
- Reduces LLM API calls by ~90% for similar queries
- Dramatically improves latency for repeated research patterns

---

## 📬 Author

**J Srujan Vishwakrama**
- Junior AI Engineer @ Trendgully
- Specializing in Agentic Workflows, MLOps, and Scalable Systems

---

## 📄 License

[Add your license here]

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Known Issues & Roadmap

### Current Implementation
- Vector database: Qdrant (replacing ChromaDB in earlier versions)
- Supports OpenAI GPT-4o and Ollama Llama 3 inference
- Redis-based semantic caching with vector similarity

### Roadmap
- [ ] Add support for more vector databases (Pinecone, Weaviate)
- [ ] Implement rate limiting and usage analytics
- [ ] Add support for multi-modal document processing
- [ ] Integrate with additional search providers
- [ ] Deploy to cloud platforms (AWS, GCP, Azure)

---

