<h1>Overview</h1>

**Quiz App** is a full-stack web application that enables users to create, share, and play interactive quizzes. The backend is built using Django and the Django REST Framework (DRF), with a MySQL database for data persistence.

<h1>Features</h1>

**User Features & Activity Tracking:**
Supports user profiles and tracks quiz attempts, enabling users to view their past activity and performance history.

**Authentication & Authorization:**
Implemented using JWT-based authentication, enabling secure, stateless communication between the frontend and backend. Custom permission classes were developed to enforce ownership-based access control, ensuring that only authorized users can modify or delete their own quizzes.

**Data Modeling & Relationships:**
Used Firebase Storage to support user image uploads (e.g., quiz cover and question images). Images are stored in cloud storage, while their corresponding access URLs are persisted in the database, enabling efficient retrieval and fast access to media assets.

**Input Validation & Serialization:**
Used DRF serializers to validate incoming request data, enforce constraints, and transform database records into JSON responses. This ensures consistency and reliability across API interactions.

**Media Handling:**
Used Firebase to support user image uploading (e.g., quiz cover images and question images). The backend saves stores images uploaded by users in Firebase cloud storage (e.g., Firebase Storage) and the access links in the database, allowing for the quick access of uploaded images.

**API Design & CRUD Operations:**
Built RESTful endpoints for creating, retrieving, updating, and deleting quizzes and related resources. The API supports partial updates, enabling efficient frontend workflows.

**Error Handling:**
Implemented consistent API error handling with structured error responses to ensure predictable client-side behavior.
