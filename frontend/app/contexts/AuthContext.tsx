'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';

interface AuthContextValue {
  isAuthenticated: boolean;
  email: string | null;
  login: (email: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [email, setEmail] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window === 'undefined') return;
    const storedEmail = window.localStorage.getItem('trendscout_email');
    if (storedEmail) {
      setEmail(storedEmail);
      setIsAuthenticated(true);
    }
  }, []);

  const login = (userEmail: string) => {
    window.localStorage.setItem('trendscout_email', userEmail);
    setEmail(userEmail);
    setIsAuthenticated(true);
  };

  const logout = () => {
    window.localStorage.removeItem('trendscout_email');
    setEmail(null);
    setIsAuthenticated(false);
  };

  const value = useMemo(
    () => ({ isAuthenticated, email, login, logout }),
    [isAuthenticated, email]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
