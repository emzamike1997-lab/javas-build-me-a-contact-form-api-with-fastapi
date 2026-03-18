from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Enable CORS for all origins
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
contacts = {}

class Contact(BaseModel):
    id: int
    name: str
    email: str
    message: str

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str

# GET /health endpoint
@app.get("/health")
def get_health():
    return {"status": "healthy"}

# GET / endpoint
@app.get("/")
def get_api_info():
    return {"api": "Contact Form API", "version": "1.0"}

# GET /contacts endpoint
@app.get("/contacts", response_model=List[Contact])
def get_contacts():
    return list(contacts.values())

# GET /contacts/{id} endpoint
@app.get("/contacts/{id}", response_model=Contact)
def get_contact(id: int):
    if id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts[id]

# POST /contacts endpoint
@app.post("/contacts", response_model=Contact)
def create_contact(contact_request: ContactRequest):
    new_id = len(contacts) + 1
    contact = Contact(id=new_id, **contact_request.dict())
    contacts[new_id] = contact
    return contact

# PUT /contacts/{id} endpoint
@app.put("/contacts/{id}", response_model=Contact)
def update_contact(id: int, contact_request: ContactRequest):
    if id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = Contact(id=id, **contact_request.dict())
    contacts[id] = contact
    return contact

# DELETE /contacts/{id} endpoint
@app.delete("/contacts/{id}")
def delete_contact(id: int):
    if id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    del contacts[id]
    return {"message": "Contact deleted"}