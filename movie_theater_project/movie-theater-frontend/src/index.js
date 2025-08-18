import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';  // ← Bootstrap CSS
import './index.css';
import App from './App';                         // ← import App only once
import './styles/theme.css';
import { AuthProvider } from './contexts/AuthContext'; // ← import AuthProvider
import { NotificationProvider } from './contexts/NotificationContext';
const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);

root.render(
  <React.StrictMode>
    <NotificationProvider>
    <AuthProvider>

        <App />
      </AuthProvider>
    </NotificationProvider>
  </React.StrictMode>
);