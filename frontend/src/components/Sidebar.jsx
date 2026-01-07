import React from 'react';
import { LayoutDashboard, Users, Settings, ShieldCheck } from 'lucide-react';

const Sidebar = () => (
  <div className="w-64 bg-slate-950 border-r border-slate-800 p-6 flex flex-col gap-8">
    <div className="flex items-center gap-3 text-blue-500 font-black text-2xl italic">
      <ShieldCheck size={32} /> DEVLENS
    </div>
    <nav className="flex flex-col gap-2">
      <div className="flex items-center gap-3 p-3 bg-blue-600/10 text-blue-400 rounded-lg cursor-pointer">
        <LayoutDashboard size={20} /> Dashboard
      </div>
      <div className="flex items-center gap-3 p-3 text-slate-500 hover:bg-slate-900 rounded-lg cursor-pointer transition-colors">
        <Users size={20} /> Team View
      </div>
      <div className="flex items-center gap-3 p-3 text-slate-500 hover:bg-slate-900 rounded-lg cursor-pointer transition-colors">
        <Settings size={20} /> Configuration
      </div>
    </nav>
  </div>
);

export default Sidebar;