
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ContractIn, ContractOut, QARequest, QAResponse
from app.agents.coordinator import process_contract, get_contract_store, answer_question

app = FastAPI(
    title="ContractOps: AI-powered Contract Lifecycle Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/contracts", response_model=ContractOut)
def create_contract(payload: ContractIn):
    try:
        return process_contract(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contracts", response_model=list[ContractOut])
def list_contracts():
    return list(get_contract_store().values())

@app.get("/contracts/{contract_id}", response_model=ContractOut)
def get_contract(contract_id: str):
    store = get_contract_store()
    if contract_id not in store:
        raise HTTPException(status_code=404, detail="Not found")
    return store[contract_id]

@app.post("/contracts/{contract_id}/qa", response_model=QAResponse)
def qa(contract_id: str, payload: QARequest):
    store = get_contract_store()
    if contract_id not in store:
        raise HTTPException(status_code=404, detail="Not found")
    ans = answer_question(payload.question, list(store.values()))
    return QAResponse(contract_id=contract_id, question=payload.question, answer=ans)
