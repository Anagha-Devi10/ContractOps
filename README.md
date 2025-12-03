# ContractOps – AI-Powered Contract Lifecycle Agent

ContractOps is an **AI-driven contract assistant** that helps legal, sales, and finance teams quickly understand and manage contracts.

It ingests raw contract text and automatically:

- Extracts **key fields** (parties, dates, payment terms, renewal terms)
- Identifies **obligations** with confidence scores
- Generates **summaries**
- Allows **natural-language Q&A** over any selected contract
- Creates **operational tasks** (e.g., renewal reminders, payment term flags)

Built as an **Enterprise Agent** project using a **multi-agent pipeline** with:

-  **Backend:** FastAPI (Python)
-  **Frontend:** React + Vite
-  **Multi-agent flow:** Extraction → Memory → QA → Task Generation

---

## Features

### Intelligent Contract Extraction
- Detects:
  - Parties (e.g., _Alpha Corp and Beta Ltd_)
  - Effective date & expiry date
  - Payment terms (e.g., _“within 30 days”_)
  - Renewal terms
- Parses **obligations** using rule-based patterns (e.g., sentences with _shall_, _must_).

### Memory & Retrieval
- Stores each processed contract into a **TF-IDF-based memory bank** for retrieval.
- Supports question answering with:
  - **Structured extraction first** (expiry, parties, payment, etc.)
  - Then **semantic memory fallback** if needed.

### Natural-Language QA
Ask questions like:
- _“When does this contract expire?”_
- _“Who are the parties?”_
- _“What are the payment terms?”_

The QA agent:
- Uses the **currently selected contract** by default.
- Falls back to memory search if it can’t answer structurally.

### Task Generation (Ops Automation)
For each contract, the Task Agent can generate operational tasks, e.g.:

- Renewal reminders (based on expiry)
- Payment terms flags
- Obligations follow-up tasks

These can later be plugged into tools like:
- Ticketing system (Jira / Linear)
- Email reminders
- Internal dashboards

### Modern UI
React-based dashboard featuring:

- **Left panel:**  
  - Upload form for new contracts  
  - List of processed contracts with confidence scores
- **Right panel:**  
  - Contract details (extracted fields, summary, obligations)  
  - QA panel to ask questions about the selected contract

Dark, clean, dashboard-style design using custom CSS (no UI libraries required).

---

## Architecture

**High-level flow:**

1. **Frontend (React)**
   - User pastes contract text and title
   - Sends to backend `/contracts` API
   - Displays extracted info and supports interactive QA

2. **Backend (FastAPI)**
   - **Extraction Agent**
     - Rule-based + pattern heuristics for fields and obligations
   - **Memory Agent**
     - Stores contract summaries in a TF-IDF vector store
     - Supports similarity search for QA fallback
   - **QA Agent**
     - Answers structured questions using extracted fields
     - Uses memory if needed
   - **Task Agent**
     - Generates derived tasks (renewal reminders, payment term flags, etc.)

---

## Project Structure

```bash
contractops-agent/
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI app entrypoint
│   │   ├── schemas.py         # Pydantic models (ContractIn, ContractOut, QARequest, etc.)
│   │   ├── agents/
│   │   │   ├── extractors.py  # Contract field + obligation extraction logic
│   │   │   ├── tasks.py       # Task generation from extracted contracts
│   │   ├── utils/
│   │   │   ├── memory.py      # Simple TF-IDF-based memory store
│   │   │   ├── storage.py     # In-memory storage for contracts
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Main layout shell
│   │   ├── main.jsx               # React entry
│   │   ├── styles.css             # Custom dashboard styling
│   │   └── components/
│   │       ├── ContractUpload.jsx # Upload form for contract text
│   │       ├── ContractDetails.jsx# Details view for selected contract
│   │       └── QaPanel.jsx        # Ask questions about selected contract
│   ├── package.json
│   └── vite.config.js
└── README.md
