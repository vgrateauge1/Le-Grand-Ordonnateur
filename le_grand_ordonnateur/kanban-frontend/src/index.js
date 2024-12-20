import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Supprimez <React.StrictMode> pour éviter les double rendus
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <App />
);
