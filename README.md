# Project Concierge: Autonomous Support Assistant 🤖

Project Concierge is a modular, source-grounded Retrieval-Augmented Generation (RAG) customer support assistant engineered during a 3-day development challenge. It combines local vector storage, regex-powered dynamic tool-calling, and safety guardrails to handle policy queries, track customer orders, and gracefully escalate high-stakes or emotional interactions.

---

## 📂 Project Directory Structure

```text
concierge-assistant/
├── DECISION_MEMO.md              # Executive architectural decision memo for the founder
├── FAILURES.md                   # Adversarial edge-case log & mitigation strategies
├── README.md                     # Project documentation and setup guide
├── requirements.txt              # Python package dependencies
├── daily_checkins/
│   ├── day1_checkin.md           # Day 1 milestone summary (Knowledge Base & Baseline)
│   ├── day2_checkin.md           # Day 2 milestone summary (Source-Grounding & Tools)
│   └── day3_checkin.md           # Day 3 milestone summary (Guardrails & Production Hardening)
├── data/
│   ├── chroma_db/                # Persistent local ChromaDB vector store
│   ├── raw_docs/                 # Source policy text files (refund_policy.txt, shipping_policy.txt)
│   └── eval_set.json             # Curated retrieval evaluation benchmark set
├── Outputs/                      # Visual verification screenshots and evidence
├── src/                          # Core application logic modules
│   ├── __init__.py               # Package initialization
│   ├── audit.py                  # Document audit and structure validator
│   ├── generator.py              # Main multi-route synthesis engine (RAG, Tools, Guardrails)
│   ├── guardrails.py             # Human hand-off escalation classifier
│   ├── indexing.py               # ChromaDB embedding & chunking pipeline
│   ├── retriever.py              # Vector similarity search engine
│   └── tools.py                  # Regex extractor and mock order database service
└── tests/
    ├── eval_adversarial.py       # Robustness testing suite (Prompt injection, OOB queries)
    └── eval_retrieval.py         # Retrieval evaluation benchmark script (Hit Rate & MRR)

```
## 🛠️ Technology Stack

- Language: Python

- Vector Store: ChromaDB (Persistent local storage)

- Embeddings: sentence-transformers (all-MiniLM-L6-v2)

- Routing & Safety: RegEx pattern matching, custom intent classifiers, and guardrails

## 🚀 Installation & Quickstart

1. Clone or Open the Repository
- Ensure you are in your project root directory:
- cd concierge-assistant

2. Create and Activate Virtual Environment
- python -m venv venv

# On Windows:
- venv\Scripts\activate

3. Install Dependencies
- pip install -r requirements.txt

## 🧪 Running the Pipeline & Evaluations
### Step 1: Knowledge Base Audit & Vector Indexing
- Audit raw documents for format consistency and index them into ChromaDB:
- python src/audit.py
- python src/indexing.py

### Step 2: Run Retrieval Benchmarks
- Evaluate baseline vector retrieval performance:
- python -m tests.eval_retrieval
- (Baseline achieves 100% Hit Rate @ 3 and an MRR of 0.8750).

### Step 3: Test Core Assistant & Tool Integration
- Execute the main generator script to test RAG retrieval, order lookup tools, and escalation guardrails:
- python -m src.generator

### Step 4: Run Adversarial & Robustness Suite
- Test system resilience against prompt injections, out-of-bounds queries, and malformed order inputs:
- python -m tests.eval_adversarial

## 📊 Evaluation Metrics & Results Summary
1. Retrieval Precision: Hit Rate @ 3 = 100% | Mean Reciprocal Rank (MRR) = 0.8750.

2. Tool Routing: Deterministic RegEx parsing successfully routes ORD-XXXX queries to the mock order database with zero latency.

3. Safety & Guardrails: Successfully detects escalation triggers (frustration, legal threats, agent requests) and reroutes traffic to a human support queue.

## 👥 Author
AI Engineering Developer: Priyanka Mohan Hundalekar