import React, { useState } from 'react';
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // Make a POST request to your authentication endpoint
    axios.post('http://localhost:8000/api/auth/', { username, password })
      .then(response => {
        // Handle successful login, e.g., store the token
        console.log('Login successful!', response.data);
      })
      .catch(error => {
        console.error('Login failed:', error);
      });
  };

  return (
    <div>
      <h2>Login</h2>
      <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Login;
