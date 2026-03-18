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

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Welcome to the contact form API"}

@app.get("/health")
def read_health():
    return {"status": "healthy"}

@app.get("/contacts/")
def read_contacts():
    return list(contacts.values())

@app.get("/contacts/{contact_id}")
def read_contact(contact_id: int):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts[contact_id]

@app.post("/contacts/")
def create_contact(contact: Contact):
    if contact.id in contacts:
        raise HTTPException(status_code=400, detail="Contact already exists")
    contacts[contact.id] = contact
    return contact

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact: Contact):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.id != contact_id:
        raise HTTPException(status_code=400, detail="Contact ID mismatch")
    contacts[contact_id] = contact
    return contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    if contact_id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    del contacts[contact_id]
    return {"message": "Contact deleted"}