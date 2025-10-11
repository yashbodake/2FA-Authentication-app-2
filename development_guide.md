# Development Guide

This guide provides a comprehensive overview of the project, including the technology stack, setup instructions, API design, and the use of AI tools in the development process.

## Technology Stack

*   **Frontend:**
    *   **Vue.js:** A progressive JavaScript framework for building user interfaces.
    *   **Vite:** A fast build tool for modern web projects.
    *   **Vue Router:** The official router for Vue.js.
*   **Backend:**
    *   **Python:** A versatile programming language.
    *   **Flask:** A lightweight web framework for Python.
    *   **Flask-SQLAlchemy:** An extension for Flask that adds support for SQLAlchemy, an Object Relational Mapper (ORM).
    *   **Flask-Login:** An extension for Flask that provides user session management.
    *   **Flask-Cors:** An extension for Flask that enables Cross-Origin Resource Sharing (CORS).
*   **Database:**
    *   **SQLite:** A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine.

## Database Setup and Running the Application

### Prerequisites

Before you begin, ensure you have the following installed:

*   Node.js and npm
*   Python 3 and pip

### Step-by-Step Instructions

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Backend Setup:**

    *   Create a virtual environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the virtual environment:
        *   On Windows:
            ```bash
            venv\Scripts\activate
            ```
        *   On macOS/Linux:
            ```bash
            source venv/bin/activate
            ```
    *   Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   Initialize the database:
        ```bash
        flask db init
        flask db migrate -m "Initial migration"
        flask db upgrade
        ```

3.  **Frontend Setup:**

    *   Install npm dependencies:
        ```bash
        npm install
        ```

4.  **Running the Application:**

    *   Start the backend server:
        ```bash
        python main.py
        ```
    *   Start the frontend development server:
        ```bash
        npm run dev
        ```

    The application will be accessible at `http://localhost:5173`.

## API Design

The backend API is designed to be a simple and RESTful interface for the frontend. It uses JSON for all requests and responses. The API endpoints are as follows:

*   `POST /api/register`: Creates a new user account.
*   `POST /api/login`: Authenticates a user and returns a session token.
*   `POST /api/logout`: Logs the user out.
*   `GET /api/dashboard`: Retrieves data for the user's dashboard.
*   `POST /api/enable-2fa`: Enables two-factor authentication for the user.

## Use of AI Tools

This project was developed with the assistance of a large language model (LLM). The LLM was used for the following tasks:

*   **Code Generation:** The LLM was used to generate boilerplate code for the frontend and backend, including the database schema and API endpoints.
*   **Debugging:** The LLM was used to help debug issues with the code, such as errors in the frontend and backend.
*   **Documentation:** The LLM was used to generate this guide and other documentation for the project.
