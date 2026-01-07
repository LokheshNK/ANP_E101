import React from 'react';
import { Zap, MessageSquare, Code, Users } from 'lucide-react';

const UserStats = ({ user }) => {
  if (!user) return <div className="text-slate-500 italic mt-20 text-center">Select a dot to view deep-dive metrics</div>;

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="border-b border-slate-800 pb-4">
        <h3 className="text-2xl font-bold text-white">{user.name}</h3>
        <p className="text-blue-400 font-medium">{user.imp_z > 0 && user.vis_z < 0 ? 'Silent Architect' : 'Team Member'}</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-slate-800/50 p-4 rounded-xl">
          <Code className="text-emerald-400 mb-2" size={20} />
          <div className="text-xs text-slate-400 uppercase">Commits</div>
          <div className="text-xl font-bold text-white">{user.commits}</div>
        </div>
        <div className="bg-slate-800/50 p-4 rounded-xl">
          <Zap className="text-blue-400 mb-2" size={20} />
          <div className="text-xs text-slate-400 uppercase">Entropy</div>
          <div className="text-xl font-bold text-white">{user.entropy.toFixed(2)}</div>
        </div>
        <div className="bg-slate-800/50 p-4 rounded-xl">
          <MessageSquare className="text-amber-400 mb-2" size={20} />
          <div className="text-xs text-slate-400 uppercase">Chat Signal</div>
          <div className="text-xl font-bold text-white">{user.comm_score.toFixed(1)}</div>
        </div>
        <div className="bg-slate-800/50 p-4 rounded-xl">
          <Users className="text-purple-400 mb-2" size={20} />
          <div className="text-xs text-slate-400 uppercase">Meetings</div>
          <div className="text-xl font-bold text-white">{user.meetings}h</div>
        </div>
      </div>
    </div>
  );
};

export default UserStats;