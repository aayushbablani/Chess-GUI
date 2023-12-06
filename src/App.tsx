// Importing necessary modules
import React from 'react';
import './App.css'; // Importing the CSS file for App styling
import Login from './Login'; // Import the Login component

// Main App component
function App() {
  return (
    <div id='app'> {/* Root container with the id 'app' */}
      <Login /> {/* Rendering the Login component */}
    </div>
  );
}

// Exporting the App component as the default export
export default App;
