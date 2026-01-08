import React, { useState, useEffect } from 'react';
import { AppProvider, useApp } from './context/AppContext';
import Login from './components/Login';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import TeamAnalytics from './components/TeamAnalytics';
import Settings from './components/Settings';
import UserStats from './components/UserStats';

const AppContent = () => {
  const { user, getMockData, settings } = useApp();
  const [data, setData] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [currentView, setCurrentView] = useState('dashboard');

  useEffect(() => {
    const fetchData = async () => {
      if (user) {
        // Get data from API based on logged-in user's company
        const response = await getMockData();
        if (response && response.developers) {
          setData(response.developers);
          if (response.developers.length > 0) setSelectedUser(response.developers[0]);
        } else {
          setData([]);
        }
      }
    };

    fetchData();
  }, [user, getMockData]);

  // If no user is logged in, show login page
  if (!user) {
    return <Login />;
  }

  const renderContent = () => {
    switch (currentView) {
      case 'team-analytics':
        return <TeamAnalytics data={data} settings={settings} />;
      case 'settings':
        return <Settings />;
      case 'dashboard':
      default:
        return (
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
            <div className="xl:col-span-3">
              <Dashboard data={data} onUserSelect={setSelectedUser} settings={settings} />
            </div>
            <div className="xl:col-span-1 bg-gray-50 p-8 rounded-xl border border-gray-200 shadow-sm">
              <UserStats user={selectedUser} settings={settings} />
            </div>
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-white text-black overflow-hidden font-sans">
      <Sidebar currentView={currentView} onViewChange={setCurrentView} user={user} />
      
      <main className="flex-1 p-8 overflow-y-auto">
        {currentView === 'dashboard' && (
          <header className="flex justify-between items-end mb-12">
            <div>
              <h1 className="text-5xl font-black text-black tracking-tighter">DEVLENS<span className="text-green-600">.</span></h1>
              <p className="text-gray-600 text-lg mt-2 font-light">Advanced Developer Performance Analytics Platform</p>
              <p className="text-sm text-gray-500 mt-1">{user.company} • {user.name}</p>
            </div>
            <div className="bg-gray-50 border border-gray-200 px-6 py-3 rounded-xl shadow-sm">
              <span className="text-xs text-gray-500 uppercase font-semibold block">System Status</span>
              <span className="text-green-600 font-mono text-sm">Active • Real-time Analytics</span>
            </div>
          </header>
        )}

        {renderContent()}
      </main>
    </div>
  );
};

function App() {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
}

export default App;