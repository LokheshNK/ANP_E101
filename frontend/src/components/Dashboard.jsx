import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import './Dashboard.css';

const Dashboard = ({ data, loading, error, onPointSelect }) => {
  if (loading) {
    return <div className="loading">Loading DevLens data...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  const handlePointClick = (data) => {
    if (data && data.payload) {
      onPointSelect(data.payload);
    }
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="custom-tooltip">
          <p className="tooltip-label">{data.name || data.id}</p>
          {data.team && <p className="tooltip-team">Team: {data.team}</p>}
          <p className="tooltip-visibility">Visibility: {data.x.toFixed(2)}</p>
          <p className="tooltip-impact">Impact: {data.y.toFixed(2)}</p>
        </div>
      );
    }
    return null;
  };

  const getTeamHiddenGems = () => {
    // Group data by team and filter for hidden gems (Q2: x < 0, y >= 0)
    const teamGroups = {};
    data.forEach(member => {
      const team = member.team || 'Unknown';
      // Only include hidden gems (Low Visibility, High Impact)
      if (member.x < 0 && member.y >= 0) {
        if (!teamGroups[team]) {
          teamGroups[team] = [];
        }
        teamGroups[team].push({
          ...member,
          totalScore: member.x + member.y,
          impactScore: member.y // Use impact score for hidden gems ranking
        });
      }
    });

    // Get all teams and create entries for each
    const allTeams = [...new Set(data.map(member => member.team || 'Unknown'))];
    const teamHiddenGems = [];

    allTeams.forEach(team => {
      if (teamGroups[team] && teamGroups[team].length > 0) {
        // Team has hidden gems - show the top one
        const topHiddenGem = teamGroups[team].sort((a, b) => b.impactScore - a.impactScore)[0];
        teamHiddenGems.push({
          team,
          performer: topHiddenGem,
          hasHiddenGems: true
        });
      } else {
        // Team has no hidden gems - show placeholder
        teamHiddenGems.push({
          team,
          performer: null,
          hasHiddenGems: false
        });
      }
    });

    // Sort: teams with hidden gems first, then alphabetically
    return teamHiddenGems.sort((a, b) => {
      if (a.hasHiddenGems && !b.hasHiddenGems) return -1;
      if (!a.hasHiddenGems && b.hasHiddenGems) return 1;
      if (a.hasHiddenGems && b.hasHiddenGems) {
        return b.performer.impactScore - a.performer.impactScore;
      }
      return a.team.localeCompare(b.team);
    });
  };

  const getTopPerformers = () => {
    // Filter for hidden gems only (Q2: x < 0, y >= 0)
    return data
      .filter(item => item.x < 0 && item.y >= 0) // Only hidden gems
      .map(item => ({
        ...item,
        totalScore: item.x + item.y,
        impactScore: item.y // Use impact score for ranking hidden gems
      }))
      .sort((a, b) => b.impactScore - a.impactScore) // Sort by impact score
      .slice(0, 10); // Top 10 hidden gems
  };

  const getQuadrantColor = (x, y) => {
    if (x >= 0 && y >= 0) return "#22c55e";
    if (x < 0 && y >= 0) return "#16a34a";
    if (x < 0 && y < 0) return "#15803d";
    return "#166534";
  };

  const getQuadrantShort = (x, y) => {
    if (x >= 0 && y >= 0) return "Q1";
    if (x < 0 && y >= 0) return "Q2";
    if (x < 0 && y < 0) return "Q3";
    return "Q4";
  };

  const getQuadrantLabel = (x, y) => {
    if (x >= 0 && y >= 0) return "High Visibility, High Impact";
    if (x < 0 && y >= 0) return "Low Visibility, High Impact";
    if (x < 0 && y < 0) return "Low Visibility, Low Impact";
    return "High Visibility, Low Impact";
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>DevLens Dashboard</h1>
        <p className="dashboard-subtitle">Team Performance Quadrant Analysis</p>
      </div>

      <div className="dashboard-content">
        <div className="chart-section">
          <div className="chart-container">
            <ResponsiveContainer width="100%" height={600}>
              <ScatterChart
                margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
                data={data}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
                <XAxis 
                  type="number" 
                  dataKey="x" 
                  name="Visibility"
                  axisLine={{ stroke: '#000000' }}
                  tickLine={{ stroke: '#000000' }}
                  tick={{ fill: '#000000' }}
                />
                <YAxis 
                  type="number" 
                  dataKey="y" 
                  name="Impact"
                  axisLine={{ stroke: '#000000' }}
                  tickLine={{ stroke: '#000000' }}
                  tick={{ fill: '#000000' }}
                />
                <ReferenceLine x={0} stroke="#22c55e" strokeWidth={2} />
                <ReferenceLine y={0} stroke="#22c55e" strokeWidth={2} />
                <Tooltip content={<CustomTooltip />} />
                <Scatter 
                  name="Teams" 
                  data={data} 
                  fill="#22c55e"
                  onClick={handlePointClick}
                  cursor="pointer"
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="ranking-section">
          <h2>Top Hidden Gems</h2>
          <p className="ranking-subtitle">Low Visibility, High Impact performers ranked by impact score</p>
          <div className="ranking-list">
            {getTopPerformers().length > 0 ? (
              getTopPerformers().map((performer, index) => (
                <div key={performer.id} className="ranking-item hidden-gem-ranking" onClick={() => onPointSelect(performer)}>
                  <div className="rank-number">#{index + 1}</div>
                  <div className="performer-info">
                    <div className="performer-id">{performer.name || performer.id}</div>
                    {performer.team && <div className="performer-team">{performer.team}</div>}
                    <div className="performer-scores">
                      <span className="score-item">V: {performer.x.toFixed(2)}</span>
                      <span className="score-item impact-highlight">I: {performer.y.toFixed(2)}</span>
                      <span className="total-score">Total: {performer.totalScore.toFixed(2)}</span>
                    </div>
                  </div>
                  <div className="quadrant-badge" style={{ backgroundColor: getQuadrantColor(performer.x, performer.y) }}>
                    {getQuadrantShort(performer.x, performer.y)}
                  </div>
                  <div className="hidden-gem-indicator">💎</div>
                </div>
              ))
            ) : (
              <div className="no-hidden-gems-message">
                <div className="no-gems-icon">🔍</div>
                <div className="no-gems-text">
                  <h3>No Hidden Gems Found</h3>
                  <p>Currently no team members are in the Hidden Gem quadrant (Low Visibility, High Impact)</p>
                </div>
              </div>
            )}
          </div>

          <div className="quadrant-legend">
            <h3>Quadrant Legend</h3>
            <div className="legend-items">
              <div className="legend-item">
                <div className="legend-color high-high"></div>
                <span>High Visibility, High Impact</span>
              </div>
              <div className="legend-item">
                <div className="legend-color low-high"></div>
                <span>Low Visibility, High Impact</span>
              </div>
              <div className="legend-item">
                <div className="legend-color low-low"></div>
                <span>Low Visibility, Low Impact</span>
              </div>
              <div className="legend-item">
                <div className="legend-color high-low"></div>
                <span>High Visibility, Low Impact</span>
              </div>
            </div>
          </div>
        </div>
      </div>


      <div className="team-performers-section">
        <h2>Top Hidden Gems by Team</h2>
        <p className="section-subtitle">Low Visibility, High Impact performers (Q2 quadrant)</p>
        <div className="team-performers-grid">
          {getTeamHiddenGems().map((teamData, index) => (
            <div key={teamData.team} className={`team-performer-card ${teamData.hasHiddenGems ? 'hidden-gem-card' : 'no-gem-card'}`} onClick={teamData.performer ? () => onPointSelect(teamData.performer) : undefined}>
              <div className="team-performer-header">
                <h4>{teamData.team}</h4>
                <div className="performer-type-badge">
                  {teamData.hasHiddenGems ? (
                    <span className="hidden-gem-badge">💎 Hidden Gem</span>
                  ) : (
                    <span className="no-gem-badge">No Hidden Gem</span>
                  )}
                </div>
                {teamData.performer && (
                  <div className="quadrant-badge" style={{ backgroundColor: getQuadrantColor(teamData.performer.x, teamData.performer.y) }}>
                    {getQuadrantShort(teamData.performer.x, teamData.performer.y)}
                  </div>
                )}
              </div>
              <div className="performer-details">
                {teamData.performer ? (
                  <>
                    <div className="performer-name">{teamData.performer.name || teamData.performer.id}</div>
                    <div className="performer-scores">
                      <span className="score-item">V: {teamData.performer.x.toFixed(2)}</span>
                      <span className="score-item">I: {teamData.performer.y.toFixed(2)}</span>
                      <span className="total-score">Total: {teamData.performer.totalScore.toFixed(2)}</span>
                    </div>
                    {teamData.hasHiddenGems && (
                      <div className="hidden-gem-note">
                        High impact with low visibility - potential for greater recognition
                      </div>
                    )}
                  </>
                ) : (
                  <div className="no-gem-message">
                    <div className="no-gem-icon">🔍</div>
                    <div className="no-gem-text">
                      This team currently has no members in the Hidden Gem quadrant (Low Visibility, High Impact)
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;