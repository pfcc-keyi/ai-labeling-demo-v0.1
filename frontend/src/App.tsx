import { useState, useEffect } from 'react';
import Login from './components/Login';
import LabelingInterface from './components/LabelingInterface';
import { isAuthenticated } from './utils/auth';

function App() {
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
  }, []);

  const handleLoginSuccess = () => {
    setAuthenticated(true);
  };

  const handleLogout = () => {
    setAuthenticated(false);
  };

  return (
    <>
      {authenticated ? (
        <LabelingInterface onLogout={handleLogout} />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </>
  );
}

export default App; 