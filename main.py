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

# GET /
@app.get("/")
def read_root():
    return {"API": "Contact Form API", "version": "1.0"}

# GET /health
@app.get("/health")
def read_health():
    return {"status": "healthy"}

# GET /contacts
@app.get("/contacts", response_model=List[Contact])
def read_contacts():
    return list(contacts.values())

# GET /contacts/{contact_id}
@app.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(contact_id: int):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts[contact_id]

# POST /contacts
@app.post("/contacts", response_model=Contact)
def create_contact(contact_request: ContactRequest):
    new_id = len(contacts) + 1
    contact = Contact(id=new_id, **contact_request.dict())
    contacts[new_id] = contact
    return contact

# PUT /contacts/{contact_id}
@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact_request: ContactRequest):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact = Contact(id=contact_id, **contact_request.dict())
    contacts[contact_id] = contact
    return contact

# DELETE /contacts/{contact_id}
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    del contacts[contact_id]
    return {"message": "Contact deleted"}