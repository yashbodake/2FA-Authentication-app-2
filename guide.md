## A Simple Guide to Editing Your Application


### Project Overview

This project is a web application that has two main parts:

1.  **Frontend:** This is the part of the application that you see in your web browser. It's responsible for the user interface (UI) and for sending and receiving data from the backend. The frontend is built with Vue.js.
2.  **Backend:** This is the part of the application that runs on the server. It's responsible for handling the business logic, interacting with the database, and providing data to the frontend. The backend is built with FastAPI.

### File Structure

Here's a simplified overview of the most important files and directories:

*   `main.py`: This is the main file for the backend. It contains the code for the API endpoints.
*   `src/`: This directory contains all the frontend code.
    *   `components/`: This directory contains the Vue components for each page of the application (e.g., `Login.vue`, `Register.vue`).
    *   `style.css`: This file contains all the styles for the application (e.g., colors, fonts, layout).

### How to Make Simple Edits

#### Changing Text

To change the text on a page, you need to edit the corresponding Vue component in the `src/components/` directory.

For example, to change the text on the login page, you would edit the `src/components/Login.vue` file.

1.  Open the file in a text editor.
2.  Look for the text you want to change. It will usually be inside HTML tags (e.g., `<h2>Login</h2>`, `<p>Don't have an account?</p>`).
3.  Change the text to whatever you want.
4.  Save the file.
5.  Restart the frontend server to see the changes.

#### Changing Colors and Fonts

To change the colors and fonts of the application, you need to edit the `src/style.css` file.

This file contains all the styles for the application. You can change the values of the CSS properties to change the look and feel of the application.

For example, to change the background color of the buttons, you would look for the `button` style and change the `background-color` property:

```css
button {
    background-color: #007bff; /* This is a blue color */
    color: #fff;
    /* ... */
}
```

You can find color codes for different colors online (e.g., by searching for "hex color picker").

**Important:** Be very careful when editing the CSS file, as a small change can have a big impact on the UI.

### How it Works

Here's a simplified explanation of how the different parts of the application work together:

**1. Frontend-Backend Communication**

Think of the frontend as a waiter in a restaurant and the backend as the kitchen. When you (the user) want to do something, like register or log in, you give your order to the waiter (the frontend). The waiter then takes your order to the kitchen (the backend). The kitchen prepares the order and gives it back to the waiter, who then brings it to you.

In our application, the "orders" are called API requests. The frontend sends an API request to the backend, and the backend sends back a response.

**2. User Registration**

When you fill out the registration form and click "Sign Up", here's what happens:

1.  The frontend (the waiter) takes your username and password and sends it to the backend (the kitchen).
2.  The backend receives the data and first checks if a user with the same username already exists in the database.
3.  If the username doesn't exist, the backend hashes your password. This is a security measure that scrambles your password so that no one, not even us, can see it.
4.  The backend then saves your username and the hashed password to the database.
5.  The backend then tells the frontend that the registration was successful.

**3. User Login**

When you log in with your username and password, here's what happens:

1.  The frontend sends your username and password to the backend.
2.  The backend finds your user in the database and compares the password you entered with the hashed password in the database.
3.  If the passwords match, the backend creates a special, temporary key called a JSON Web Token (JWT). This token is like a temporary access card that proves you are who you say you are.
4.  The backend sends this token to the frontend, and the frontend stores it in your browser.
5.  Now, whenever you try to access a protected page (like the dashboard), the frontend sends the token to the backend to prove that you are logged in.

**4. 2-Factor Authentication (2FA)**

2FA adds an extra layer of security to your account. Here's how it works:

1.  **Enabling 2FA:** When you enable 2FA, the backend generates a secret key that is unique to your account. This key is then displayed as a QR code and as a string of text.
2.  **Authenticator App:** You scan the QR code or manually enter the secret key into an authenticator app on your phone (like Google Authenticator or Authy).
3.  **Generating Codes:** The authenticator app uses the secret key to generate a new 6-digit code every 30 seconds.
4.  **Verification:** When you log in, after you enter your password, you'll be asked to enter the 6-digit code from your authenticator app. The backend checks if the code is correct, and if it is, it lets you in.
