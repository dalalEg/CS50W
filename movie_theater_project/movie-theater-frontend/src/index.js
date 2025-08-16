import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';  // ← Bootstrap CSS
import './index.css';
import App from './App';                         // ← import App only once
import './styles/theme.css';
import { AuthProvider } from './contexts/AuthContext'; // ← import AuthProvider

const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);

root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);