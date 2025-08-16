import React, { createContext, useContext, useEffect, useState } from 'react';
import { fetchUsers } from '../api/user';
const AuthContext = createContext({ user: null, loading: true });

export function AuthProvider({ children }) {
  const [user, setUser]     = useState(null);
  const [loading, setLoad]  = useState(true);

  useEffect(() => {
      fetchUsers()
      .then(res => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoad(false));
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);