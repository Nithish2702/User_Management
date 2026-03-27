# User Management REST API

FastAPI backend with SQLite for user management - BuyerForeSight Backend Assignment

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application entry point
│   ├── app/
│   │   ├── models.py        # Pydantic models for validation
│   │   ├── database.py      # SQLite connection and initialization
│   │   └── routes/
│   │       └── users.py     # All user endpoints
│   ├── test_api.py          # Test script to verify endpoints
│   ├── requirements.txt     # Dependencies
│   └── README.md           # Backend-specific instructions
└── README.md               # This file
```

## Features

- RESTful API with CRUD operations
- SQLite database for persistent storage
- Search functionality across name and email
- Sorting by any field (name, email, age, created_at)
- Email validation
- Proper error handling
- Interactive API documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **Language**: Python 3.x
- **Validation**: Pydantic

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python -m uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### 3. Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### 1. Create User
- **Method**: `POST`
- **URL**: `http://localhost:8000/users`
- **Body**:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

### 2. List All Users
- **Method**: `GET`
- **URL**: `http://localhost:8000/users`

### 3. Search Users
- **Method**: `GET`
- **URL**: `http://localhost:8000/users?search=John`

### 4. Sort Users
- **Method**: `GET`
- **URL**: `http://localhost:8000/users?sort=name&order=asc`
- **Sort Options**: `id`, `name`, `email`, `age`, `created_at`
- **Order Options**: `asc`, `desc`

### 5. Get User by ID
- **Method**: `GET`
- **URL**: `http://localhost:8000/users/1`

### 6. Update User
- **Method**: `PUT`
- **URL**: `http://localhost:8000/users/1`
- **Body** (all fields optional):
```json
{
  "name": "John Updated",
  "email": "john.new@example.com",
  "age": 35
}
```

### 7. Delete User
- **Method**: `DELETE`
- **URL**: `http://localhost:8000/users/1`

## Testing

### Option 1: Using the Test Script

```bash
cd backend
python test_api.py
```

### Option 2: Using Postman

Import the following requests into Postman:

1. **Create User**: POST `http://localhost:8000/users`
2. **List Users**: GET `http://localhost:8000/users`
3. **Search**: GET `http://localhost:8000/users?search=John`
4. **Sort**: GET `http://localhost:8000/users?sort=name&order=asc`
5. **Get by ID**: GET `http://localhost:8000/users/1`
6. **Update**: PUT `http://localhost:8000/users/1`
7. **Delete**: DELETE `http://localhost:8000/users/1`

### Option 3: Using curl

```bash
# Create a user
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":30}'

# List all users
curl "http://localhost:8000/users"

# Search users
curl "http://localhost:8000/users?search=John"

# Get user by ID
curl "http://localhost:8000/users/1"

# Update user
curl -X PUT "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"age":31}'

# Delete user
curl -X DELETE "http://localhost:8000/users/1"
```

## Database

The application uses SQLite with the following schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

The database file `users.db` is created automatically in the backend directory when the server starts.

## Error Handling

- **400**: Bad Request (invalid data, duplicate email)
- **404**: User Not Found
- **422**: Validation Error (invalid email format, etc.)

## Development

To run in development mode with auto-reload:

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Notes

- Email validation is done using regex pattern
- Age must be between 0 and 150
- Email must be unique
- All timestamps are in UTC
- The API supports partial updates (PATCH-like behavior with PUT)

## Author

Backend Engineer Assessment for BuyerForeSight
