import React, { createContext, useContext, useState } from 'react';
export const ToastContext = createContext();
export const useToast = () => useContext(ToastContext);

export function ToastProvider({ children }) {
  const [note, setNote] = useState(null);

  const show = (message, type = 'info') => {
    setNote({ message, type });
    setTimeout(() => setNote(null), 3000);
  };

  return (
    <ToastContext.Provider value={{ show }}>
      {note && (
        <div className={`notification ${note.type}`}>
          {note.message}
        </div>
      )}
      {children}
    </ToastContext.Provider>
  );
}