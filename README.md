# Vue FastAPI Auth App

This is a full-stack web application with a Vue.js frontend and a FastAPI backend that provides user authentication with 2-Factor Authentication (2FA).

## Design: Vibrant Glass

The application features a modern and vibrant design called "Vibrant Glass". It uses a colorful gradient background and glassmorphism effects to create a visually engaging user experience.

## Features

*   User registration and login
*   Secure password hashing using Argon2
*   JSON Web Token (JWT) authentication
*   2-Factor Authentication (2FA) with TOTP (Time-based One-Time Password)
*   QR code generation for easy 2FA setup
*   Protected routes
*   MySQL database

## Technology Stack

This project utilizes a modern and robust technology stack to deliver a secure and responsive web application:

*   **Frontend:**
    *   **Vue.js 3:** A progressive JavaScript framework for building user interfaces.
    *   **Vue Router:** The official router for Vue.js, enabling seamless navigation.
    *   **Axios:** A promise-based HTTP client for making API requests.
    *   **Vite:** A fast and opinionated build tool for modern web projects.
*   **Backend:**
    *   **FastAPI:** A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
    *   **Uvicorn:** An ASGI server for running FastAPI applications.
    *   **MySQL:** A popular open-source relational database management system.
    *   **Passlib:** A comprehensive password hashing library for Python.
    *   **python-jose:** A JOSE (JSON Object Signing and Encryption) implementation in Python, used for JWT.
    *   **pyotp:** A Python library for generating and verifying one-time passwords (TOTP/HOTP).
    *   **qrcode:** A Python library for generating QR codes.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.7+
*   Node.js 14+
*   MySQL Server

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure the database:**
    Open `main.py` and replace the placeholder values in the `DB_CONFIG` dictionary with your actual MySQL database credentials.

4.  **Create the database table:**
    Execute the SQL commands in `db.sql` in your MySQL server to create the `users` table. This table is essential for storing user information.

5.  **Configure the JWT secret key:**
    In `main.py`, replace the value of the `SECRET_KEY` variable with a strong, randomly generated secret key. This key is crucial for signing and verifying JWT tokens.

6.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend server will be running at `http://localhost:8000`.

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the frontend server:**
    ```bash
    npm run dev
    ```
    The frontend server will be running at `http://localhost:5173`.

### 3. Access the application

Open your web browser and go to `http://localhost:5173` to access the application.

## Project Structure

```
.
├── backend
│   ├── main.py
│   ├── requirements.txt
│   └── db.sql
└── frontend
    ├── index.html
    ├── package.json
    ├── src
    │   ├── App.vue
    │   ├── components
    │   │   ├── Dashboard.vue
    │   │   ├── Enable2FA.vue
    │   │   ├── Login.vue
    │   │   └── Register.vue
    │   ├── main.js
    │   └── router.js
    └── vite.config.js
```

## API Design

The API is designed following RESTful principles, providing clear and consistent endpoints for user authentication and management. JWT (JSON Web Tokens) are used for secure, stateless authentication, ensuring that user sessions are managed efficiently and securely.

## AI Tools Used

This project was developed with the assistance of Gemini, an AI-powered coding assistant. Gemini helped with:

*   **Code Generation:** Generating boilerplate code and complex logic snippets.
*   **Debugging:** Identifying and suggesting fixes for errors.
*   **Refactoring:** Restructuring code for better readability and maintainability.
*   **Design Iteration:** Proposing and implementing UI design changes based on feedback.
*   **Documentation:** Generating and updating project documentation.

## API Endpoints

*   `POST /register`: Register a new user.
*   `POST /login`: Log in a user and get a JWT token.
*   `POST /2fa/enable`: Generate a QR code for enabling 2FA.
*   `POST /2fa/confirm`: Confirm the 2FA setup.
*   `POST /2fa/verify`: Verify the 2FA code during login.
*   `GET /me`: Get the current user's information.
*   `GET /dashboard`: A protected endpoint that returns a welcome message.