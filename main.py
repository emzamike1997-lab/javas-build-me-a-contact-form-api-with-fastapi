import os
from fastapi import FastAPI, HTTPException
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
def root(): 
    return {"status": "ok", "service": "build me a contact form API with FastAPI"}

@app.get("/health")
def health(): 
    return {"status": "healthy"}

@app.post("/contact")
async def create_contact_form(contact_form: ContactForm):
    try:
        # Here you can add your logic to save the contact form data
        # For example, you can save it to a database or send an email
        return {"message": "Contact form submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contact")
async def get_contact_forms():
    try:
        # Here you can add your logic to retrieve the contact form data
        # For example, you can retrieve it from a database
        return [{"message": "No contact forms found"}]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 FastAPI app starting...")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)