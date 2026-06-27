import React, { useState } from 'react';

function Register() {
  // State buckets to track form inputs
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    account_type: 'regular', // Default selection
    fips_input: '' // Temporary bucket for comma-separated FIPS codes
  });

  const [message, setMessage] = useState({ text: '', isError: false });

  // Update state whenever a user types into a field
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // Submit the form data to the Django Cloud backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ text: '', isError: false });

    // Clean up the input string of FIPS codes into an array of trimmed strings
    const fipsArray = formData.fips_input
      .split(',')
      .map(code => code.trim())
      .filter(code => code.length > 0);

    const payload = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      account_type: formData.account_type,
      fips_codes: fipsArray
    };

    try {
      // Replace with your actual Google Cloud Run or local server URL
      const response = await fetch('http://127.0.0.1:8000/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage({ text: result.message, isError: false });
        // Optional: clear form data here on successful account generation
      } else {
        setMessage({ text: result.error || "Registration failed", isError: true });
      }
    } catch (error) {
      setMessage({ text: "Cannot connect to server. Check backend routing status.", isError: true });
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Create New Account</h2>
      
      {message.text && (
        <div style={{ color: message.isError ? 'red' : 'green', marginBottom: '15px' }}>
          {message.text}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block' }}>Username:</label>
          <input 
            type="text" name="username" value={formData.username} 
            onChange={handleChange} required style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block' }}>Email Address:</label>
          <input 
            type="email" name="email" value={formData.email} 
            onChange={handleChange} required style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block' }}>Password:</label>
          <input 
            type="password" name="password" value={formData.password} 
            onChange={handleChange} required style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label style={{ display: 'block' }}>Account Level:</label>
          <select name="account_type" value={formData.account_type} onChange={handleChange} style={{ width: '100%', padding: '8px' }}>
            <option value="regular">Regular</option>
            <option value="premium">Premium</option>
            <option value="admin">Admin</option>
          </select>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block' }}>Regional FIPS Codes (comma separated):</label>
          <input 
            type="text" name="fips_input" value={formData.fips_input} 
            onChange={handleChange} placeholder="e.g. 1900100000, 1900100370"
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Register Account
        </button>
      </form>
    </div>
  );
}

export default Register;