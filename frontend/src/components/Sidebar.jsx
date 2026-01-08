import React from 'react';
import { LayoutDashboard, Users, Settings, Shield, LogOut, User } from 'lucide-react';
import { useApp } from '../context/AppContext';

const Sidebar = ({ currentView, onViewChange }) => {
  const { user, logout } = useApp();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="w-64 bg-gray-50 border-r border-gray-200 p-6 flex flex-col gap-8">
      <div className="flex items-center gap-3 text-green-600 font-bold text-xl">
        <Shield size={28} /> 
        <span>DEVLENS</span>
      </div>
      
      {/* User Info */}
      <div className="bg-white p-4 rounded-lg border border-gray-200">
        <div className="flex items-center gap-3 mb-2">
          <User size={20} className="text-gray-600" />
          <div>
            <p className="font-medium text-black text-sm">{user?.name}</p>
            <p className="text-xs text-gray-500">{user?.role}</p>
          </div>
        </div>
        <p className="text-xs text-gray-500">{user?.company}</p>
      </div>

      <nav className="flex flex-col gap-2 flex-1">
        <div 
          onClick={() => onViewChange('dashboard')}
          className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border transition-all ${
            currentView === 'dashboard' 
              ? 'bg-green-100 text-green-700 border-green-200' 
              : 'text-gray-600 hover:text-black hover:bg-gray-100 border-transparent'
          }`}
        >
          <LayoutDashboard size={18} /> 
          <span className="font-medium">Dashboard</span>
        </div>
        <div 
          onClick={() => onViewChange('team-analytics')}
          className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border transition-all ${
            currentView === 'team-analytics' 
              ? 'bg-green-100 text-green-700 border-green-200' 
              : 'text-gray-600 hover:text-black hover:bg-gray-100 border-transparent'
          }`}
        >
          <Users size={18} /> 
          <span className="font-medium">Team Analytics</span>
        </div>
        <div 
          onClick={() => onViewChange('settings')}
          className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border transition-all ${
            currentView === 'settings' 
              ? 'bg-green-100 text-green-700 border-green-200' 
              : 'text-gray-600 hover:text-black hover:bg-gray-100 border-transparent'
          }`}
        >
          <Settings size={18} /> 
          <span className="font-medium">Settings</span>
        </div>
      </nav>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        className="flex items-center gap-3 p-3 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg cursor-pointer transition-all border border-transparent hover:border-red-200"
      >
        <LogOut size={18} /> 
        <span className="font-medium">Logout</span>
      </button>
    </div>
  );
};

export default Sidebar;