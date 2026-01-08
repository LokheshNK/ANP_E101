import React from 'react';
<<<<<<< HEAD
import { LayoutDashboard, Users, Settings, Shield, LogOut, User, Brain, BookOpen } from 'lucide-react';
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
          onClick={() => onViewChange('nlp-demo')}
          className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border transition-all ${
            currentView === 'nlp-demo' 
              ? 'bg-blue-100 text-blue-700 border-blue-200' 
              : 'text-gray-600 hover:text-black hover:bg-gray-100 border-transparent'
          }`}
        >
          <Brain size={18} /> 
          <span className="font-medium">NLP Visibility</span>
        </div>
        <div 
          onClick={() => onViewChange('methodology')}
          className={`flex items-center gap-3 p-3 rounded-lg cursor-pointer border transition-all ${
            currentView === 'methodology' 
              ? 'bg-purple-100 text-purple-700 border-purple-200' 
              : 'text-gray-600 hover:text-black hover:bg-gray-100 border-transparent'
          }`}
        >
          <BookOpen size={18} /> 
          <span className="font-medium">Methodology</span>
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
=======
import './Sidebar.css';

const Sidebar = ({ selectedPoint, teamAnalysis, onRefresh, loading, error }) => {
  const getQuadrantInfo = (x, y) => {
    if (x >= 0 && y >= 0) {
      return {
        quadrant: "Q1: High Visibility, High Impact",
        description: "Star performers with high visibility and impact",
        color: "#22c55e"
      };
    }
    if (x < 0 && y >= 0) {
      return {
        quadrant: "Q2: Low Visibility, High Impact",
        description: "Hidden gems with high impact but low visibility",
        color: "#16a34a"
      };
    }
    if (x < 0 && y < 0) {
      return {
        quadrant: "Q3: Low Visibility, Low Impact",
        description: "Teams needing attention and support",
        color: "#15803d"
      };
    }
    return {
      quadrant: "Q4: High Visibility, Low Impact",
      description: "Teams with high visibility but lower impact",
      color: "#166534"
    };
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>DevLens</h2>
        <p className="sidebar-subtitle">Team Analytics</p>
      </div>

      <div className="sidebar-section">
        <button 
          className="refresh-btn btn"
          onClick={onRefresh}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh Data'}
        </button>
      </div>

      {error && (
        <div className="sidebar-section">
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        </div>
      )}

      <div className="sidebar-section">
        <h3>Team Analysis</h3>
        <div className="team-analysis">
          {teamAnalysis.map((team, index) => (
            <div key={index} className="team-card">
              <div className="team-header">
                <h4>{team.name}</h4>
                <span className="member-count">{team.total_members} members</span>
              </div>
              <div className="team-stats">
                <div className="stat-row">
                  <span className="stat-label">Avg Visibility:</span>
                  <span className="stat-value">{team.avg_visibility.toFixed(2)}</span>
                </div>
                <div className="stat-row">
                  <span className="stat-label">Avg Impact:</span>
                  <span className="stat-value">{team.avg_impact.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {selectedPoint && (
        <div className="sidebar-section">
          <h3>Selected Team Member</h3>
          <div className="selected-point-info">
            <div className="point-id">
              <strong>Name:</strong> {selectedPoint.name || selectedPoint.id}
            </div>
            {selectedPoint.team && (
              <div className="point-team">
                <strong>Team:</strong> {selectedPoint.team}
              </div>
            )}
            <div className="point-coords">
              <div className="coord-item">
                <span className="coord-label">Visibility:</span>
                <span className="coord-value">{selectedPoint.x.toFixed(3)}</span>
              </div>
              <div className="coord-item">
                <span className="coord-label">Impact:</span>
                <span className="coord-value">{selectedPoint.y.toFixed(3)}</span>
              </div>
            </div>
            <div className="quadrant-info">
              {(() => {
                const info = getQuadrantInfo(selectedPoint.x, selectedPoint.y);
                return (
                  <>
                    <div className="quadrant-label" style={{ color: info.color }}>
                      {info.quadrant}
                    </div>
                    <div className="quadrant-description">
                      {info.description}
                    </div>
                  </>
                );
              })()}
            </div>
          </div>
        </div>
      )}

      <div className="sidebar-section">
        <h3>Quadrant Guide</h3>
        <div className="quadrant-guide">
          <div className="guide-item">
            <div className="guide-color q1"></div>
            <div className="guide-text">
              <strong>Q1:</strong> Star Performers
            </div>
          </div>
          <div className="guide-item">
            <div className="guide-color q2"></div>
            <div className="guide-text">
              <strong>Q2:</strong> Hidden Gems
            </div>
          </div>
          <div className="guide-item">
            <div className="guide-color q3"></div>
            <div className="guide-text">
              <strong>Q3:</strong> Need Support
            </div>
          </div>
          <div className="guide-item">
            <div className="guide-color q4"></div>
            <div className="guide-text">
              <strong>Q4:</strong> High Visibility
            </div>
          </div>
        </div>
      </div>
>>>>>>> 115173da8f5783f233c9214b986ef3c3f815ef23
    </div>
  );
};

export default Sidebar;