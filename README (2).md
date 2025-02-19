# Green Academy API

## Description
The **Green Academy** is a non-profit organization that provides accessible online education about environmental sustainability and conservation. The Green Academy API enables users to manage courses, enrollments, and related functionality.

## Features
- **Course Management**: CRUD operations for courses.
- **Enrollment Management**: Enroll students in courses, view enrollments.
- **User Authentication**: Secure user authentication via JWT. (If in production - using Session Authentication at the moment)
- **Caching with Redis**: Improves performance by caching frequently accessed data.

## Technologies Used
- **Django**: Web framework.
- **Django REST Framework (DRF)**: API framework for building RESTful services.
- **Redis**: Caching backend for improved performance.
- **JWT Authentication**: For secure and stateless API access.
- **Mypy**: Static type-checking for Python code.

## Authentication
### 1. Generating a JWT Token
Before accessing protected endpoints, users must authenticate using their registered username and password.

**Request:**
```http
POST http://localhost:8000/api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "refresh": "your_refresh_token",
    "access": "your_access_token"
}
```

Use the **access token** for subsequent requests by including it in the `Authorization` header:
```http
Authorization: Bearer your_access_token
```

### 2. Refreshing a JWT Token
To get a new access token using a refresh token:
```http
POST http://localhost:8000/api/token/refresh/
Content-Type: application/json

{
    "refresh": "your_refresh_token"
}
```

### 3. Using Basic Authentication
If using basic authentication, student must first log in to view courses only and nothing more:
```http
POST http://localhost:8000/api/courses
Authorization: <base64_encoded_credentials>
```

## API Endpoints  

### Course Endpoints  
| Method     | Endpoint                 | Description          | Permissions |
|------------|--------------------------|----------------------|-------------|
| **GET**    | `/api/courses/`           | List all courses     | Any User    |
| **POST**   | `/api/courses/`           | Create a new course  | Admin/Instructors |
| **GET**    | `/api/courses/{id}/`      | Retrieve a course    | Any User    |
| **PUT**    | `/api/courses/{id}/`      | Update a course      | Admin/Instructors |
| **PATCH**  | `/api/courses/{id}/`   | Update a specific field of a course | Admin/Instructors |
| **DELETE** | `/api/courses/{id}/`   | Delete a course      | Admin/Instructors |


#### **Example: Get All Courses**
```http
GET http://127.0.0.1:8000/api/courses/
Authorization: Bearer your_jwt_access_token
Authorization: Basic <base64_encoded_credentials> # For students without a JWT token
```

## Role-Based Access Control
The API implements role-based access control (RBAC) to restrict access to specific endpoints based on user roles:

### Roles and Permissions
| Role        | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| **Admin**   | Full access to all endpoints (create, read, update, delete).                |
| **Instructor** | Can create, update, and delete their own courses. Can view enrollments. |
| **Student** | Can view courses and their own enrollments. Cannot modify any data.         |

For a detailed mapping of roles to endpoints, refer to the [API Design Document](API_DESIGN.md).
---

### Enrollment Endpoints  
| Method | Endpoint                 | Description              | Permissions       |
|--------|--------------------------|--------------------------|-------------------|
| **GET** | `/api/enrollments/`      | List all enrollments     | Admin/Instructors |
| **POST** | `/api/enrollments/`      | Enroll a student        | Admin/Instructors |
| **GET** | `/api/enrollments/{id}/` | Get enrollment details  | Admin/Instructors |
| **PUT** | `/api/enrollments/{id}/` | Update an enrollment    | Admin/Instructors |
| **PATCH**  | `/api/enrollments/{id}/` | Update a specific field of an enrollment | Admin/Instructors |
| **DELETE** | `/api/enrollments/{id}/` | Remove an enrollment    | Admin/Instructors |
| **GET** | `/api/enrollments/?student_id={id}` | Filter enrollments by student ID | Admin/Instructors |
| **GET** | `/api/enrollments/?course_id={id}` | Filter enrollments by course ID | Admin/Instructors |

---

### My Enrollments (For Students)  
| Method | Endpoint                               | Description                  | Permissions |
|--------|----------------------------------------|------------------------------|-------------|
| **GET** | `/api/my-enrollments/`                 | View my enrollments         | Student |
| **PUT** | `/api/my-enrollments/{id}/`            | Update an enrollment        | Student |
| **PATCH** | `/api/my-enrollments/{id}/`       | Update a specific field of an enrollment | Student |



#### **Example: View My Enrollments**
```http
GET http://127.0.0.1:8000/my-enrollments/
Authorization: Bearer your_jwt_access_token
```
## Sensitive Data Handling
- Sensitive information such as `SECRET_KEY`, `JWT_SECRET`, and database credentials are stored securely in environment variables (via `.env`).
- Passwords are securely hashed using Django's `make_password` function before being stored in the database.
- **Never hardcode sensitive information in the codebase.**

## Environment Variables
Create a `.env` file in the project root (check the `.env.example` file) with the following variables:
```ini
SECRET_KEY=your_secret_key
USERNAME=your_username
PASSWORD=your_password
```
## API Documentation
The API documentation is automatically generated using **DRF-yasg** and can be accessed at:
- **Swagger UI**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

The documentation includes:
- All API endpoints and their HTTP methods.
- Request and response formats.
- Authentication requirements.
- Error codes and examples.
---

## Installation
To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/green-academy-api.git

2. Navigate to the project folder:
   ```bash
   cd green-academy-api

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate


4. Install dependencies:
   ```bash
   pip install -r requirements.txt


5. Set up the database:
   ```bash
   python manage.py migrate


6. Run the development server:
   ```bash
   python manage.py runserver


7. Visit the API in your browser at http://127.0.0.1:8000/api/ after generating a JWT token as started above

## Running Tests

1. Install the testing dependencies (if not already installed):
   ```bash
   pip install django-redis

2. Run the tests:
   ```bash
   python manage.py test api/

## Troubleshooting

- If you get a **Redis connection error**, ensure Redis is installed and running on port 6379.
- If authentication fails, verify that the username, password, and `SECRET_KEY` match the stored values.
- Ensure required packages (`Pillow`, `django-redis`, `mypy`, etc.) are installed.

**Notes:** For more information about the API check the [API Design Document](API_DESIGN.md).

## Contributors
Bavukile Vilane
Email: b.vilane@alustudent.com
GitHub: https://github.com/bvilane

Ayotunde Adeleke
Email: a.adeleke@alustudent.com
GitHub: https://github.com/ayadeleke