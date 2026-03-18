import os
from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="build me a contact form API with FastAPI")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.get("/")
def root(): return {"status": "ok", "service": "build me a contact form API with FastAPI"}

@app.get("/health")
def health(): return {"status": "healthy"}

@app.post("/contact")
async def create_contact_form(contact_form: ContactForm):
    return {"status": "ok", "message": f"Contact form submitted successfully by {contact_form.name}"}

@app.post("/contact/form")
async def create_contact_form_with_form(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    return {"status": "ok", "message": f"Contact form submitted successfully by {name}"}

if __name__ == "__main__":
    print("🚀 FastAPI app starting...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)