# Vue FastAPI Auth App

This is a full-stack web application with a Vue.js frontend and a FastAPI backend that provides user authentication with 2-Factor Authentication (2FA).

## Features

*   User registration and login
*   Secure password hashing using Argon2
*   JSON Web Token (JWT) authentication
*   2-Factor Authentication (2FA) with TOTP (Time-based One-Time Password)
*   QR code generation for easy 2FA setup
*   Protected routes
*   MySQL database
*   Modern and responsive UI

## Technologies Used

*   **Frontend:**
    *   Vue.js 3 (with Composition API)
    *   Vue Router
    *   Axios
    *   Vite
*   **Backend:**
    *   FastAPI
    *   Uvicorn
    *   MySQL
    *   Passlib (for password hashing)
    *   python-jose (for JWT)
    *   pyotp (for 2FA)
    *   qrcode (for QR code generation)

## Getting Started

### Prerequisites

*   Python 3.7+
*   Node.js 14+
*   MySQL Server

### 1. Backend Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure the database:**
    Open `main.py` and replace the placeholder values in the `DB_CONFIG` dictionary with your actual MySQL database credentials.

3.  **Create the database table:**
    Execute the SQL commands in `db.sql` in your MySQL server to create the `users` table.

4.  **Configure the JWT secret key:**
    In `main.py`, replace the value of the `SECRET_KEY` variable with a strong, randomly generated secret key.

5.  **Run the backend server:**
    ```bash
    uvicorn main:app --reload
    ```
    The backend server will be running at `http://localhost:8000`.

### 2. Frontend Setup

1.  **Install dependencies:**
    ```bash
    npm install
    ```

2.  **Run the frontend server:**
    ```bash
    npm run dev
    ```
    The frontend server will be running at `http://localhost:5173`.

### 3. Access the application

Open your web browser and go to `http://localhost:5173` to access the application.

## Project Structure

```
.
├── main.py
├── package.json
├── README.md
├── requirements.txt
├── src
│   ├── App.vue
│   ├── components
│   │   ├── Dashboard.vue
│   │   ├── Enable2FA.vue
│   │   ├── Login.vue
│   │   └── Register.vue
│   ├── main.js
│   ├── router.js
├── style.css
├── db.sql
└── vite.config.js
```

## API Endpoints

*   `POST /register`: Register a new user.
*   `POST /login`: Log in a user and get a JWT token.
*   `POST /2fa/enable`: Generate a QR code for enabling 2FA.
*   `POST /2fa/confirm`: Confirm the 2FA setup.
*   `POST /2fa/verify`: Verify the 2FA code during login.
*   `GET /me`: Get the current user's information.
*   `GET /dashboard`: A protected endpoint that returns a welcome message.