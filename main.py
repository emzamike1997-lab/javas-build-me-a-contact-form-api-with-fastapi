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

# GET /health endpoint
@app.get("/health")
def get_health():
    return {"status": "healthy"}

# GET / endpoint
@app.get("/")
def get_api_info():
    return {"api": "Contact Form API", "version": "1.0"}

# GET /contacts endpoint
@app.get("/contacts")
def get_contacts():
    return list(contacts.values())

# GET /contacts/{id} endpoint
@app.get("/contacts/{id}")
def get_contact(id: int):
    if id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contacts[id]

# POST /contacts endpoint
@app.post("/contacts")
def create_contact(contact: Contact):
    if contact.id in contacts:
        raise HTTPException(status_code=400, detail="Contact already exists")
    contacts[contact.id] = contact
    return contact

# PUT /contacts/{id} endpoint
@app.put("/contacts/{id}")
def update_contact(id: int, contact: Contact):
    if id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    if contact.id != id:
        raise HTTPException(status_code=400, detail="Contact ID mismatch")
    contacts[id] = contact
    return contact

# DELETE /contacts/{id} endpoint
@app.delete("/contacts/{id}")
def delete_contact(id: int):
    if id not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found")
    del contacts[id]
    return {"message": "Contact deleted"}