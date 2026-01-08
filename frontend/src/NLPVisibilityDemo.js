import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const NLPVisibilityDemo = () => {
  const [messages, setMessages] = useState([
    "Fixed critical security vulnerability in payment API - deployed hotfix to production",
    "Optimized database queries, reduced response time by 40%",
    "Code review: Great refactoring work on the auth service @jordan",
    "Created comprehensive API documentation for the new microservices",
    "Mentoring new team member on best practices for error handling"
  ]);
  
  const [developerName, setDeveloperName] = useState("Alex Smith");
  const [meetingHours, setMeetingHours] = useState(12.0);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyzeMessages = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze-visibility', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: messages.filter(msg => msg.trim() !== ''),
          developer_name: developerName,
          meeting_hours: meetingHours
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setAnalysis(result.analysis);
    } catch (err) {
      setError(`Analysis failed: ${err.message}`);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const addMessage = () => {
    setMessages([...messages, ""]);
  };

  const updateMessage = (index, value) => {
    const newMessages = [...messages];
    newMessages[index] = value;
    setMessages(newMessages);
  };

  const removeMessage = (index) => {
    const newMessages = messages.filter((_, i) => i !== index);
    setMessages(newMessages);
  };

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-blue-600';
    if (score >= 4) return 'text-yellow-600';
    if (score >= 2) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreLabel = (score) => {
    if (score >= 8) return 'Exceptional';
    if (score >= 6) return 'High';
    if (score >= 4) return 'Moderate';
    if (score >= 2) return 'Low';
    return 'Minimal';
  };

  // Prepare data for charts
  const componentData = analysis ? Object.entries(analysis.component_scores).map(([key, value]) => ({
    name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    score: value,
    fullName: key
  })) : [];

  const radarData = componentData.map(item => ({
    component: item.name.length > 12 ? item.name.substring(0, 12) + '...' : item.name,
    score: item.score,
    fullName: item.name
  }));

  return (
    <div className="max-w-6xl mx-auto p-6 bg-white">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🤖 DevLens NLP Visibility Scorer
        </h1>
        <p className="text-gray-600">
          Advanced AI/NLP engine that analyzes message content to calculate visibility scores based on technical impact, leadership, collaboration, and knowledge sharing.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Developer Name
            </label>
            <input
              type="text"
              value={developerName}
              onChange={(e) => setDeveloperName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter developer name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Meeting Hours per Week
            </label>
            <input
              type="number"
              value={meetingHours}
              onChange={(e) => setMeetingHours(parseFloat(e.target.value) || 0.0)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Hours spent in meetings"
              min="0"
              max="40"
              step="0.5"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Messages to Analyze
            </label>
            <div className="space-y-2">
              {messages.map((message, index) => (
                <div key={index} className="flex gap-2">
                  <textarea
                    value={message}
                    onChange={(e) => updateMessage(index, e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows="2"
                    placeholder={`Message ${index + 1}...`}
                  />
                  <button
                    onClick={() => removeMessage(index)}
                    className="px-3 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
                    disabled={messages.length <= 1}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
            
            <div className="flex gap-2 mt-3">
              <button
                onClick={addMessage}
                className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                + Add Message
              </button>
              
              <button
                onClick={analyzeMessages}
                disabled={loading || messages.every(msg => msg.trim() === '')}
                className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? '🔄 Analyzing...' : '🚀 Analyze with NLP'}
              </button>
            </div>
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-600">❌ {error}</p>
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {analysis && (
            <>
              {/* Overall Score */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-6 rounded-lg border">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  🎯 Visibility Analysis Results
                </h3>
                
                <div className="text-center mb-4">
                  <div className={`text-4xl font-bold ${getScoreColor(analysis.visibility_score)}`}>
                    {analysis.visibility_score}/10
                  </div>
                  <div className="text-lg text-gray-600 mt-1">
                    {getScoreLabel(analysis.visibility_score)} Visibility
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Messages:</span>
                    <span className="font-medium ml-2">{analysis.message_count}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Meeting Hours:</span>
                    <span className="font-medium ml-2">{analysis.meeting_hours}h</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Quality:</span>
                    <span className="font-medium ml-2">{analysis.quality_multiplier}x</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Sentiment:</span>
                    <span className="font-medium ml-2">{analysis.sentiment_multiplier}x</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Frequency:</span>
                    <span className="font-medium ml-2">{analysis.frequency_factor}x</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Meeting Score:</span>
                    <span className="font-medium ml-2">{analysis.meeting_engagement}/100</span>
                  </div>
                </div>

                <div className="mt-4 p-3 bg-white rounded border">
                  <p className="text-sm text-gray-700">
                    <strong>Summary:</strong> {analysis.analysis_summary}
                  </p>
                </div>
              </div>

              {/* Component Breakdown */}
              <div className="bg-white p-6 rounded-lg border">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  📊 Component Breakdown
                </h4>
                
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={componentData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={10}
                    />
                    <YAxis />
                    <Tooltip 
                      formatter={(value, name) => [value.toFixed(2), 'Score']}
                      labelFormatter={(label) => `Component: ${label}`}
                    />
                    <Bar dataKey="score" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Radar Chart */}
              <div className="bg-white p-6 rounded-lg border">
                <h4 className="text-lg font-semibold text-gray-900 mb-4">
                  🎯 Skills Radar
                </h4>
                
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="component" fontSize={10} />
                    <PolarRadiusAxis angle={90} domain={[0, 'dataMax']} fontSize={8} />
                    <Radar
                      name="Score"
                      dataKey="score"
                      stroke="#3B82F6"
                      fill="#3B82F6"
                      fillOpacity={0.3}
                    />
                    <Tooltip 
                      formatter={(value) => [value.toFixed(2), 'Score']}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </>
          )}

          {!analysis && !loading && (
            <div className="bg-gray-50 p-8 rounded-lg border-2 border-dashed border-gray-300 text-center">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Ready to Analyze
              </h3>
              <p className="text-gray-600">
                Enter some messages and click "Analyze with NLP" to see the AI-powered visibility scoring in action.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Info Section */}
      <div className="mt-8 bg-blue-50 p-6 rounded-lg border">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">
          🧠 How NLP Visibility Scoring Works
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Analysis Components:</h4>
            <ul className="space-y-1 text-gray-700">
              <li>• <strong>Technical Impact (20%)</strong> - Technical contributions</li>
              <li>• <strong>Leadership Influence (15%)</strong> - Decision making</li>
              <li>• <strong>Knowledge Sharing (15%)</strong> - Teaching & mentoring</li>
              <li>• <strong>Problem Solving (12%)</strong> - Helping others</li>
              <li>• <strong>Meeting Engagement (20%)</strong> - Meeting participation</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-2">AI Features:</h4>
            <ul className="space-y-1 text-gray-700">
              <li>• Semantic keyword analysis</li>
              <li>• Sentiment detection</li>
              <li>• Message quality assessment</li>
              <li>• Meeting participation scoring</li>
              <li>• Collaboration pattern recognition</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NLPVisibilityDemo;