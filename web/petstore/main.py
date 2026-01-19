from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import os
import json
from rbd import ReferenceBaseDB

# Initialize app
app = FastAPI(title="Pet Store Manager")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Initialize the RBD database
DB_PATH = "data/petstore_rbd.json"
db = ReferenceBaseDB(DB_PATH)

# Models
class CustomerForm(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str = None

class PetForm(BaseModel):
    name: str
    type: str
    breed: str = None
    age_months: int = None
    gender: str = "unknown"
    price: float
    status: str = "available"

# Routes
@app.get("/")
async def home(request: Request):
    return RedirectResponse(url="/customers")

@app.get("/customers")
async def list_customers(request: Request):
    # Get all customer records
    all_records = db.get_all_records()
    customers = [r["data"] for r in all_records 
                if isinstance(r["data"], dict) and r["data"].get("first_name") and r["type"] == "j"]
    
    return templates.TemplateResponse("customers.html", {
        "request": request,
        "customers": customers
    })

@app.post("/customers/create")
async def create_customer(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(None)
):
    new_customer = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email
    }
    
    # Add to database
    db.add(new_customer, text_hint=f"Customer: {first_name} {last_name}")
    
    return RedirectResponse(url="/customers", status_code=303)

@app.get("/pets")
async def list_pets(request: Request):
    # Get all pet records
    all_records = db.get_all_records()
    pets = [r["data"] for r in all_records 
           if isinstance(r["data"], dict) and r["data"].get("type") in ["dog", "cat", "bird", "fish"]]
    
    return templates.TemplateResponse("pets.html", {
        "request": request,
        "pets": pets
    })

@app.post("/pets/create")
async def create_pet(
    request: Request,
    name: str = Form(...),
    animal_type: str = Form(...),
    breed: str = Form(None),
    age: int = Form(None),
    gender: str = Form("unknown"),
    price: float = Form(...),
    status: str = Form("available")
):
    new_pet = {
        "name": name,
        "type": animal_type,
        "breed": breed,
        "age_months": age,
        "gender": gender,
        "price": price,
        "status": status
    }
    
    # Add to database
    db.add(new_pet, text_hint=f"Pet: {name}")
    
    return RedirectResponse(url="/pets", status_code=303)

@app.get("/sales")
async def list_sales(request: Request):
    # Get all sale records
    all_records = db.get_all_records()
    sales = [r["data"] for r in all_records 
            if isinstance(r["data"], dict) and r["data"].get("customer_id")]
    
    return templates.TemplateResponse("sales.html", {
        "request": request,
        "sales": sales
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)