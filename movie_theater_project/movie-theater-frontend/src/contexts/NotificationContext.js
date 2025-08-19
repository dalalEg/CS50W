import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchNotifications, markNotificationRead } from '../api/notification';
import { useAuth } from './AuthContext';

const NotificationsContext = createContext();
export const useNotifications = () => useContext(NotificationsContext);

export function NotificationsProvider({ children }) {
  const { user, loading: authLoading } = useAuth();
  const [notes, setNotes] = useState([]);

  const reload = () => {
    if (!user) return Promise.resolve(setNotes([]));
    return fetchNotifications()
      .then(r => setNotes(r.data))
      .catch(() => setNotes([]));
  };

  // reload every time auth finishes loading, and user flips from null→object or vice-versa
  useEffect(() => {
    if (!authLoading) reload();
  }, [authLoading, user]);

  // OPTIONAL: poll every 30s for new
   useEffect(() => {
     if (user) {
       const iv = setInterval(reload, 30000);
      return () => clearInterval(iv);
    }
  }, [user]);

  const markRead = id =>
    markNotificationRead(id).then(() => reload());

  return (
    <NotificationsContext.Provider value={{ notes, reload, markRead }}>
      {children}
    </NotificationsContext.Provider>
  );
}
