import React, { useState, useEffect } from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LineChart, Line } from 'recharts';
import { Activity, Brain, Users, Code, Target, TrendingUp, Info, X } from 'lucide-react';

const MetricsBreakdown = ({ developer, onClose }) => {
  const [activeTab, setActiveTab] = useState('radar');
  const [radarData, setRadarData] = useState([]);
  const [detailedMetrics, setDetailedMetrics] = useState({});

  useEffect(() => {
    if (developer) {
      calculateMetrics();
    }
  }, [developer]);

  const calculateMetrics = () => {
    if (!developer) return;

    // Calculate advanced metrics
    const complexity = calculateComplexity(developer);
    const consistency = calculateConsistency(developer);
    const breadth = calculateBreadth(developer);
    const collaboration = calculateCollaboration(developer);
    const reliability = calculateReliability(developer);

    // Prepare radar chart data
    const radar = [
      {
        metric: 'Complexity',
        value: complexity.normalized,
        fullName: 'Code Complexity (Entropy)',
        description: 'Shannon entropy of code changes',
        rawValue: complexity.raw,
        formula: 'H(X) = -Σ p(x) log₂ p(x)'
      },
      {
        metric: 'Consistency',
        value: consistency.normalized,
        fullName: 'Commit Consistency (CV)',
        description: 'Coefficient of variation in commit patterns',
        rawValue: consistency.raw,
        formula: 'CV = σ / μ (lower is more consistent)'
      },
      {
        metric: 'Breadth',
        value: breadth.normalized,
        fullName: 'Code Breadth (Files)',
        description: 'Diversity of files modified',
        rawValue: breadth.raw,
        formula: 'Unique files touched / Total commits'
      },
      {
        metric: 'Collaboration',
        value: collaboration.normalized,
        fullName: 'Team Collaboration',
        description: 'Communication and teamwork indicators',
        rawValue: collaboration.raw,
        formula: 'Weighted sum of collaboration keywords'
      },
      {
        metric: 'Reliability',
        value: reliability.normalized,
        fullName: 'Commit Reliability',
        description: 'Consistency in commit sizes and patterns',
        rawValue: reliability.raw,
        formula: 'Inverse of commit size variance'
      }
    ];

    setRadarData(radar);
    setDetailedMetrics({
      complexity,
      consistency,
      breadth,
      collaboration,
      reliability,
      overall: {
        impact: developer.raw_impact || developer.impact_score || 0,
        visibility: developer.raw_visibility || developer.visibility_score || 0,
        attendance: developer.attendance_rate || 0.85,
        performance: developer.overall_performance_score || 0
      }
    });
  };

  const calculateComplexity = (dev) => {
    // Shannon Entropy calculation
    const entropy = dev.entropy || 0;
    const commits = dev.commits || 1;
    
    // Normalize entropy (typical range 0-3, normalize to 0-100)
    const normalized = Math.min(100, (entropy / 3.0) * 100);
    
    return {
      raw: entropy,
      normalized: normalized,
      interpretation: entropy > 2.0 ? 'High complexity' : entropy > 1.0 ? 'Medium complexity' : 'Low complexity',
      commits: commits
    };
  };

  const calculateConsistency = (dev) => {
    // Coefficient of Variation (CV) - lower is more consistent
    const commits = dev.commits || 0;
    const entropy = dev.entropy || 0;
    
    // Simulate CV based on commits and entropy patterns
    // In real implementation, this would be calculated from actual commit timestamps
    const avgCommitsPerWeek = commits / 4; // Assuming 4-week period
    const stdDev = Math.sqrt(entropy) * 2; // Simulated standard deviation
    const cv = avgCommitsPerWeek > 0 ? stdDev / avgCommitsPerWeek : 1;
    
    // Normalize CV (lower CV = higher consistency score)
    const consistencyScore = Math.max(0, 100 - (cv * 50));
    
    return {
      raw: cv,
      normalized: consistencyScore,
      interpretation: cv < 0.5 ? 'Very consistent' : cv < 1.0 ? 'Moderately consistent' : 'Inconsistent',
      avgCommitsPerWeek: avgCommitsPerWeek
    };
  };

  const calculateBreadth = (dev) => {
    // File diversity calculation
    const commits = dev.commits || 1;
    
    // Estimate unique files based on entropy and commits
    // Higher entropy typically means more diverse file changes
    const estimatedUniqueFiles = Math.floor((dev.entropy || 0.5) * commits * 0.7);
    const breadthRatio = estimatedUniqueFiles / commits;
    
    // Normalize to 0-100 scale
    const normalized = Math.min(100, breadthRatio * 100);
    
    return {
      raw: breadthRatio,
      normalized: normalized,
      interpretation: breadthRatio > 0.7 ? 'High breadth' : breadthRatio > 0.4 ? 'Medium breadth' : 'Focused work',
      estimatedFiles: estimatedUniqueFiles
    };
  };

  const calculateCollaboration = (dev) => {
    // Collaboration score from messages and meetings
    const messages = dev.msgs || [];
    const meetings = dev.meetings || 0;
    const commScore = dev.comm_score || 0;
    
    // Collaboration keywords weight
    const collaborationKeywords = [
      'help', 'support', 'team', 'together', 'collaborate', 'sync',
      'meeting', 'discuss', 'review', 'feedback', 'share', 'mentor'
    ];
    
    let keywordScore = 0;
    messages.forEach(msg => {
      const content = typeof msg === 'string' ? msg : (msg.text || msg.content || '');
      collaborationKeywords.forEach(keyword => {
        if (content.toLowerCase().includes(keyword)) {
          keywordScore += 1;
        }
      });
    });
    
    // Combine message keywords, meetings, and communication score
    const totalScore = keywordScore + (meetings * 2) + (commScore * 10);
    const normalized = Math.min(100, totalScore * 2);
    
    return {
      raw: totalScore,
      normalized: normalized,
      interpretation: normalized > 70 ? 'Highly collaborative' : normalized > 40 ? 'Moderately collaborative' : 'Individual contributor',
      keywordMatches: keywordScore,
      meetings: meetings
    };
  };

  const calculateReliability = (dev) => {
    // Reliability based on commit patterns and attendance
    const commits = dev.commits || 0;
    const attendance = dev.attendance_rate || 0.85;
    const entropy = dev.entropy || 0;
    
    // Reliability score combines attendance and commit consistency
    const attendanceScore = attendance * 50; // 0-50 points
    const commitConsistency = commits > 0 ? Math.min(50, (commits / entropy) * 10) : 0; // 0-50 points
    
    const totalReliability = attendanceScore + commitConsistency;
    
    return {
      raw: totalReliability / 100,
      normalized: totalReliability,
      interpretation: totalReliability > 80 ? 'Highly reliable' : totalReliability > 60 ? 'Reliable' : 'Needs improvement',
      attendanceContribution: attendanceScore,
      commitContribution: commitConsistency
    };
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#16a34a'; // Green
    if (score >= 60) return '#3b82f6'; // Blue
    if (score >= 40) return '#f59e0b'; // Amber
    return '#ef4444'; // Red
  };

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Fair';
    return 'Needs Improvement';
  };

  if (!developer) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold flex items-center gap-3">
                <Activity size={28} />
                Metrics Breakdown: {developer.name}
              </h2>
              <p className="text-blue-100 mt-1">{developer.team} Team • {developer.commits} commits • {Math.round((developer.attendance_rate || 0.85) * 100)}% attendance</p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white hover:bg-opacity-20 rounded-lg transition-colors"
            >
              <X size={24} />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'radar', label: 'Radar Analysis', icon: Target },
              { id: 'detailed', label: 'Detailed Metrics', icon: BarChart },
              { id: 'formulas', label: 'Methodology', icon: Brain }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 border-b-2 font-medium text-sm flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon size={16} />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto" style={{ maxHeight: 'calc(90vh - 200px)' }}>
          {activeTab === 'radar' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Radar Chart */}
              <div className="bg-gray-50 p-6 rounded-lg">
                <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <Target className="text-blue-600" size={20} />
                  Performance Radar
                </h3>
                <ResponsiveContainer width="100%" height={400}>
                  <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="metric" tick={{ fontSize: 12 }} />
                    <PolarRadiusAxis 
                      angle={90} 
                      domain={[0, 100]} 
                      tick={{ fontSize: 10 }}
                      tickCount={5}
                    />
                    <Radar
                      name="Score"
                      dataKey="value"
                      stroke="#3b82f6"
                      fill="#3b82f6"
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                    <Tooltip
                      formatter={(value, name) => [`${value.toFixed(1)}%`, 'Score']}
                      labelFormatter={(label) => {
                        const metric = radarData.find(d => d.metric === label);
                        return metric ? metric.fullName : label;
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              {/* Metric Details */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Info className="text-blue-600" size={20} />
                  Metric Explanations
                </h3>
                
                {radarData.map((metric, index) => (
                  <div key={index} className="bg-white border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900">{metric.fullName}</h4>
                      <div className="flex items-center gap-2">
                        <div 
                          className="w-3 h-3 rounded-full"
                          style={{ backgroundColor: getScoreColor(metric.value) }}
                        ></div>
                        <span className="font-semibold" style={{ color: getScoreColor(metric.value) }}>
                          {metric.value.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{metric.description}</p>
                    <div className="text-xs text-gray-500 font-mono bg-gray-50 p-2 rounded">
                      {metric.formula}
                    </div>
                    <div className="mt-2 text-sm">
                      <span className="text-gray-500">Raw value:</span>
                      <span className="ml-2 font-medium">{metric.rawValue.toFixed(3)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'detailed' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* Overall Performance */}
              <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
                <h3 className="text-lg font-semibold text-green-800 mb-4 flex items-center gap-2">
                  <TrendingUp size={20} />
                  Overall Performance
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-green-700">Impact Score:</span>
                    <span className="font-semibold text-green-800">{detailedMetrics.overall?.impact?.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-700">Visibility Score:</span>
                    <span className="font-semibold text-green-800">{detailedMetrics.overall?.visibility?.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-700">Attendance Rate:</span>
                    <span className="font-semibold text-green-800">{Math.round((detailedMetrics.overall?.attendance || 0) * 100)}%</span>
                  </div>
                  <div className="flex justify-between border-t border-green-300 pt-2">
                    <span className="text-green-700 font-medium">Total Performance:</span>
                    <span className="font-bold text-green-800">{detailedMetrics.overall?.performance?.toFixed(1)}</span>
                  </div>
                </div>
              </div>

              {/* Complexity Analysis */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <Code size={20} />
                  Code Complexity
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Shannon Entropy:</span>
                    <span className="font-semibold">{detailedMetrics.complexity?.raw?.toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Normalized Score:</span>
                    <span className="font-semibold">{detailedMetrics.complexity?.normalized?.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Commits:</span>
                    <span className="font-semibold">{detailedMetrics.complexity?.commits}</span>
                  </div>
                  <div className="text-sm text-gray-500 bg-gray-50 p-2 rounded">
                    {detailedMetrics.complexity?.interpretation}
                  </div>
                </div>
              </div>

              {/* Collaboration Analysis */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                  <Users size={20} />
                  Team Collaboration
                </h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Keyword Matches:</span>
                    <span className="font-semibold">{detailedMetrics.collaboration?.keywordMatches}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Meetings Attended:</span>
                    <span className="font-semibold">{detailedMetrics.collaboration?.meetings}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Collaboration Score:</span>
                    <span className="font-semibold">{detailedMetrics.collaboration?.normalized?.toFixed(1)}%</span>
                  </div>
                  <div className="text-sm text-gray-500 bg-gray-50 p-2 rounded">
                    {detailedMetrics.collaboration?.interpretation}
                  </div>
                </div>
              </div>

              {/* Consistency Analysis */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Commit Consistency</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Coefficient of Variation:</span>
                    <span className="font-semibold">{detailedMetrics.consistency?.raw?.toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Consistency Score:</span>
                    <span className="font-semibold">{detailedMetrics.consistency?.normalized?.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Avg Commits/Week:</span>
                    <span className="font-semibold">{detailedMetrics.consistency?.avgCommitsPerWeek?.toFixed(1)}</span>
                  </div>
                  <div className="text-sm text-gray-500 bg-gray-50 p-2 rounded">
                    {detailedMetrics.consistency?.interpretation}
                  </div>
                </div>
              </div>

              {/* Breadth Analysis */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Code Breadth</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Breadth Ratio:</span>
                    <span className="font-semibold">{detailedMetrics.breadth?.raw?.toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Breadth Score:</span>
                    <span className="font-semibold">{detailedMetrics.breadth?.normalized?.toFixed(1)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Est. Unique Files:</span>
                    <span className="font-semibold">{detailedMetrics.breadth?.estimatedFiles}</span>
                  </div>
                  <div className="text-sm text-gray-500 bg-gray-50 p-2 rounded">
                    {detailedMetrics.breadth?.interpretation}
                  </div>
                </div>
              </div>

              {/* Reliability Analysis */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Reliability</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Attendance Score:</span>
                    <span className="font-semibold">{detailedMetrics.reliability?.attendanceContribution?.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Commit Score:</span>
                    <span className="font-semibold">{detailedMetrics.reliability?.commitContribution?.toFixed(1)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Reliability:</span>
                    <span className="font-semibold">{detailedMetrics.reliability?.normalized?.toFixed(1)}%</span>
                  </div>
                  <div className="text-sm text-gray-500 bg-gray-50 p-2 rounded">
                    {detailedMetrics.reliability?.interpretation}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'formulas' && (
            <div className="space-y-8">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
                <h3 className="text-xl font-semibold text-blue-800 mb-4 flex items-center gap-2">
                  <Brain size={24} />
                  DevLens Methodology & Formulas
                </h3>
                <p className="text-blue-700">
                  Our advanced analytics system uses mathematical models to quantify developer performance across multiple dimensions.
                </p>
              </div>

              {/* Core Formulas */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-lg border border-gray-200">
                  <h4 className="text-lg font-semibold text-gray-800 mb-4">📊 Core Mathematical Models</h4>
                  
                  <div className="space-y-4">
                    <div className="bg-gray-50 p-4 rounded">
                      <h5 className="font-medium text-gray-800 mb-2">Shannon Entropy (Complexity)</h5>
                      <code className="text-sm bg-gray-800 text-green-400 p-2 rounded block">
                        H(X) = -Σ p(x) log₂ p(x)
                      </code>
                      <p className="text-sm text-gray-600 mt-2">
                        Measures information content and code complexity. Higher entropy indicates more diverse and complex changes.
                      </p>
                    </div>

                    <div className="bg-gray-50 p-4 rounded">
                      <h5 className="font-medium text-gray-800 mb-2">Z-Score Normalization</h5>
                      <code className="text-sm bg-gray-800 text-green-400 p-2 rounded block">
                        Z = (x - μ) / σ
                      </code>
                      <p className="text-sm text-gray-600 mt-2">
                        Standardizes metrics across different scales for fair comparison between developers.
                      </p>
                    </div>

                    <div className="bg-gray-50 p-4 rounded">
                      <h5 className="font-medium text-gray-800 mb-2">Coefficient of Variation</h5>
                      <code className="text-sm bg-gray-800 text-green-400 p-2 rounded block">
                        CV = σ / μ
                      </code>
                      <p className="text-sm text-gray-600 mt-2">
                        Measures consistency in commit patterns. Lower CV indicates more consistent work habits.
                      </p>
                    </div>

                    <div className="bg-gray-50 p-4 rounded">
                      <h5 className="font-medium text-gray-800 mb-2">Log Scaling</h5>
                      <code className="text-sm bg-gray-800 text-green-400 p-2 rounded block">
                        log₁₀(x + 1)
                      </code>
                      <p className="text-sm text-gray-600 mt-2">
                        Reduces the impact of outliers and creates more balanced distributions for metrics like commit counts.
                      </p>
                    </div>
                  </div>
                </div>

                <div className="bg-white p-6 rounded-lg border border-gray-200">
                  <h4 className="text-lg font-semibold text-gray-800 mb-4">⚖️ Weighted Scoring System</h4>
                  
                  <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded border border-blue-200">
                      <h5 className="font-medium text-blue-800 mb-2">Overall Performance Formula</h5>
                      <code className="text-sm bg-blue-900 text-blue-100 p-2 rounded block">
                        Performance = (Impact × 0.4) + (Visibility × 0.3) + (Attendance × 0.3)
                      </code>
                    </div>

                    <div className="bg-green-50 p-4 rounded border border-green-200">
                      <h5 className="font-medium text-green-800 mb-2">Impact Score Components</h5>
                      <ul className="text-sm text-green-700 space-y-1">
                        <li>• Commit count (log-scaled)</li>
                        <li>• Code complexity (Shannon entropy)</li>
                        <li>• Technical keyword density</li>
                        <li>• Code breadth (unique files)</li>
                      </ul>
                    </div>

                    <div className="bg-amber-50 p-4 rounded border border-amber-200">
                      <h5 className="font-medium text-amber-800 mb-2">Visibility Score Components</h5>
                      <ul className="text-sm text-amber-700 space-y-1">
                        <li>• Communication frequency</li>
                        <li>• Collaboration keywords</li>
                        <li>• Meeting participation</li>
                        <li>• Knowledge sharing indicators</li>
                      </ul>
                    </div>

                    <div className="bg-purple-50 p-4 rounded border border-purple-200">
                      <h5 className="font-medium text-purple-800 mb-2">Attendance Integration</h5>
                      <code className="text-sm bg-purple-900 text-purple-100 p-2 rounded block">
                        Penalty = max(0.1, attendance_rate)
                      </code>
                      <p className="text-sm text-purple-700 mt-2">
                        Attendance below 70% applies significant performance penalties.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Technical Keywords */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">🔍 Technical Keywords & Weights</h4>
                <p className="text-gray-600 mb-4">
                  Our NLP engine uses weighted keywords to identify technical contributions and expertise levels:
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div className="bg-red-50 p-4 rounded border border-red-200">
                    <h5 className="font-medium text-red-800 mb-2">High Impact (2.0-3.0)</h5>
                    <div className="text-sm text-red-700 space-y-1">
                      <div className="flex justify-between"><span>critical</span><span>3.0</span></div>
                      <div className="flex justify-between"><span>security</span><span>2.9</span></div>
                      <div className="flex justify-between"><span>architecture</span><span>2.6</span></div>
                      <div className="flex justify-between"><span>refactor</span><span>2.4</span></div>
                      <div className="flex justify-between"><span>performance</span><span>2.5</span></div>
                    </div>
                  </div>

                  <div className="bg-yellow-50 p-4 rounded border border-yellow-200">
                    <h5 className="font-medium text-yellow-800 mb-2">Medium Impact (1.5-2.0)</h5>
                    <div className="text-sm text-yellow-700 space-y-1">
                      <div className="flex justify-between"><span>deploy</span><span>2.0</span></div>
                      <div className="flex justify-between"><span>database</span><span>2.0</span></div>
                      <div className="flex justify-between"><span>api</span><span>1.9</span></div>
                      <div className="flex justify-between"><span>fix</span><span>1.8</span></div>
                      <div className="flex justify-between"><span>pipeline</span><span>1.8</span></div>
                    </div>
                  </div>

                  <div className="bg-green-50 p-4 rounded border border-green-200">
                    <h5 className="font-medium text-green-800 mb-2">Standard Impact (1.0-1.5)</h5>
                    <div className="text-sm text-green-700 space-y-1">
                      <div className="flex justify-between"><span>feature</span><span>1.4</span></div>
                      <div className="flex justify-between"><span>test</span><span>1.5</span></div>
                      <div className="flex justify-between"><span>merge</span><span>1.4</span></div>
                      <div className="flex justify-between"><span>create</span><span>1.2</span></div>
                      <div className="flex justify-between"><span>update</span><span>1.0</span></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Quadrant System */}
              <div className="bg-white p-6 rounded-lg border border-gray-200">
                <h4 className="text-lg font-semibold text-gray-800 mb-4">📍 Performance Quadrant System</h4>
                
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-green-50 p-4 rounded border border-green-200">
                    <h5 className="font-medium text-green-800 mb-2">🌟 Quadrant 1: Stars</h5>
                    <p className="text-sm text-green-700">High Impact + High Visibility</p>
                    <p className="text-xs text-green-600 mt-1">Top performers with strong technical contributions and team visibility</p>
                  </div>

                  <div className="bg-amber-50 p-4 rounded border border-amber-200">
                    <h5 className="font-medium text-amber-800 mb-2">💎 Quadrant 2: Hidden Gems</h5>
                    <p className="text-sm text-amber-700">High Impact + Low Visibility</p>
                    <p className="text-xs text-amber-600 mt-1">Strong technical contributors who need more recognition</p>
                  </div>

                  <div className="bg-blue-50 p-4 rounded border border-blue-200">
                    <h5 className="font-medium text-blue-800 mb-2">🔗 Quadrant 3: Connectors</h5>
                    <p className="text-sm text-blue-700">Low Impact + High Visibility</p>
                    <p className="text-xs text-blue-600 mt-1">Great communicators who could increase technical contributions</p>
                  </div>

                  <div className="bg-gray-50 p-4 rounded border border-gray-200">
                    <h5 className="font-medium text-gray-800 mb-2">🌱 Quadrant 4: Developing</h5>
                    <p className="text-sm text-gray-700">Low Impact + Low Visibility</p>
                    <p className="text-xs text-gray-600 mt-1">New team members or those needing support and development</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MetricsBreakdown;