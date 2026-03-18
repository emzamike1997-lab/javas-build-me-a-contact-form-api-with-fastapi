Here's an example of how you can write comprehensive tests for the contact form API using FastAPI and the `pytest` framework.

### === test_contact_form_api.py ===

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Contact Form API"}

def test_create_contact_form():
    """Test creating a new contact form"""
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_create_contact_form_missing_fields():
    """Test creating a new contact form with missing fields"""
    data = {
        "name": "John Doe",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"

def test_create_contact_form_invalid_email():
    """Test creating a new contact form with an invalid email"""
    data = {
        "name": "John Doe",
        "email": "invalid_email",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "email does not match format"
    assert response.json()["detail"][0]["type"] == "value_error.email"

def test_get_contact_form():
    """Test getting a contact form by ID"""
    # Create a new contact form
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    contact_form_id = response.json()["id"]
    # Get the contact form by ID
    response = client.get(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_get_contact_form_not_found():
    """Test getting a contact form by ID that does not exist"""
    response = client.get("/contact/1234567890")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"

def test_update_contact_form():
    """Test updating a contact form"""
    # Create a new contact form
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    contact_form_id = response.json()["id"]
    # Update the contact form
    updated_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, this is an updated test message."
    }
    response = client.put(f"/contact/{contact_form_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["email"] == updated_data["email"]
    assert response.json()["message"] == updated_data["message"]

def test_update_contact_form_not_found():
    """Test updating a contact form that does not exist"""
    # Update the contact form
    updated_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, this is an updated test message."
    }
    response = client.put("/contact/1234567890", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"

def test_delete_contact_form():
    """Test deleting a contact form"""
    # Create a new contact form
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    contact_form_id = response.json()["id"]
    # Delete the contact form
    response = client.delete(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Contact form deleted"

def test_delete_contact_form_not_found():
    """Test deleting a contact form that does not exist"""
    response = client.delete("/contact/1234567890")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"
```

### === test_main.py ===

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/contact")
async def create_contact_form(contact_form: ContactForm):
    # Save the contact form to the database
    # For this example, we'll just return the contact form
    return contact_form

@app.get("/contact/{contact_form_id}")
async def get_contact_form(contact_form_id: int):
    # Get the contact form from the database
    # For this example, we'll just return a dummy contact form
    return {"id": contact_form_id, "name": "John Doe", "email": "john@example.com", "message": "Hello, this is a test message."}

@app.put("/contact/{contact_form_id}")
async def update_contact_form(contact_form_id: int, contact_form: ContactForm):
    # Update the contact form in the database
    # For this example, we'll just return the updated contact form
    return contact_form

@app.delete("/contact/{contact_form_id}")
async def delete_contact_form(contact_form_id: int):
    # Delete the contact form from the database
    # For this example, we'll just return a success message
    return {"message": "Contact form deleted"}
```

### === test_main_test.py ===

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Contact Form API"}

def test_create_contact_form():
    """Test creating a new contact form"""
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_create_contact_form_missing_fields():
    """Test creating a new contact form with missing fields"""
    data = {
        "name": "John Doe",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"

def test_create_contact_form_invalid_email():
    """Test creating a new contact form with an invalid email"""
    data = {
        "name": "John Doe",
        "email": "invalid_email",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "email does not match format"
    assert response.json()["detail"][0]["type"] == "value_error.email"

def test_get_contact_form():
    """Test getting a contact form by ID"""
    # Create a new contact form
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    contact_form_id = response.json()["id"]
    # Get the contact form by ID
    response = client.get(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_get_contact_form_not_found():
    """Test getting a contact form by ID that does not exist"""
    response = client.get("/contact/1234567890")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"

def test_update_contact_form():
    """Test updating a contact form"""
    # Create a new contact form
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    contact_form_id = response.json()["id"]
    # Update the contact form
    updated_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, this is an updated test message."
    }
    response = client.put(f"/contact/{contact_form_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]
    assert response.json()["email"] == updated_data["email"]
    assert response.json()["message"] == updated_data["message"]

def test_update_contact_form_not_found():
    """Test updating a contact form that does not exist"""
    # Update the contact form
    updated_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, this is an updated test message."
    }
    response = client.put("/contact/1234567890", json=updated_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"

def test_delete_contact_form():
    """Test deleting a contact form"""
    # Create a new contact form
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message."
    }
    response = client.post("/contact", json=data)
    contact_form_id = response.json()["id"]
    # Delete the contact form
    response = client.delete(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Contact form deleted"

def test_delete_contact_form_not_found():
    """Test deleting a contact form that does not exist"""
    response = client.delete("/contact/1234567890")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"
```

Note: The above code is just an example and may need to be modified to fit your specific use case. Additionally, this code assumes that you have a database set up to store the contact forms. In a real-world application, you would replace the dummy data with actual data from your database.