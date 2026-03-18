**=== test_contact_form_api.py ===**
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Contact Form API"}

def test_create_contact_form():
    """Test creating a new contact form"""
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_create_contact_form_missing_required_fields():
    """Test creating a new contact form with missing required fields"""
    data = {
        "email": "john@example.com",
        "message": "Hello, World!"
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "name"]
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][0]["type"] == "value_error.missing"

def test_create_contact_form_invalid_email():
    """Test creating a new contact form with invalid email"""
    data = {
        "name": "John Doe",
        "email": "invalid_email",
        "message": "Hello, World!"
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]
    assert response.json()["detail"][0]["msg"] == "email does not match format"
    assert response.json()["detail"][0]["type"] == "value_error.email"

def test_get_contact_form():
    """Test getting a contact form by ID"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    })
    contact_form_id = response.json()["id"]
    response = client.get(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"
    assert response.json()["message"] == "Hello, World!"

def test_get_contact_form_not_found():
    """Test getting a contact form that does not exist"""
    response = client.get("/contact/12345")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"

def test_update_contact_form():
    """Test updating a contact form"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    })
    contact_form_id = response.json()["id"]
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, Universe!"
    }
    response = client.put(f"/contact/{contact_form_id}", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_update_contact_form_not_found():
    """Test updating a contact form that does not exist"""
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, Universe!"
    }
    response = client.put("/contact/12345", json=data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"

def test_delete_contact_form():
    """Test deleting a contact form"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    })
    contact_form_id = response.json()["id"]
    response = client.delete(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Contact form deleted"

def test_delete_contact_form_not_found():
    """Test deleting a contact form that does not exist"""
    response = client.delete("/contact/12345")
    assert response.status_code == 404
    assert response.json()["detail"] == "Contact form not found"
```

**=== test_contact_form_api_unit.py ===**
```python
import pytest
from main import ContactForm

def test_contact_form_init():
    """Test initializing a contact form"""
    contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, World!")
    assert contact_form.name == "John Doe"
    assert contact_form.email == "john@example.com"
    assert contact_form.message == "Hello, World!"

def test_contact_form_str():
    """Test string representation of a contact form"""
    contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, World!")
    assert str(contact_form) == "ContactForm(name=John Doe, email=john@example.com, message=Hello, World!)"

def test_contact_form_repr():
    """Test representation of a contact form"""
    contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, World!")
    assert repr(contact_form) == "ContactForm(name=John Doe, email=john@example.com, message=Hello, World!)"

def test_contact_form_eq():
    """Test equality of two contact forms"""
    contact_form1 = ContactForm(name="John Doe", email="john@example.com", message="Hello, World!")
    contact_form2 = ContactForm(name="John Doe", email="john@example.com", message="Hello, World!")
    assert contact_form1 == contact_form2

def test_contact_form_ne():
    """Test inequality of two contact forms"""
    contact_form1 = ContactForm(name="John Doe", email="john@example.com", message="Hello, World!")
    contact_form2 = ContactForm(name="Jane Doe", email="jane@example.com", message="Hello, Universe!")
    assert contact_form1 != contact_form2
```

**=== test_contact_form_api_integration.py ===**
```python
import pytest
from main import app, ContactForm

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_create_contact_form(client):
    """Test creating a new contact form"""
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_get_contact_form(client):
    """Test getting a contact form by ID"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    })
    contact_form_id = response.json()["id"]
    response = client.get(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"
    assert response.json()["message"] == "Hello, World!"

def test_update_contact_form(client):
    """Test updating a contact form"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    })
    contact_form_id = response.json()["id"]
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, Universe!"
    }
    response = client.put(f"/contact/{contact_form_id}", json=data)
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_delete_contact_form(client):
    """Test deleting a contact form"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, World!"
    })
    contact_form_id = response.json()["id"]
    response = client.delete(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Contact form deleted"
```
Note that these tests are just examples and you may need to modify them to fit your specific use case. Additionally, you will need to implement the `ContactForm` model and the API endpoints in the `main.py` file.