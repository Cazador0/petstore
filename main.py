# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from rbd.database import ReferenceBaseDB
from rbd.query import QueryManager
from petstore import Pet, create_sample_pet

app = FastAPI(title="Reference Base Database (RBD)", version="0.1.0")

# In-memory (or file-based) RBD instance
db = ReferenceBaseDB("data/rbd_store.json")

# Query manager for unified data access
query_manager = QueryManager("data/rbd_store.json")

class AddRequest(BaseModel):
    data: str
    text_hint: str = None
    prev: str = None

class QueryRequest(BaseModel):
    text: str
    threshold: float = 0.6
    limit: int = 5

@app.get("/")
def home():
    return {
        "message": "Welcome to the Reference Base Database (RBD)",
        "endpoints": {
            "add": "POST /add",
            "query": "POST /query",
            "chain": "GET /chain/{ref_hash}"
        }
    }

@app.post("/add")
def add_data(request: AddRequest):
    try:
        ref_hash = query_manager.add_record(request.data, text_hint=request.text_hint, prev=request.prev)
        return {"ref": ref_hash, "message": "Data added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query")
def query_similar(request: QueryRequest):
    try:
        results = query_manager.query_similar(request.text, threshold=request.threshold)
        # Apply limit if specified
        if request.limit > 0:
            results = results[:request.limit]
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chain/{ref_hash}")
def get_chain(ref_hash: str):
    try:
        chain = query_manager.get_chain(ref_hash)
        if not chain:
            raise HTTPException(status_code=404, detail="Reference not found")
        return {"chain": chain}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/pets")
def add_pet(pet_data: dict):
    # Validate with Pydantic
    pet = Pet(**pet_data)
    # Add to RBD
    ref = db.add(pet.dict(), text_hint=f"{pet.breed} {pet.type}")
    return {"ref": ref}    

@app.get("/records")
def get_all_records():
    """Get all records from the database"""
    records = query_manager.get_all_records()
    
    return {
        "total": len(records),
        "records": records
    }

@app.get("/records/type/{record_type}")
def get_records_by_type(record_type: str):
    """Get all records of a specific type"""
    records = query_manager.get_records_by_type(record_type)
    
    return {
        "type": record_type,
        "total": len(records),
        "records": records
    }