### API Design Document
 
An API (Application Programming Interface) design document is the blueprint document needed for the 
development and integration of an API. I give the structural overview of the API purpose, the endpoints,
architecture, authentication and authorization methods, different ways which errors will be handled and
the format which the request and response of the API will take during usage. The document helps track the
consistency and the ability to maintain the API and making it easy for developer(s) to be able to use the API.
Following the best practices for API design, the documentation provides a seamless integration of the API
with client applications. 

#### **Key Components of an API Design Document**  
A well written API design document would generally include the following sections:
- Resource Overview
- Endpoint Specification
- HTTP Methods
- Request/Response Structure
- Status Codes
- Pagination and Caching
- Authentication and Authorization
- Personal Data Handling
- Error Handling

#### 1. Resources:
- **Courses**: Information about each course.
- **Enrollments**: Data about which students are enrolled in which courses.

#### 2. Endpoints:
- **Courses**:
  - `GET /api/courses/`: List all courses.
  - `POST /api/courses/`: Create a new course.
  - `GET /api/courses/{course_id}/`: Retrieve a specific course by ID.
  - `PUT /api/courses/{course_id}/`: Update a course by ID changing the course details.
  - `PATCH /api/courses/{course_id}/`: Update a course by ID changing specific aspect of the course details.
  - `DELETE /api/courses/{course_id}/`: Delete a course by ID.
- **Enrollments**:
  - `GET /api/enrollments/`: List all enrollments.
  - `POST /api/enrollments/`: Enroll a student in a course by admin or instructor.
  - `GET /api/enrollments/{enrollment_id}/`: Retrieve a specific enrollment by ID.
  - `PUT /api/enrollments/{enrollment_id}/`: Update an enrollment by ID.
  - `PATCH /api/enrollments/{enrollment_id}/`: Update specific fields of an enrollment by ID.
  - `DELETE /api/enrollments/{enrollment_id}/`: Delete an enrollment by ID.
  - `GET /api/enrollments/?student_id={id}/`: List all enrollments for a specific student.
  - `GET /api/enrollments/?course_id={id}/`: List all enrollments for a specific course.
  - `POST /api/my-enrollments/`: Enroll a student in a course by students.
  - `GET /api/my-enrollments/`: List all enrollments for a specific student.
  - `PUT /api/my-enrollments/{id}/`: Edit a specific enrollment by a student throughID.

 

#### 3. HTTP Methods:
- `GET`: Retrieve information.
- `POST`: Create new resources.
- `PUT`: Update existing resources.
- `PATCH`: Update specific fields of existing resources.
- `DELETE`: Remove resources.

#### 5. Status Codes:
- **Success**:
  - `200 OK`: Request successful (e.g., course list or enrollment list or enrollment details by ID).
  - `201 Created`: Resource created (e.g., enrollment created or course created).
  - `204 No Content`: Deletion successful (e.g., enrollment deleted or course deleted).
 
- **Errors**:
1. **Generic Error Messages**:
    - Error messages are generic and do not expose internal details (e.g., "Invalid credentials" instead of "Incorrect password").

2. **Error Codes**:
   - Standard HTTP error codes are used to indicate the nature of the error:
     - `400 Bad Request`: Invalid input data.
     - `401 Unauthorized`: Authentication failed.
     - `403 Forbidden`: Insufficient permissions.
     - `404 Not Found`: Resource not found.
     - `500 Internal Server Error`: Server-side error.

3. **Custom Exceptions**:
   - Custom exceptions (e.g., `APIException`) are raised for specific scenarios (e.g., duplicate courses or enrollments).

#### 6. Pagination:
- Implement PageNumberPagination using query parameters:
  - `/api/courses/?page=?`
  - `/api/enrollments/?page=?`

#### 7. Caching:
Using the Redis due to its fast in-memory storage and scalability through Django’s cache framework (django.core.cache).
- **Cache Key**: Use the course ID or enrollment ID as the cache key.
- **Cache Expiry**: Expiry time for all the cached data would be at least 30 minutes.
- **Cache Invalidation**: Invalidate the cache when a course or enrollment is created, updated, or deleted.

## **API Documentation**
The API documentation is automatically generated using **DRF-yasg** and is accessible at `/swagger/` and `/redoc/`.

### **Documentation Features**
1. **Endpoints**:
   - All API endpoints are documented, including their HTTP methods and paths.

2. **Request/Response Formats**:
   - The expected request payload and response formats are clearly documented for each endpoint.

3. **Authentication Requirements**:
   - The authentication method (JWT or Basic Authentication) required for each endpoint is specified.

4. **Error Codes**:
   - Common error codes and their meanings are documented.

5. **Examples**:
   - Example requests and responses are provided for each endpoint.

### **Example Documentation**
- **Courses**:
```http
POST /api/courses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Advanced Renewable Energy",
    "description": "Explore advanced topics in renewable energy.",
    "instructor": "Jane Smith",
    "start_date": "2023-11-01",
    "end_date": "2024-01-31"
}
```

**Response:**
```json
{
    "id": 2,
    "title": "Advanced Renewable Energy",
    "description": "Explore advanced topics in renewable energy.",
    "instructor": "Jane Smith",
    "instructor_image": null,
    "start_date": "2023-11-01",
    "end_date": "2024-01-31"
}
```

- **Enrollments**:
  - **Request (POST)**:
    ```json
    {
      "student_id": "",
      "student_name": "",
      "course_title": ""
    }
    ```
  - **Response (GET)**:
    ```json
    {
      "id": "int",
    "student_id": "",
    "student_name": "",
    "student_email": "",
    "student_image": "",
    "start_date": "",
    "end_date": "",
    "course": "",
    "enrollment_date": ""
    }
    ```

#### 8. Authentication and Authorization:
## **Authentication Methods**
The Green Academy API supports two authentication methods to ensure secure access to its endpoints:

1. **JWT (JSON Web Token) Authentication**:
   - Used for general API access by all users (students, instructors, and admins).
   - Users obtain a JWT by authenticating with their username and password at the `/api/token/` endpoint.
   - The JWT is included in the `Authorization` header for subsequent requests:
     ```
     Authorization: Bearer <access_token>
     ```
   - Tokens have a limited lifespan, and a refresh token can be used to obtain a new access token at the `/api/token/refresh/` endpoint.

2. **Basic Authentication**:
   - Used for specific student functionality (e.g., To view available courses, this means even students without enrollments can view courses offering).
   - Students authenticate using their username and password, which are encoded and sent in the `Authorization` header:
     ```
     Authorization: Basic <base64_encoded_credentials>
     
     ```

---

## **Authorization (Granular Role-Based Access Control)**
The API implements role-based access control (RBAC) to restrict access to specific endpoints based on user roles. The roles and their permissions are as follows:

### **Roles**
1. **Admin**:
   - Full access to all endpoints (create, read, update, delete).
2. **Instructor**:
   - Can create, update, and delete their own courses.
   - Can view and manage enrollments for their courses.
3. **Student**:
   - Can view courses and their own enrollments.
   - Cannot modify any data.

### **Permissions Mapping**
| Endpoint                 | Method     | Admin | Instructor | Student |
|--------------------------|------------|-------|------------|---------|
| `/api/courses/`          | GET        | ✅    | ✅         | ✅      |
| `/api/courses/`          | POST       | ✅    | ✅         | ❌      |
| `/api/courses/{id}/`     | GET        | ✅    | ✅         | ✅      |
| `/api/courses/{id}/`     | PUT/PATCH  | ✅    | ✅         | ❌      |
| `/api/courses/{id}/`     | DELETE     | ✅    | ✅         | ❌      |
| `/api/enrollments/`      | GET        | ✅    | ✅         | ❌      |
| `/api/enrollments/`      | POST       | ✅    | ✅         | ❌      |
| `/api/enrollments/{id}/` | GET        | ✅    | ✅         | ❌      |
| `/api/enrollments/{id}/` | PUT/PATCH  | ✅    | ✅         | ❌      |
| `/api/enrollments/{id}/` | DELETE     | ✅    | ✅         | ❌      |
| `/api/my-enrollments/`   | GET        | ❌    | ❌         | ✅      |

---

### **Sensitive Data Handling**

1. **Environment Variables**:
   - Sensitive data such as `SECRET_KEY`, `JWT_SECRET`, and database credentials are stored in environment variables using a `.env` file.
   - The `.env` file is excluded from version control to prevent accidental exposure.

2. **Password Security**:
   - User passwords are securely hashed using Django's `make_password` function before being stored in the database.
   - Plaintext passwords are never stored or logged.

3. **JWT Secret Key**:
   - The JWT secret key is stored securely in an environment variable and is not hardcoded in the codebase.

---

## **Input Validation**

1. **DRF Serializers**:
   - Input validation is performed using Django REST Framework (DRF) serializers.
   - Examples:
     - `CourseSerializer`: Validates course title length, ensures unique titles, and validates date ranges.
     - `EnrollmentSerializer`: Validates student email format and prevents duplicate enrollments.

2. **Custom Validation Functions**:
   - Custom validation logic is implemented in serializers to enforce business rules (e.g., ensuring end dates are after start dates).

---

