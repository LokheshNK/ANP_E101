import React, { useState, useEffect } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Cell } from 'recharts';
import { BarChart3, TrendingUp, Eye, EyeOff, Calendar, Users } from 'lucide-react';

const Dashboard = ({ data, onUserSelect, settings }) => {
  const [hiddenGems, setHiddenGems] = useState([]);
  const [showingHiddenGems, setShowingHiddenGems] = useState(true);

  // Filter Hidden Gems (Quadrant 2 - High Impact, Low Visibility)
  useEffect(() => {
    console.log('Dashboard data received:', data.length, 'developers');
    
    // Debug: Check what quadrant data looks like
    data.forEach(dev => {
      if (dev.quadrant === 2 || dev.is_hidden_gem) {
        console.log(`POTENTIAL HIDDEN GEM: ${dev.name} - quadrant=${dev.quadrant}, is_hidden_gem=${dev.is_hidden_gem}, impact=${dev.raw_impact}, visibility=${dev.raw_visibility}, attendance=${dev.attendance_rate}`);
      }
    });
    
    // Filter Hidden Gems - try multiple approaches
    let gems = data.filter(dev => dev.is_hidden_gem === true);
    console.log(`Found ${gems.length} hidden gems via is_hidden_gem flag`);
    
    // Fallback: if no hidden gems found via flag, use quadrant logic
    if (gems.length === 0) {
      console.log('No hidden gems found via is_hidden_gem flag, trying quadrant approach...');
      gems = data.filter(dev => dev.quadrant === 2);
      console.log(`Found ${gems.length} hidden gems via quadrant 2`);
    }
    
    // Fallback: if still no gems, use impact/visibility thresholds
    if (gems.length === 0) {
      console.log('No hidden gems found via quadrant, trying threshold approach...');
      const impacts = data.map(d => d.raw_impact || d.impact_score || 0);
      const visibilities = data.map(d => d.raw_visibility || d.visibility_score || 0);
      
      if (impacts.length > 0 && visibilities.length > 0) {
        const impactMedian = impacts.sort((a, b) => a - b)[Math.floor(impacts.length / 2)];
        const visibilityMedian = visibilities.sort((a, b) => a - b)[Math.floor(visibilities.length / 2)];
        
        console.log(`Thresholds: impact >= ${impactMedian}, visibility < ${visibilityMedian}`);
        
        gems = data.filter(dev => {
          const impact = dev.raw_impact || dev.impact_score || 0;
          const visibility = dev.raw_visibility || dev.visibility_score || 0;
          const attendance = dev.attendance_rate || 0.85;
          const qualifies = impact >= impactMedian && visibility < visibilityMedian && attendance >= 0.75;
          
          if (qualifies) {
            console.log(`THRESHOLD HIDDEN GEM: ${dev.name} - impact=${impact}, visibility=${visibility}, attendance=${attendance}`);
          }
          
          return qualifies;
        });
        
        console.log(`Found ${gems.length} hidden gems via threshold approach`);
      }
    }
    
    console.log(`Final hidden gems count: ${gems.length}`);
    if (gems.length > 0) {
      console.log('Hidden gems:', gems.map(g => g.name));
    }
    
    gems.sort((a, b) => (b.raw_impact || b.impact_score || 0) - (a.raw_impact || a.impact_score || 0));
    setHiddenGems(gems);
  }, [data]);

  // Sorting data by Impact Z-score for alternative view
  const leaderboard = [...data].sort((a, b) => b.imp_z - a.imp_z);

  // Calculate team attendance statistics
  const teamAttendanceStats = () => {
    if (!data || data.length === 0) return { avgAttendance: 0, totalMembers: 0 };
    
    const totalAttendance = data.reduce((sum, dev) => sum + (dev.attendance_rate || 0.85), 0);
    const avgAttendance = totalAttendance / data.length;
    
    return {
      avgAttendance: avgAttendance,
      totalMembers: data.length,
      highAttendance: data.filter(dev => (dev.attendance_rate || 0.85) > 0.9).length,
      lowAttendance: data.filter(dev => (dev.attendance_rate || 0.85) < 0.7).length
    };
  };

  const attendanceStats = teamAttendanceStats();

  const getColor = (node) => {
    // Color coding based on quadrants
    if (node.quadrant === 1) return '#16a34a'; // Stars - Green
    if (node.quadrant === 2) return '#f59e0b'; // Hidden Gems - Amber
    if (node.quadrant === 3) return '#3b82f6'; // Communicators - Blue
    return '#6b7280'; // Needs Support - Gray
  };

  const getQuadrantLabel = (quadrant) => {
    switch(quadrant) {
      case 1: return "Star";
      case 2: return "Hidden Gem";
      case 3: return "Connector";
      case 4: return "Developing";
      default: return "Unknown";
    }
  };

  const formatAttendancePercentage = (rate) => {
    return `${Math.round((rate || 0.85) * 100)}%`;
  };

  const getAttendanceColor = (rate) => {
    const percentage = (rate || 0.85) * 100;
    if (percentage >= 90) return 'text-green-600';
    if (percentage >= 80) return 'text-yellow-600';
    return 'text-red-600';
  };

  const animationClass = settings?.dashboard?.showAnimations ? 'transition-all duration-200' : '';

  const displayData = showingHiddenGems ? hiddenGems : leaderboard;
  const sectionTitle = showingHiddenGems ? "Hidden Gems" : "Performance Rankings";
  const sectionSubtitle = showingHiddenGems 
    ? "High-impact developers who deserve more recognition" 
    : "Overall performance rankings by impact score";

  return (
    <div className="flex gap-6 h-full">
      {/* Performance Matrix Visualization */}
      <div className={`flex-[3] bg-gray-50 p-6 rounded-xl border border-gray-200 shadow-sm ${animationClass}`}>
        <h2 className="text-xl font-semibold text-black mb-4 flex items-center gap-3">
          <BarChart3 className="text-green-600" size={20} /> 
          Performance Impact Matrix
        </h2>
        
        {/* Team Attendance Summary */}
        <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Calendar className="text-blue-600" size={16} />
              <span className="font-medium text-blue-800">Team Attendance:</span>
              <span className={`font-semibold ${getAttendanceColor(attendanceStats.avgAttendance)}`}>
                {formatAttendancePercentage(attendanceStats.avgAttendance)}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="text-blue-600" size={16} />
              <span className="text-blue-700">
                {attendanceStats.highAttendance} high (90%+) • {attendanceStats.lowAttendance} need attention (&lt;70%)
              </span>
            </div>
          </div>
          <div className="mt-2 text-xs text-blue-600">
            ⚠️ Rankings include attendance as 30% of overall performance score
          </div>
        </div>
        
        {/* Quadrant Legend */}
        <div className="mb-4 flex flex-wrap gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-green-600 rounded-full"></div>
            <span>Stars (High Impact, High Visibility)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
            <span>Hidden Gems (High Impact, Low Visibility)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span>Connectors (Low Impact, High Visibility)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
            <span>Developing (Low Impact, Low Visibility)</span>
          </div>
        </div>

        <div className="h-[400px] w-full">
          <ResponsiveContainer>
            <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 10 }}>
              <XAxis 
                type="number" 
                dataKey="vis_z" 
                name="Visibility" 
                stroke="#6b7280" 
                tick={{fill: '#6b7280'}} 
                label={{ value: 'Visibility Score', position: 'bottom', fill: '#6b7280', fontSize: 12 }} 
              />
              <YAxis 
                type="number" 
                dataKey="imp_z" 
                name="Impact" 
                stroke="#6b7280" 
                tick={{fill: '#6b7280'}} 
                label={{ value: 'Impact Score', angle: -90, position: 'left', fill: '#6b7280', fontSize: 12 }} 
              />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3', stroke: '#16a34a', strokeWidth: 1 }} 
                contentStyle={{ 
                  backgroundColor: 'white', 
                  border: '1px solid #d1d5db', 
                  borderRadius: '8px', 
                  color: 'black',
                  fontSize: '12px',
                  boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
                formatter={(value, name) => [value?.toFixed(2), name === 'vis_z' ? 'Visibility' : 'Impact']}
                labelFormatter={(label, payload) => {
                  if (payload && payload[0]) {
                    const dev = payload[0].payload;
                    return `${dev.name} (${getQuadrantLabel(dev.quadrant)}) - Attendance: ${formatAttendancePercentage(dev.attendance_rate)}`;
                  }
                  return label;
                }}
              />
              <ReferenceLine x={0} stroke="#d1d5db" strokeDasharray="2 2" />
              <ReferenceLine y={0} stroke="#d1d5db" strokeDasharray="2 2" />
              <Scatter data={data} onClick={(e) => onUserSelect(e.payload)}>
                {data.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={getColor(entry)} 
                    className="cursor-pointer hover:opacity-80" 
                    style={{ filter: 'none' }}
                  />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Hidden Gems / Performance Rankings */}
      <div className={`flex-1 bg-gray-50 rounded-xl border border-gray-200 overflow-hidden ${animationClass} max-w-sm`}>
        <div className="p-4 border-b border-gray-200 bg-white">
          <div className="flex items-center justify-between">
            <div className="min-w-0 flex-1">
              <h2 className="text-lg font-semibold text-black flex items-center gap-2">
                <TrendingUp className="text-green-600 flex-shrink-0" size={18} /> 
                <span className="truncate">{sectionTitle}</span>
              </h2>
              <p className="text-xs text-gray-600 mt-1 truncate">{sectionSubtitle}</p>
            </div>
            <button
              onClick={() => setShowingHiddenGems(!showingHiddenGems)}
              className="flex items-center gap-2 px-3 py-2 text-sm bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex-shrink-0 ml-2"
              title={showingHiddenGems ? "Show all rankings" : "Show hidden gems only"}
            >
              {showingHiddenGems ? <Eye size={14} /> : <EyeOff size={14} />}
              <span className="hidden sm:inline">{showingHiddenGems ? "All" : "Gems"}</span>
            </button>
          </div>
        </div>

        <div className="p-3 overflow-y-auto" style={{ maxHeight: 'calc(100vh - 300px)' }}>
          <div className="space-y-2">
            {displayData.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <div className="mb-2">
                  {showingHiddenGems ? "No hidden gems found" : "No data available"}
                </div>
                {showingHiddenGems && data.length > 0 && (
                  <div className="text-xs text-gray-400">
                    Try switching to "All" rankings to see performance data
                  </div>
                )}
              </div>
            ) : (
              displayData.map((user, index) => (
                <div 
                  key={user.name} 
                  onClick={() => onUserSelect(user)}
                  className={`group relative p-3 rounded-lg bg-white hover:bg-green-50 border border-gray-200 hover:border-green-300 cursor-pointer ${animationClass} transition-all duration-200`}
                >
                  {/* Rank Badge */}
                  <div className="absolute -top-2 -left-2 w-6 h-6 rounded-full bg-gradient-to-br from-green-500 to-green-600 text-white text-xs font-bold flex items-center justify-center shadow-sm">
                    {index + 1}
                  </div>
                  
                  {/* Hidden Gem Badge */}
                  {showingHiddenGems && (
                    <div className="absolute -top-2 -right-2">
                      <span className="px-2 py-1 text-xs bg-gradient-to-r from-amber-400 to-amber-500 text-white rounded-full font-medium shadow-sm">
                        💎 Gem
                      </span>
                    </div>
                  )}
                  
                  <div className="mt-2">
                    {/* Name and Team */}
                    <div className="mb-2">
                      <h4 className="font-semibold text-sm text-black truncate">{user.name}</h4>
                      <p className="text-xs text-gray-500">{user.team} Team</p>
                    </div>
                    
                    {/* Metrics Grid */}
                    <div className="grid grid-cols-2 gap-2 mb-2">
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <div className="text-xs text-gray-500">Impact</div>
                        <div className="font-semibold text-sm text-green-600">
                          {showingHiddenGems ? user.raw_impact?.toFixed(2) : user.overall_performance_score?.toFixed(1)}
                        </div>
                      </div>
                      <div className="text-center p-2 bg-gray-50 rounded">
                        <div className="text-xs text-gray-500">Attendance</div>
                        <div className={`font-semibold text-sm ${getAttendanceColor(user.attendance_rate)}`}>
                          {formatAttendancePercentage(user.attendance_rate)}
                        </div>
                      </div>
                    </div>
                    
                    {/* Additional Info */}
                    <div className="flex items-center justify-between text-xs text-gray-400">
                      <span>{user.commits} commits</span>
                      {showingHiddenGems && (
                        <span>Vis: {user.raw_visibility?.toFixed(2)}</span>
                      )}
                    </div>
                    
                    {/* Days Present */}
                    {user.days_present && user.total_work_days && (
                      <div className="mt-1 text-xs text-gray-400 text-center">
                        {user.days_present}/{user.total_work_days} days present
                      </div>
                    )}
                  </div>
                  
                  {/* Hover Indicator */}
                  <div className="absolute bottom-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  </div>
                </div>
              ))
            )}
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;