import React from 'react';
import { Activity, MessageSquare, Terminal, Users, User, Calendar, Clock } from 'lucide-react';

const StatCard = ({ icon: Icon, label, value, color, subtitle }) => (
  <div className="bg-white p-4 rounded-lg border border-gray-200 flex flex-col gap-2">
    <Icon size={16} className={color} />
    <span className="text-xs text-gray-500 uppercase font-medium tracking-wide">{label}</span>
    <span className="text-lg font-semibold text-black font-mono">{value}</span>
    {subtitle && <span className="text-xs text-gray-400">{subtitle}</span>}
  </div>
);

const UserStats = ({ user, settings }) => {
  const animationClass = settings?.dashboard?.showAnimations ? 'animate-in slide-in-from-bottom-4 duration-300' : '';

  if (!user) return (
    <div className="h-full flex flex-col items-center justify-center text-gray-500">
      <User size={48} className="mb-4 opacity-50" />
      <p className="text-sm font-medium">Select a developer to view analytics</p>
    </div>
  );

  const getPerformanceCategory = (user) => {
    if (user.is_hidden_gem) return 'Hidden Gem';
    if (user.imp_z > 0 && user.vis_z > 0) return 'Star Performer';
    if (user.imp_z > 0 && user.vis_z < 0) return 'High Impact Contributor';
    if (user.imp_z < 0 && user.vis_z > 0) return 'Team Connector';
    return 'Developing Contributor';
  };

  const getCategoryColor = (user) => {
    if (user.is_hidden_gem) return 'bg-amber-100 text-amber-700 border-amber-200';
    if (user.imp_z > 0 && user.vis_z > 0) return 'bg-green-100 text-green-700 border-green-200';
    if (user.imp_z > 0) return 'bg-blue-100 text-blue-700 border-blue-200';
    if (user.vis_z > 0) return 'bg-purple-100 text-purple-700 border-purple-200';
    return 'bg-gray-100 text-gray-600 border-gray-200';
  };

  const getAttendanceColor = (rate) => {
    const percentage = (rate || 0.85) * 100;
    if (percentage >= 90) return 'text-green-600';
    if (percentage >= 80) return 'text-yellow-600';
    return 'text-red-600';
  };

  const formatAttendancePercentage = (rate) => {
    return `${Math.round((rate || 0.85) * 100)}%`;
  };

  return (
    <div className={animationClass}>
      <div className="mb-8">
        <h3 className="text-2xl font-semibold text-black mb-3">{user.name}</h3>
        <div className="flex flex-col gap-2">
          <span className={`px-3 py-1 text-xs font-medium rounded-full border ${getCategoryColor(user)} w-fit`}>
            {getPerformanceCategory(user)}
          </span>
          <span className="text-xs text-gray-500">{user.team} Team</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-6">
        <StatCard 
          icon={Terminal} 
          label="Commits" 
          value={user.commits} 
          color="text-green-600" 
        />
        <StatCard 
          icon={Activity} 
          label="Complexity" 
          value={user.entropy.toFixed(2)} 
          color="text-green-600" 
        />
        <StatCard 
          icon={MessageSquare} 
          label="Communication" 
          value={user.comm_score.toFixed(1)} 
          color="text-green-600" 
        />
        <StatCard 
          icon={Users} 
          label="Meetings" 
          value={`${user.meetings}h`} 
          color="text-green-600" 
        />
      </div>

      {/* Attendance Section */}
      <div className="mb-6">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <div className="flex items-center gap-2 mb-3">
            <Calendar size={16} className="text-blue-600" />
            <span className="text-sm font-medium text-black">Attendance</span>
          </div>
          <div className="flex items-center justify-between">
            <span className={`text-2xl font-bold font-mono ${getAttendanceColor(user.attendance_rate)}`}>
              {formatAttendancePercentage(user.attendance_rate)}
            </span>
            <div className="text-right">
              <div className="text-xs text-gray-500">
                {user.days_present || Math.round((user.attendance_rate || 0.85) * 20)}/{user.total_work_days || 20} days
              </div>
              <div className="text-xs text-gray-400">
                This period
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="p-4 bg-gray-100 rounded-lg border border-gray-200">
        <h4 className="text-sm font-medium text-black mb-2">Performance Analysis</h4>
        <div className="space-y-2 text-xs text-gray-600 leading-relaxed">
          <p>
            <strong>Overall Score:</strong> {user.overall_performance_score?.toFixed(2) || 'N/A'} 
            <span className="text-gray-500"> (Technical: 40% • Visibility: 30% • Attendance: 30%)</span>
          </p>
          <p>
            <strong>Impact:</strong> {user.imp_z?.toFixed(2)} | <strong>Visibility:</strong> {user.vis_z?.toFixed(2)}
          </p>
          <p>
            This developer demonstrates {user.imp_z > 0 ? 'above-average' : 'standard'} technical impact 
            with {user.vis_z > 0 ? 'high' : 'moderate'} visibility in team communications.
          </p>
          {user.attendance_rate && user.attendance_rate < 0.8 && (
            <p className="text-red-700 bg-red-50 p-2 rounded mt-2">
              <strong>Attendance Impact:</strong> Low attendance ({formatAttendancePercentage(user.attendance_rate)}) 
              significantly reduces overall performance ranking.
            </p>
          )}
          {user.is_hidden_gem && user.attendance_rate >= 0.8 && (
            <p className="text-amber-700 bg-amber-50 p-2 rounded mt-2">
              <strong>Hidden Gem:</strong> High technical contribution with good attendance. 
              Growth potential in visibility and collaboration.
            </p>
          )}
          {user.attendance_rate >= 0.9 && (
            <p className="text-green-700 bg-green-50 p-2 rounded mt-2">
              <strong>Excellent Attendance:</strong> Consistent presence enables strong team collaboration and impact.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserStats;