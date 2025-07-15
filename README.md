# ⚡ FastAPI Boilerplate

A minimal, production-ready FastAPI boilerplate with:

- RESTful API structure
- Health check endpoint
- Reservation service with full CRUD functionality
- MongoDB integration via Motor (async)
- Centralized logging configuration
- Dependency injection for MongoDB access

---

## 🚀 Getting Started

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### ⚙️ Environment Variables (`.env`)

```env
MONGODB_URL=mongodb://mongo_user:mongo_password@localhost:27017/appdb?authSource=appdb
```

---

### 🖥️ Run the Application

Run the app using:

```bash
python main.py
```

> ✅ The API will be available at:  
> 🌐 http://localhost:8000  
> 📘 Swagger UI: http://localhost:8000/docs  
> 📕 ReDoc: http://localhost:8000/redoc

---

## 📡 API Endpoints

### 🔍 Health Check

**GET** `/api/v1/health`

Returns the health status of the application.

#### ✅ Response
```json
{
  "status": "OK"
}
```

---

### 🏨 Reservation API

All endpoints are prefixed with `/api/v1/reservation`

#### ➕ Create a Reservation

**POST** `/make`  
Creates a new reservation.

#### 📄 Get Reservation by UUID

**GET** `/{reservation_uuid}`  
Fetches reservation details by UUID.

#### 📅 Check Room Availability

**GET** `/room_availability/{reservation_uuid}`  
Returns availability details based on the reservation UUID.

#### ❌ Delete Reservation

**DELETE** `/{reservation_uuid}`  
Deletes a reservation by UUID.

---

## 🧩 Project Structure

```text
.
├── api
│   ├── config
│   │   ├── logger.py
│   │   └── settings.py
│   ├── controller
│   │   └── reservation_controller.py
│   ├── database
│   │   └── mongo_repository.py
│   ├── models
│   │   └── reservation_model.py
│   └── v1
│       └── routes
│           ├── health_check_route.py
│           └── reservation_route.py
├── main.py
├── requirements.txt
├── README.md
└── .env
```

---
## 🧪 Running Tests

Ensure pytest is installed:
```bash
pip install pytest
```

Run tests from the project root directory:
```bash
PYTHONPATH=. pytest -v
```
PYTHONPATH=. ensures your modules are discoverable during testing.

Tests are automatically discovered in files matching test_*.py or *_test.py.

---

## 📬 Contributions

Pull requests, issues, and feature requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 🛡 License

This project is open-source and available under the MIT License.