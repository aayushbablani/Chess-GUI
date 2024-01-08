// Import necessary modules and components
import React, { useState } from "react";
import "./Login.css"; // Importing the CSS file for Login styling
import Chessboard from "./components/Chessboard/Chessboard"; // Import the Chessboard component
import Selection from './components/Selection/Selection'; // Import the Chessboard component
import Referee from "./components/Referee/Referee";

// Login component
function Login() {
  // Setting up state variables for username, password, and login status
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false); // State variable to track if the user is logged in
  const [isImageClicked, setIsImageClicked] = useState(false);

  // Function to handle the login process
  const handleLogin = (e) => {
    e.preventDefault(); // Prevent the form from submitting

    // You can add your authentication logic here
    // For simplicity, we'll just check if the username and password are not empty
    if (username !== "" && password !== "") {
      setLoggedIn(true); // Set the loggedIn state to true if the username and password are not empty
    } else {
      alert("Please enter both username and password."); // Alert the user to enter both username and password if they are empty
    }
  };

  // JSX content for the Login component
  return (
    <div className="login-container">
      {" "}
      {/* Main container for the login component */}
      {!loggedIn ? ( // Check if the user is not logged in
        <>
          {" "}
          {/* Fragment shorthand */}
          <h2 style={{color: 'white'}}>Login</h2> {/* Heading for the login section */}
          <form onSubmit={handleLogin}>
            {" "}
            {/* Login form with a submit event handler */}
            <div className="form-group">
              {" "}
              {/* Container for the username input field */}
              <label htmlFor="username">Username:</label>{" "}
              {/* Label for the username input field */}
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)} // Event handler for changing the username state
              />
            </div>
            <div className="form-group">
              {" "}
              {/* Container for the password input field */}
              <label htmlFor="password">Password:</label>{" "}
              {/* Label for the password input field */}
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)} // Event handler for changing the password state
              />
            </div>
            <button type="submit">Login</button>{" "}
            {/* Button to submit the form */}
          </form>
        </>
      ) : (
        !isImageClicked && (
          <div>
            <User /> {/* Component for the User Icon */}
            <Selection /> {/* Component for the Home Page. */}
            <HomeExit /> {/* Component for the Home Button and Log Out Button. */}
          </div> // Render the Home Page if the user is logged in.
        )
      )}
    </div>
  );

  function User() { /* Profile Icon displaying the username of the user currently logged in.*/
    
    return (
      <div className='profileIcon'> {/* See Selection.css for the corresponding styles for this class. */}
        <img src="assets/images/profile_icon.svg" alt={`Profile Icon for ${username}`} width="4%" style={{paddingRight: 10}}/>
        <h2 className='profileName'>
          {username}
        </h2>
      </div>
    )
  }

  function HomeExit() { /* Home Button and Log Out Buttons located in the bottom right corner. */

    const [isIconsVisible, setIsIconsVisible] = useState(true);
    const [ImgClicked, setImgClicked] = useState(null);

    const handleHomeClick = () => {
      setIsImageClicked(true);
      setIsImageClicked(false);
      setImgClicked('home');
    };

    const handleExitClick = () => {
      setImgClicked('exit');
      setIsImageClicked(false);
      setIsIconsVisible(false);
    }

    return (
      <div className='home_exitIcons'>
        {isIconsVisible && (
          <>
            <img className='home_Icon' src='assets/images/home_icon.svg' alt='Click house to go back home' width="3%" onClick={handleHomeClick}/>
            <img className='exit_Icon' src='assets/images/exit_icon.svg' alt='Click exit to log out' width="3%" onClick={handleExitClick}/>
          </>
        )}

        {ImgClicked === 'home' && (
          <>
            <User />
            <Selection />
            <HomeExit />
          </>
        )}

        {ImgClicked === 'exit' && (
          <>
            <Login />
          </>
        )}

      </div>
    )

  }




}

// Export the Login component as the default export
export default Login;
