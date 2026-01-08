import React, { createContext, useContext, useState, useEffect } from 'react';

// 1. DYNAMIC API URL CONFIGURATION
// On Vercel, it will use the Render URL. Locally, it stays on localhost.
const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [settings, setSettings] = useState(null);

  // Load user and settings from localStorage
  useEffect(() => {
    const savedUser = localStorage.getItem('devlens-user');
    const savedSettings = localStorage.getItem('devlens-settings');
    
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    } else {
      // Default settings
      const defaultSettings = {
        notifications: {
          emailAlerts: true,
          performanceAlerts: true,
          weeklyReports: false,
          teamUpdates: true,
          criticalIssues: true,
          emailAddress: ''
        },
        dashboard: {
          refreshInterval: '5',
          defaultView: 'dashboard',
          showAnimations: true,
          compactMode: false,
          darkMode: false
        },
        analytics: {
          trackingPeriod: '30',
          minCommitsThreshold: '1',
          impactCalculation: 'weighted',
          excludeWeekends: false,
          includeDocumentation: true
        },
        team: {
          autoAssignTeams: true,
          allowTeamSwitching: false,
          requireApproval: true,
          showSensitiveData: false
        },
        privacy: {
          anonymizeData: false,
          retentionPeriod: '365',
          shareAnalytics: false,
          exportEnabled: true
        }
      };
      setSettings(defaultSettings);
      localStorage.setItem('devlens-settings', JSON.stringify(defaultSettings));
    }
  }, []);

  const login = async (email, password, company) => {
    try {
      // 2. UPDATED TO USE API_URL
      const response = await fetch(`${API_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, company }),
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data.user);
        localStorage.setItem('devlens-user', JSON.stringify(data.user));
        return { success: true };
      } else {
        const error = await response.json();
        return { success: false, error: error.detail || 'Login failed' };
      }
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Network error' };
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('devlens-user');
    localStorage.removeItem('devlens-settings');
    setSettings(null);
  };

  const updateSettings = (newSettings) => {
    setSettings(newSettings);
    localStorage.setItem('devlens-settings', JSON.stringify(newSettings));
  };

  // Get data from API based on company
  const getMockData = async () => {
    if (!user) return { developers: [] };

    try {
      // 3. UPDATED TO USE API_URL
      const response = await fetch(`${API_URL}/api/dashboard/${encodeURIComponent(user.company)}`);
      if (response.ok) {
        const data = await response.json();
        console.log('API Response received from:', API_URL); 
        return data;
      } else {
        console.error('API Error:', response.status, response.statusText);
        return { developers: [] };
      }
    } catch (error) {
      console.error('Error fetching data from backend:', error);
      return { developers: [] };
    }
  };

  const value = {
    user,
    settings,
    login,
    logout,
    updateSettings,
    getMockData
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export default AppContext;
