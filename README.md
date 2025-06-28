# Customer Support System for E-Commerce Platform

A production-grade, end-to-end Retrieval-Augmented Generation (RAG) chatbot engineered for modern e-commerce. By harnessing real customer reviews and cutting-edge generative AI, this system delivers accurate, empathetic support—24/7, at scale.

---

## 🔧 Core Workflow

1. **Review Extraction**  
   Pulls structured and unstructured product reviews from MongoDB.

2. **Vectorization & Ingestion**  
   Encodes review text into dense embeddings and indexes them in AstraDB for lightning-fast semantic search.

3. **Context-Aware Reasoning**  
   Retrieves the most relevant review vectors and feeds them to an LLM, grounding replies in actual user feedback.

4. **Real-Time Chat API**  
   Serves REST and WebSocket endpoints via FastAPI, running on Uvicorn for sub-200 ms response times under heavy load.

---

## ✅ Key Capabilities

- **Review-Grounded Conversation**  
  Delivers answers anchored in your customers’ own words—product fit, usage tips, troubleshooting, and more.  
- **Modular, Scalable Architecture**  
  Decoupled ingestion, indexing, and inference layers make customization and horizontal scaling trivial.  
- **Production-Ready Best Practices**  
  Dockerized services, health checks, structured logging, and centralized metrics (Prometheus/Grafana).  
- **Extensible AI Stack**  
  Swap LLM providers or vector stores with minimal code changes.

---

## 🚀 Deployment & CI/CD

- **GitHub Workflows**  
  Automated build, test, and push pipelines for every commit.  
- **AWS ECR**  
  Hosts Docker images in a secure, versioned registry.  
- **AWS App Runner**  
  Auto-scales containerized services—zero infra management, built-in HTTPS.  
- **Environment-Driven Configuration**  
  Pass secrets and endpoints via environment variables (`ASTRADB_ENDPOINT`, `ASTRADB_TOKEN`, `MONGODB_URI`, `GROQ_API_KEY`, `GOOGLE_API_KEY`, `HF_TOKEN`).

---

## 🏃 Running Locally

1. With full source code
    ```
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

2. Build and tag the Docker image:  
   ```
   docker build -t support-bot:latest .
   ```

   ```
   docker run -p 8000 support-bot:latest
   ```

