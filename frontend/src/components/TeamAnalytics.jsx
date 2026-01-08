import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Users, Trophy, TrendingUp, Award, Target, Activity } from 'lucide-react';

const TeamAnalytics = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-gray-500">
        <p>Loading team analytics...</p>
      </div>
    );
  }

  // Group data by teams
  const teamStats = data.reduce((acc, member) => {
    const team = member.team || 'Unassigned';
    if (!acc[team]) {
      acc[team] = {
        name: team,
        members: [],
        totalCommits: 0,
        avgEntropy: 0,
        totalMeetings: 0,
        avgImpact: 0,
        topPerformer: null
      };
    }
    
    acc[team].members.push(member);
    acc[team].totalCommits += member.commits;
    acc[team].totalMeetings += member.meetings;
    
    return acc;
  }, {});

  // Calculate team metrics
  Object.keys(teamStats).forEach(teamName => {
    const team = teamStats[teamName];
    const memberCount = team.members.length;
    
    team.avgEntropy = team.members.reduce((sum, m) => sum + m.entropy, 0) / memberCount;
    team.avgImpact = team.members.reduce((sum, m) => sum + (m.imp_z || 0), 0) / memberCount;
    team.avgCommitsPerMember = team.totalCommits / memberCount;
    team.avgMeetingsPerMember = team.totalMeetings / memberCount;
    
    // Find top performer in team
    team.topPerformer = team.members.reduce((top, current) => 
      (current.imp_z || 0) > (top.imp_z || 0) ? current : top
    );
  });

  const teams = Object.values(teamStats);
  
  // Overall rankings
  const topTeamByCommits = teams.reduce((top, current) => 
    current.totalCommits > top.totalCommits ? current : top
  );
  
  const topTeamByEfficiency = teams.reduce((top, current) => 
    current.avgEntropy > top.avgEntropy ? current : top
  );
  
  const topTeamByImpact = teams.reduce((top, current) => 
    current.avgImpact > top.avgImpact ? current : top
  );

  // Overall top performer
  const globalTopPerformer = data.reduce((top, current) => 
    (current.imp_z || 0) > (top.imp_z || 0) ? current : top
  );

  // Data for charts
  const teamCommitsData = teams.map(team => ({
    name: team.name,
    commits: team.totalCommits,
    avgCommits: team.avgCommitsPerMember
  }));

  const teamEfficiencyData = teams.map(team => ({
    name: team.name,
    efficiency: team.avgEntropy,
    impact: team.avgImpact
  }));

  const pieData = teams.map(team => ({
    name: team.name,
    value: team.members.length,
    commits: team.totalCommits
  }));

  const COLORS = ['#16a34a', '#22c55e', '#4ade80', '#86efac', '#bbf7d0'];

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-black mb-2">Team Analytics</h1>
        <p className="text-gray-600">Comprehensive analysis of team performance and efficiency</p>
      </div>

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <Trophy className="text-green-600" size={24} />
            <h3 className="font-semibold text-black">Top Performer</h3>
          </div>
          <p className="text-2xl font-bold text-black">{globalTopPerformer.name}</p>
          <p className="text-sm text-gray-600">Team: {globalTopPerformer.team}</p>
          <p className="text-xs text-green-600 mt-1">Impact Score: {(globalTopPerformer.imp_z || 0).toFixed(2)}</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <Target className="text-green-600" size={24} />
            <h3 className="font-semibold text-black">Most Productive</h3>
          </div>
          <p className="text-2xl font-bold text-black">{topTeamByCommits.name}</p>
          <p className="text-sm text-gray-600">{topTeamByCommits.totalCommits} total commits</p>
          <p className="text-xs text-green-600 mt-1">{topTeamByCommits.avgCommitsPerMember.toFixed(1)} avg per member</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <Activity className="text-green-600" size={24} />
            <h3 className="font-semibold text-black">Most Efficient</h3>
          </div>
          <p className="text-2xl font-bold text-black">{topTeamByEfficiency.name}</p>
          <p className="text-sm text-gray-600">Complexity: {topTeamByEfficiency.avgEntropy.toFixed(2)}</p>
          <p className="text-xs text-green-600 mt-1">Highest code complexity</p>
        </div>

        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <div className="flex items-center gap-3 mb-3">
            <Award className="text-green-600" size={24} />
            <h3 className="font-semibold text-black">Highest Impact</h3>
          </div>
          <p className="text-2xl font-bold text-black">{topTeamByImpact.name}</p>
          <p className="text-sm text-gray-600">Impact: {topTeamByImpact.avgImpact.toFixed(2)}</p>
          <p className="text-xs text-green-600 mt-1">Team average impact score</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Team Commits Chart */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-xl font-semibold text-black mb-4 flex items-center gap-2">
            <BarChart className="text-green-600" size={20} />
            Team Productivity
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teamCommitsData}>
                <XAxis dataKey="name" tick={{ fill: '#6b7280', fontSize: 12 }} />
                <YAxis tick={{ fill: '#6b7280', fontSize: 12 }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #d1d5db', 
                    borderRadius: '8px',
                    fontSize: '12px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                  formatter={(value, name) => [value, name === 'commits' ? 'Total Commits' : name]}
                />
                <Bar dataKey="commits" fill="#16a34a" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Team Distribution */}
        <div className="bg-white p-6 rounded-xl border border-gray-200 shadow-sm">
          <h3 className="text-xl font-semibold text-black mb-4 flex items-center gap-2">
            <Users className="text-green-600" size={20} />
            Team Distribution
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, value }) => `${name}: ${value}`}
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #d1d5db', 
                    borderRadius: '8px',
                    fontSize: '12px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }}
                  formatter={(value, name) => [value, name === 'value' ? 'Team Members' : name]}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Team Details */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-xl font-semibold text-black flex items-center gap-2">
            <TrendingUp className="text-green-600" size={20} />
            Team Performance Details
          </h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {teams.map((team, index) => (
              <div key={team.name} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-semibold text-black">{team.name} Team</h4>
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                    {team.members.length} members
                  </span>
                </div>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Commits:</span>
                    <span className="font-medium text-black">{team.totalCommits}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg Complexity:</span>
                    <span className="font-medium text-black">{team.avgEntropy.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg Impact:</span>
                    <span className="font-medium text-black">{team.avgImpact.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Top Performer:</span>
                    <span className="font-medium text-green-600">{team.topPerformer.name}</span>
                  </div>
                </div>
                
                <div className="mt-3 pt-3 border-t border-gray-200">
                  <p className="text-xs text-gray-500">
                    Team Members: {team.members.map(m => m.name).join(', ')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeamAnalytics;