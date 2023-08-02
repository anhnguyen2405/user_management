// Function to handle the form submission for login
async function handleLogin(event) {
    event.preventDefault();

    const loginForm = event.target;
    const username = loginForm['login-username'].value;
    const password = loginForm['login-password'].value;

    try {
        const response = await axios.post('/api/login', {
            username: username,
            password: password
        });

        // Assuming the server returns a JWT token upon successful login
        const token = response.data.access_token;
        // Save the token in localStorage or use it as needed for authentication
        // For example, you can use it as a Bearer token in the Authorization header for subsequent API calls
        console.log('Login successful. JWT token:', token);
        // Add your code to redirect to a dashboard page or display a success message, etc.
    } catch (error) {
        console.error('Login failed:', error.response.data.message);
        // Add your code to display an error message to the user, e.g., in a <p> element with id="login-error"
    }
}

// Function to handle the form submission for registration
async function handleRegister(event) {
    event.preventDefault();

    const registerForm = event.target;
    const username = registerForm['register-username'].value;
    const password = registerForm['register-password'].value;

    try {
        const response = await axios.post('/api/register', {
            username: username,
            password: password
        });

        // Assuming the server returns a success message upon successful registration
        console.log('Registration successful:', response.data.message);
        // Add your code to display a success message to the user, e.g., in a <p> element with id="register-success"
    } catch (error) {
        console.error('Registration failed:', error.response.data.message);
        // Add your code to display an error message to the user, e.g., in a <p> element with id="register-error"
    }
}

// Add event listeners for the login and register forms
document.getElementById('login-form').addEventListener('submit', handleLogin);
document.getElementById('register-form').addEventListener('submit', handleRegister);
