import { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import Register from './components/Register'; 

// --- Sub-Component 1: Moved OUTSIDE and accepts props ---
const LoginView = ({ token, error, handleLogin, username, setUsername, password, setPassword }) => (
  token ? <Navigate to="/dashboard" replace /> : (
    <div style={{ maxWidth: '400px', margin: '100px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', fontFamily: 'sans-serif' }}>
      <h2>Rosana Tool</h2>
      <h3>User Sign In</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Username:</label>
          <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }} />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>Password:</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }} />
        </div>
        <button type="submit" style={{ width: '100%', padding: '10px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Login</button>
      </form>
      <p style={{ marginTop: '15px', fontSize: '14px', textAlign: 'center' }}>
        Need a new profile? <Link to="/register" style={{ color: '#007bff', textDecoration: 'none', fontWeight: 'bold' }}>Create an account</Link>
      </p>
    </div>
  )
);

// --- Sub-Component 2: Moved OUTSIDE and accepts props ---
const DashboardView = ({ token, handleLogout, userProfile }) => (
  !token ? <Navigate to="/login" replace /> : (
    <div style={{ maxWidth: '700px', margin: '50px auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
        <h2>Rosana Safety Workspace</h2>
        <button onClick={handleLogout} style={{ padding: '8px 15px', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Logout</button>
      </div>

      {userProfile ? (
        <div style={{ marginTop: '20px' }}>
          <div style={{ background: '#f8f9fa', padding: '20px', borderRadius: '8px', border: '1px solid #e9ecef', marginBottom: '20px' }}>
            <h3 style={{ marginTop: 0 }}>Welcome back, {userProfile.username}!</h3>
            <p style={{ margin: '5px 0' }}><strong>Email Context:</strong> {userProfile.email}</p>
            <p style={{ margin: '5px 0' }}>Company Name: {userProfile.company_name || <em style={{ color: '#999' }}>Not Specified</em>}</p>
            <p style={{ margin: '5px 0' }}>Mailing Address: {userProfile.mailing_address || <em style={{ color: '#999' }}>Not Specified</em>}</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
            <div style={{ border: '1px solid #e0e0e0', padding: '15px', borderRadius: '8px' }}>
              <h4 style={{ marginTop: 0 }}>Licensing Details</h4>
              <p>Tier: <span style={{ padding: '3px 8px', borderRadius: '4px', color: 'white', fontWeight: 'bold', fontSize: '12px', background: userProfile.account_type === 'admin' ? '#dc3545' : userProfile.account_type === 'premium' ? '#ffc107' : '#6c757d' }}>{userProfile.account_type ? userProfile.account_type.toUpperCase() : 'REGULAR'}</span></p>
              <p style={{ fontSize: '14px' }}>Renewal Date: {userProfile.subscription_end_date ? userProfile.subscription_end_date : 'Lifetime Access'}</p>
            </div>

            <div style={{ border: '1px solid #e0e0e0', padding: '15px', borderRadius: '8px' }}>
              <h4 style={{ marginTop: 0 }}>System Standing</h4>
              <p style={{ margin: 0 }}>Status: <span style={{ padding: '3px 8px', borderRadius: '4px', color: 'white', fontWeight: 'bold', fontSize: '12px', background: userProfile.account_standing === 'good' ? '#28a745' : '#6c757d' }}>{userProfile.account_standing ? userProfile.account_standing.toUpperCase() : 'GOOD'}</span></p>
            </div>
          </div>

          <div style={{ background: '#ffffff', padding: '15px', border: '1px solid #e0e0e0', borderRadius: '8px' }}>
            <h4 style={{ marginTop: 0 }}>Authorized FIPS Regional Coverage:</h4>
            {userProfile.fips_codes && userProfile.fips_codes.length > 0 ? (
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginTop: '10px' }}>
                {userProfile.fips_codes.map((code) => (
                  <span key={code} style={{ background: '#e2e3e5', padding: '6px 12px', borderRadius: '20px', fontSize: '14px', border: '1px solid #ced4da' }}>
                    📍 FIPS: {code}
                  </span>
                ))}
              </div>
            ) : (
              <p style={{ color: '#856404', background: '#fff3cd', padding: '10px', borderRadius: '4px', margin: 0 }}>
                ⚠️ No spatial access permissions assigned.
              </p>
            )}
          </div>
        </div>
      ) : (
        <p>Verifying secure data payload clearance...</p>
      )}
    </div>
  )
);

// --- Main App Component ---
function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState(localStorage.getItem('accessToken') || '');
  const [userProfile, setUserProfile] = useState(null);
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/api/token/', {
        username,
        password,
      });
      const accessToken = response.data.access;
      localStorage.setItem('accessToken', accessToken);
      setToken(accessToken);
    } catch (err) {
      setError('Login failed. Please check your username and password.');
    }
  };

  const fetchProfile = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/profile/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUserProfile(response.data);
    } catch (err) {
      setError('Failed to fetch user profile. Token might be expired.');
      handleLogout();
    }
  };

  useEffect(() => {
    if (token) {
      fetchProfile();
    }
  }, [token]);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    setToken('');
    setUserProfile(null);
    setUsername('');
    setPassword('');
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={token ? <Navigate to="/dashboard" replace /> : <Navigate to="/login" replace />} />
        
        {/* Pass state and handlers via props down into the components */}
        <Route 
          path="/login" 
          element={
            <LoginView 
              token={token} 
              error={error} 
              handleLogin={handleLogin} 
              username={username} 
              setUsername={setUsername} 
              password={password} 
              setPassword={setPassword} 
            />
          } 
        />
        
        <Route path="/register" element={<Register />} />
        
        <Route 
          path="/dashboard" 
          element={
            <DashboardView 
              token={token} 
              handleLogout={handleLogout} 
              userProfile={userProfile} 
            />
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;