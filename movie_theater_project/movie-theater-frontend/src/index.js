import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';  // ← Bootstrap CSS
import './index.css';
import App from './App';                         // ← import App only once
import './styles/theme.css';
import { AuthProvider } from './contexts/AuthContext'; // ← import AuthProvider
import { ToastProvider } from './contexts/ToastContext';
import { NotificationsProvider } from './contexts/NotificationContext'; // ← import NotificationsProvider
const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);

root.render(
  <React.StrictMode>
      <AuthProvider>
            <ToastProvider>
              <NotificationsProvider>
                <App />
              </NotificationsProvider>
            </ToastProvider>
      </AuthProvider>
  </React.StrictMode>
);