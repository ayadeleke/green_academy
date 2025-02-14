@@ -1,59 +1,60 @@
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/USEfmVMq)
# Formative Assessment 2: API Security, Authorization, and Documentation
**Green Academy API - Phase 2: Enhancing Security and Usability**

**Scenario:**

Building upon the foundation laid in Phase 1, this phase focuses on securing the Green Academy API, implementing fine-grained authorization, and generating comprehensive API documentation. Protecting sensitive data, ensuring only authorized users can access specific functionalities, and providing clear documentation are paramount for a robust and usable API.  Additionally, best practices for secure storage of sensitive information will be reinforced.

---

**Instructions:**

In this group (group of 2) assignment, you will significantly enhance the API developed in Phase 1 by implementing robust security measures, including JWT and Basic Authentication, granular authorization, and automated API documentation. You will also reinforce secure storage of sensitive information.  *Testing will be covered in a subsequent phase.*

---

**Part 1: Enhanced API Design Document (20%)**

Update the API Design Document from Phase 1 to include the following enhancements:

*   **Authentication Methods:** Detail the implementation of both JWT (JSON Web Token) and Basic Authentication. Explain the use cases for each method (e.g., JWT for general API access, Basic Auth for specific admin functionalities).
*   **Authorization (Granular Control):** Define specific roles and permissions within the API. Specify which roles have access to which endpoints with a fine-grained approach (e.g., only admins can create courses, instructors can update their own courses, students can only view course content). Explain how you plan to implement role-based access control, including specific examples for different endpoints.  Provide a clear mapping of roles to permissions.
*   **Sensitive Data Handling:** Describe the methods used to securely store sensitive information like passwords, API keys, and JWT secrets. Discuss best practices such as hashing passwords (using bcrypt or scrypt), using environment variables for sensitive keys, and avoiding storing sensitive data directly in the codebase.
*   **Input Validation:** Explain your approach to validating user input to prevent vulnerabilities like SQL injection and cross-site scripting (XSS). Specify the validation techniques you will use (e.g., using DRF serializers, custom validation functions).
*   **Error Handling:** Describe your strategy for handling errors securely. Avoid revealing sensitive information in error messages.  Define specific error codes and messages for common scenarios.
*   **API Documentation:** Explain how you plan to generate API documentation automatically (e.g., using DRF-yasg, Swagger, or similar tools).  Describe the information that will be included in the documentation (e.g., endpoints, request/response formats, authentication requirements, error codes).

---

**Part 2: Implementation (80%)**

Implement the security, authorization, and documentation enhancements designed in Part 1 using Django REST Framework. Your implementation must meet the following requirements:

*   **JWT Authentication:** Implement JWT authentication for API access. Users should be able to obtain a JWT upon successful login and use it for subsequent requests.  Implement token refresh mechanisms.
*   **Basic Authentication:** Implement Basic Authentication for specific endpoints (e.g., admin functionalities).
*   **Granular Role-Based Access Control:** Implement role-based access control to restrict access to certain endpoints based on user roles.  Use Django's built-in permissions system or a custom role management system for fine-grained control.  Provide clear examples in your code demonstrating how different roles are granted access to specific endpoints.
*   **Password Security:** Ensure passwords are securely hashed before being stored in the database (use Django's `make_password` function).
*   **Sensitive Data Storage:** Store sensitive information (e.g., JWT secret key, database credentials) securely using environment variables or a similar secure configuration method. **Do not hardcode sensitive information in your codebase.**
*   **Input Validation:** Implement robust input validation to prevent common web vulnerabilities. Use DRF serializers with appropriate validation rules or custom validation functions.
*   **Error Handling:** Implement secure error handling. Return generic error messages to avoid revealing sensitive information. Use informative error codes.
*   **HTTPS:** (Highly recommended) Configure your development server to use HTTPS if possible. This is crucial for secure communication.
*   **Automated API Documentation:** Integrate a tool like DRF-yasg or Swagger to generate API documentation automatically.  Ensure that your documentation is complete and accurate.

---

**Deliverables:**

*   A link to your GitHub repository containing the updated project code.
*   A well-structured README.md file explaining how to set up, run, and use the API, including instructions for generating the API documentation.
*   An updated API_DESIGN.md document reflecting the enhanced security, authorization, and documentation considerations.

---

**Assessment Criteria:**

*   **Enhanced API Design Document (20%):** Clarity, completeness, and thoroughness of the design document, including detailed authorization strategies and API documentation plans.
*   **Code Functionality (60%):** Correct implementation of JWT and Basic Authentication, granular role-based access control, secure password handling, robust input validation, and secure error handling.
*   **API Documentation (20%):** Completeness and accuracy of the generated API documentation.  All endpoints, request/response formats, authentication requirements, and error codes should be properly documented.
*   **Code Quality (10%):** Well-organized, readable, and maintainable code following PEP 8 style guidelines with adequate comments.
*   **Security Best Practices (10%):** Adherence to security best practices for sensitive data handling, secure configuration of the API, and consideration of HTTPS.