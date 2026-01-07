import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import UserStats from './components/UserStats';

function App() {
  const [data, setData] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/dashboard')
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div className="flex h-screen bg-slate-950 text-slate-200">
      <Sidebar />
      <main className="flex-1 flex flex-col p-8 overflow-hidden">
        <div className="flex justify-between items-start mb-10">
          <div>
            <h1 className="text-4xl font-bold text-white tracking-tight">Engineering Truth Layer</h1>
            <p className="text-slate-400 mt-2">Validating impact through cross-platform signal correlation.</p>
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-full font-semibold transition-all shadow-lg shadow-blue-900/20">
            Sync Data
          </button>
        </div>

        <div className="flex gap-8 flex-1">
          <div className="flex-[2]">
            <Dashboard data={data} onUserSelect={setSelectedUser} />
          </div>
          <div className="flex-1 bg-slate-900 p-8 rounded-2xl border border-slate-800 shadow-2xl">
            <h2 className="text-xl font-semibold mb-6">User Deep-Dive</h2>
            <UserStats user={selectedUser} />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;