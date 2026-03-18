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
        "message": "Hello, this is a test message"
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_create_contact_form_invalid_data():
    """Test creating a new contact form with invalid data"""
    data = {
        "name": "John Doe",
        "email": "invalid_email"
    }
    response = client.post("/contact", json=data)
    assert response.status_code == 422

def test_get_contact_form():
    """Test getting a contact form by ID"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message"
    })
    contact_form_id = response.json()["id"]
    response = client.get(f"/contact/{contact_form_id}")
    assert response.status_code == 200
    assert response.json()["id"] == contact_form_id
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"
    assert response.json()["message"] == "Hello, this is a test message"

def test_get_contact_form_not_found():
    """Test getting a contact form by ID that does not exist"""
    response = client.get("/contact/12345")
    assert response.status_code == 404

def test_update_contact_form():
    """Test updating a contact form"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message"
    })
    contact_form_id = response.json()["id"]
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, this is an updated test message"
    }
    response = client.put(f"/contact/{contact_form_id}", json=data)
    assert response.status_code == 200
    assert response.json()["id"] == contact_form_id
    assert response.json()["name"] == data["name"]
    assert response.json()["email"] == data["email"]
    assert response.json()["message"] == data["message"]

def test_update_contact_form_not_found():
    """Test updating a contact form that does not exist"""
    data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "message": "Hello, this is an updated test message"
    }
    response = client.put("/contact/12345", json=data)
    assert response.status_code == 404

def test_delete_contact_form():
    """Test deleting a contact form"""
    response = client.post("/contact", json={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "Hello, this is a test message"
    })
    contact_form_id = response.json()["id"]
    response = client.delete(f"/contact/{contact_form_id}")
    assert response.status_code == 200

def test_delete_contact_form_not_found():
    """Test deleting a contact form that does not exist"""
    response = client.delete("/contact/12345")
    assert response.status_code == 404
```

### === test_contact_form_api_unit.py ===

```python
import unittest
from main import ContactForm, ContactFormRepository

class TestContactFormRepository(unittest.TestCase):
    def test_create_contact_form(self):
        """Test creating a new contact form"""
        repository = ContactFormRepository()
        contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message")
        repository.create(contact_form)
        self.assertEqual(len(repository.get_all()), 1)

    def test_get_contact_form(self):
        """Test getting a contact form by ID"""
        repository = ContactFormRepository()
        contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message")
        repository.create(contact_form)
        self.assertEqual(repository.get(1).name, "John Doe")

    def test_update_contact_form(self):
        """Test updating a contact form"""
        repository = ContactFormRepository()
        contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message")
        repository.create(contact_form)
        contact_form.name = "Jane Doe"
        repository.update(contact_form)
        self.assertEqual(repository.get(1).name, "Jane Doe")

    def test_delete_contact_form(self):
        """Test deleting a contact form"""
        repository = ContactFormRepository()
        contact_form = ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message")
        repository.create(contact_form)
        repository.delete(contact_form)
        self.assertEqual(len(repository.get_all()), 0)

if __name__ == "__main__":
    unittest.main()
```

### === test_contact_form_api_integration.py ===

```python
import unittest
from main import app, ContactFormRepository

class TestContactFormAPI(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = TestClient(self.app)
        self.repository = ContactFormRepository()

    def tearDown(self):
        self.repository.delete_all()

    def test_create_contact_form(self):
        """Test creating a new contact form"""
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Hello, this is a test message"
        }
        response = self.client.post("/contact", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.repository.get(1).name, data["name"])

    def test_get_contact_form(self):
        """Test getting a contact form by ID"""
        self.repository.create(ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message"))
        response = self.client.get("/contact/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "John Doe")

    def test_update_contact_form(self):
        """Test updating a contact form"""
        self.repository.create(ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message"))
        data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "message": "Hello, this is an updated test message"
        }
        response = self.client.put("/contact/1", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.repository.get(1).name, data["name"])

    def test_delete_contact_form(self):
        """Test deleting a contact form"""
        self.repository.create(ContactForm(name="John Doe", email="john@example.com", message="Hello, this is a test message"))
        response = self.client.delete("/contact/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.repository.get_all()), 0)

if __name__ == "__main__":
    unittest.main()
```