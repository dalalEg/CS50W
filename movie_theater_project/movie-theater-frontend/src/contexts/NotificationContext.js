import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { fetchNotifications, markNotificationRead } from '../api/notification';
import { useAuth } from './AuthContext';

const NotificationsContext = createContext();
export const useNotifications = () => useContext(NotificationsContext);

export function NotificationsProvider({ children }) {
  const { user, loading: authLoading } = useAuth();
  const [notes, setNotes] = useState([]);

  const reload = useCallback(() => {
    if (!user) return Promise.resolve(setNotes([]));
    return fetchNotifications()
      .then(r => setNotes(r.data))
      .catch(() => setNotes([]));
  }, [user]);

  // Reload when auth finishes loading or user changes
  useEffect(() => {
    if (!authLoading) reload();
  }, [authLoading, user, reload]);

  useEffect(() => {
    if (user) {
      const iv = setInterval(reload, 30000);
      return () => clearInterval(iv);
    }
  }, [user, reload]);

  const markRead = id =>
    markNotificationRead(id).then(() => reload());

  const add = (message) => {
    const newNote = { id: Date.now(), message, read: false };  
    setNotes(prev => [newNote, ...prev]);
  };

  return (
    <NotificationsContext.Provider value={{ notes, reload, markRead, add }}>
      {children}
    </NotificationsContext.Provider>
  );
}
