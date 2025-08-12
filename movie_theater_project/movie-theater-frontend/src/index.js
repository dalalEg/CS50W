import React from 'react';
import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';  // ← Bootstrap CSS
import './index.css';
import App from './App';                         // ← import App only once
import './styles/theme.css';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
