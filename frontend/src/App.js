import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState([]);
  const [teamAnalysis, setTeamAnalysis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPoint, setSelectedPoint] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [scoresResponse, teamResponse] = await Promise.all([
        axios.get('/api/scores'),
        axios.get('/api/team-analysis')
      ]);
      
      setData(scoresResponse.data.data || []);
      setTeamAnalysis(teamResponse.data.teams || []);
      setError(null);
    } catch (err) {
      setError('Failed to fetch data from API');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    fetchData();
  };

  const handlePointSelect = (point) => {
    setSelectedPoint(point);
  };

  return (
    <div className="app">
      <Sidebar 
        selectedPoint={selectedPoint}
        teamAnalysis={teamAnalysis}
        onRefresh={handleRefresh}
        loading={loading}
        error={error}
      />
      <main className="main-content">
        <Dashboard 
          data={data}
          loading={loading}
          error={error}
          onPointSelect={handlePointSelect}
        />
      </main>
    </div>
  );
}

export default App;