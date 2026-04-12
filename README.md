# Introduction

**Quiz App** is a full-stack web application that enables users to create, share, and play interactive quizzes. The backend is built using Django and the Django REST Framework (DRF), with a MySQL database for data persistence.

## Features

**User Features & Activity Tracking:**
Supports user profiles and tracks quiz attempts, enabling users to view their past activity and performance history.

**Authentication & Authorization:**
Uses JWT-based authentication, enabling secure, stateless communication between the frontend and backend. Custom DRF permission classes were developed to enforce ownership-based access control, ensuring that only authorized users can modify or delete their own quizzes.

**Input Validation & Serialization:**
Used DRF serializers to validate incoming request data and transform database records into JSON responses. The validation of incoming data ensures that it is safe and usable.

**Image Uploading:**
Used Firebase to support user image uploading (e.g., quiz cover images and question images). The backend saves stores images uploaded by users in Firebase cloud storage (e.g., Firebase Storage) and the access links in the database, allowing for the quick access of uploaded images.

**API Design & CRUD Operations:**
Built RESTful endpoints for creating, retrieving, updating, and deleting quizzes and related resources. The API supports partial updates, enabling efficient frontend workflows.

**Error Handling:**
Implemented consistent API error handling with structured error responses to ensure predictable client-side behavior.
