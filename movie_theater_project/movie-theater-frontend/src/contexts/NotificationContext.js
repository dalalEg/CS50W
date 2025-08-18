import React, { createContext, useContext, useState } from 'react';
export const NotificationContext = createContext();
export const useNotification = () => useContext(NotificationContext);

export function NotificationProvider({ children }) {
  const [note, setNote] = useState(null);

  const show = (message, type = 'info') => {
    setNote({ message, type });
    setTimeout(() => setNote(null), 3000);
  };

  return (
    <NotificationContext.Provider value={{ show }}>
      {note && (
        <div className={`notification ${note.type}`}>
          {note.message}
        </div>
      )}
      {children}
    </NotificationContext.Provider>
  );
}