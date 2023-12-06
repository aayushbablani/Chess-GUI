// Import necessary modules and components
import React, { useState } from 'react';
import './Login.css'; // Importing the CSS file for Login styling
import Chessboard from './components/Chessboard/Chessboard'; // Import the Chessboard component

// Login component
function Login() {
  // Setting up state variables for username, password, and login status
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false); // State variable to track if the user is logged in

  // Function to handle the login process
  const handleLogin = (e) => {
    e.preventDefault(); // Prevent the form from submitting

    // You can add your authentication logic here
    // For simplicity, we'll just check if the username and password are not empty
    if (username !== '' && password !== '') {
      setLoggedIn(true); // Set the loggedIn state to true if the username and password are not empty
    } else {
      alert('Please enter both username and password.'); // Alert the user to enter both username and password if they are empty
    }
  };

  // JSX content for the Login component
  return (
    <div className="login-container"> {/* Main container for the login component */}
      {!loggedIn ? ( // Check if the user is not logged in
        <> {/* Fragment shorthand */}
          <h2>Login</h2> {/* Heading for the login section */}
          <form onSubmit={handleLogin}> {/* Login form with a submit event handler */}
            <div className="form-group"> {/* Container for the username input field */}
              <label htmlFor="username">Username:</label> {/* Label for the username input field */}
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)} // Event handler for changing the username state
              />
            </div>
            <div className="form-group"> {/* Container for the password input field */}
              <label htmlFor="password">Password:</label> {/* Label for the password input field */}
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)} // Event handler for changing the password state
              />
            </div>
            <button type="submit">Login</button> {/* Button to submit the form */}
          </form>
        </>
      ) : (
        <Chessboard /> // Render the Chessboard component if the user is logged in
      )}
    </div>
  );
}

// Export the Login component as the default export
export default Login;
