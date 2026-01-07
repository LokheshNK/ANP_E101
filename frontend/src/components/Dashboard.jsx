import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';

const Dashboard = ({ data, onUserSelect }) => {
  const getColor = (node) => {
    if (node.imp_z > 0 && node.vis_z < 0) return '#10b981'; // Green: Silent Architect
    if (node.imp_z > 0 && node.vis_z > 0) return '#3b82f6'; // Blue: Force Multiplier
    if (node.imp_z < 0 && node.vis_z > 0) return '#f59e0b'; // Orange: Socialite
    return '#ef4444'; // Red: Underperformer
  };

  return (
    <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-2xl h-full">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-slate-200">The Disparity Quadrant</h2>
        <div className="flex gap-4 text-xs">
          <span className="flex items-center gap-1 text-emerald-400">● Architect</span>
          <span className="flex items-center gap-1 text-blue-400">● Leader</span>
          <span className="flex items-center gap-1 text-amber-400">● Socialite</span>
        </div>
      </div>
      
      <div className="h-[500px] w-full">
        <ResponsiveContainer>
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <XAxis type="number" dataKey="vis_z" name="Visibility" stroke="#64748b" label={{ value: 'Visibility (Noise)', position: 'insideBottom', offset: -5, fill: '#64748b' }} />
            <YAxis type="number" dataKey="imp_z" name="Impact" stroke="#64748b" label={{ value: 'Impact (Signal)', angle: -90, position: 'insideLeft', fill: '#64748b' }} />
            <ZAxis dataKey="name" name="Engineer" />
            <Tooltip 
              cursor={{ strokeDasharray: '3 3' }} 
              contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '8px' }}
            />
            <ReferenceLine x={0} stroke="#334155" strokeWidth={2} />
            <ReferenceLine y={0} stroke="#334155" strokeWidth={2} />
            <Scatter data={data} onClick={(e) => onUserSelect(e.payload)}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getColor(entry)} className="cursor-pointer hover:opacity-80 transition-opacity" />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Dashboard;