import React, { useState } from 'react';
import { Brain, Calculator, BarChart3, Target, Code, Users, TrendingUp, Info, ChevronDown, ChevronRight } from 'lucide-react';

const Methodology = () => {
  const [expandedSections, setExpandedSections] = useState({
    formulas: true,
    keywords: false,
    quadrants: false,
    nlp: false
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const techWeights = {
    "critical": 3.0, "urgent": 2.8, "blocker": 3.0, "security": 2.9,
    "performance": 2.5, "optimization": 2.3, "refactor": 2.4, "architecture": 2.6,
    "bug": 2.0, "fix": 1.8, "patch": 1.9, "hotfix": 2.2,
    "deploy": 2.1, "release": 2.0, "production": 2.3, "staging": 1.7,
    "api": 1.9, "database": 2.0, "migration": 2.2, "schema": 2.1,
    "test": 1.5, "testing": 1.5, "qa": 1.6, "automation": 1.8,
    "ci": 1.7, "cd": 1.7, "pipeline": 1.8, "build": 1.6,
    "feature": 1.4, "enhancement": 1.5, "improvement": 1.6,
    "review": 1.3, "merge": 1.4, "pr": 1.5, "pull request": 1.5
  };

  const ExpandableSection = ({ title, icon: Icon, isExpanded, onToggle, children }) => (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm">
      <button
        onClick={onToggle}
        className="w-full p-6 text-left flex items-center justify-between hover:bg-gray-50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <Icon className="text-blue-600" size={24} />
          <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
        </div>
        {isExpanded ? <ChevronDown size={20} /> : <ChevronRight size={20} />}
      </button>
      {isExpanded && (
        <div className="px-6 pb-6 border-t border-gray-100">
          {children}
        </div>
      )}
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-8 rounded-xl">
        <div className="flex items-center gap-4 mb-4">
          <Brain size={40} />
          <div>
            <h1 className="text-3xl font-bold">DevLens Methodology</h1>
            <p className="text-blue-100 text-lg">Mathematical Models & Algorithms Behind Developer Analytics</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="bg-white bg-opacity-10 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Calculator size={20} />
              <span className="font-semibold">Advanced Mathematics</span>
            </div>
            <p className="text-sm text-blue-100">Shannon entropy, Z-scores, statistical modeling</p>
          </div>
          <div className="bg-white bg-opacity-10 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Target size={20} />
              <span className="font-semibold">Multi-Dimensional Analysis</span>
            </div>
            <p className="text-sm text-blue-100">5-axis radar charts, quadrant classification</p>
          </div>
          <div className="bg-white bg-opacity-10 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Brain size={20} />
              <span className="font-semibold">NLP & AI</span>
            </div>
            <p className="text-sm text-blue-100">Semantic analysis, sentiment detection</p>
          </div>
        </div>
      </div>

      {/* Core Mathematical Formulas */}
      <ExpandableSection
        title="Core Mathematical Formulas"
        icon={Calculator}
        isExpanded={expandedSections.formulas}
        onToggle={() => toggleSection('formulas')}
      >
        <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="space-y-6">
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                <Code size={20} />
                Shannon Entropy (Code Complexity)
              </h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-lg mb-4">
                H(X) = -Σ p(x) log₂ p(x)
              </div>
              <div className="space-y-3 text-sm">
                <p><strong>Purpose:</strong> Measures information content and code complexity</p>
                <p><strong>Range:</strong> 0 (no diversity) to ~3+ (high complexity)</p>
                <p><strong>Interpretation:</strong> Higher entropy indicates more diverse and complex code changes</p>
                <div className="bg-blue-50 p-3 rounded border border-blue-200">
                  <p className="text-blue-800"><strong>Example:</strong> A developer who modifies many different file types and functions will have higher entropy than one who makes repetitive changes.</p>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Z-Score Normalization</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-lg mb-4">
                Z = (x - μ) / σ
              </div>
              <div className="space-y-3 text-sm">
                <p><strong>Purpose:</strong> Standardizes metrics across different scales</p>
                <p><strong>μ (mu):</strong> Population mean</p>
                <p><strong>σ (sigma):</strong> Population standard deviation</p>
                <p><strong>Result:</strong> Values centered around 0 with standard deviation of 1</p>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Coefficient of Variation</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-lg mb-4">
                CV = σ / μ
              </div>
              <div className="space-y-3 text-sm">
                <p><strong>Purpose:</strong> Measures relative variability (consistency)</p>
                <p><strong>Lower CV:</strong> More consistent work patterns</p>
                <p><strong>Higher CV:</strong> More irregular work patterns</p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg border border-green-200">
              <h3 className="text-lg font-semibold text-green-800 mb-4 flex items-center gap-2">
                <TrendingUp size={20} />
                Overall Performance Formula
              </h3>
              <div className="bg-green-900 text-green-100 p-4 rounded font-mono text-sm mb-4">
                Performance = (Impact × 0.4) + (Visibility × 0.3) + (Attendance × 0.3)
              </div>
              <div className="space-y-3 text-sm text-green-800">
                <div className="flex justify-between items-center">
                  <span>Technical Impact:</span>
                  <span className="font-semibold">40% weight</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Team Visibility:</span>
                  <span className="font-semibold">30% weight</span>
                </div>
                <div className="flex justify-between items-center">
                  <span>Attendance Rate:</span>
                  <span className="font-semibold">30% weight</span>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Log Scaling</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-lg mb-4">
                log₁₀(x + 1)
              </div>
              <div className="space-y-3 text-sm">
                <p><strong>Purpose:</strong> Reduces impact of outliers</p>
                <p><strong>Application:</strong> Commit counts, message frequencies</p>
                <p><strong>Benefit:</strong> Creates more balanced distributions</p>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Attendance Penalty</h3>
              <div className="bg-gray-900 text-green-400 p-4 rounded font-mono text-lg mb-4">
                Penalty = max(0.1, attendance_rate)
              </div>
              <div className="space-y-2 text-sm">
                <p>• &lt;70% attendance: 50% performance penalty</p>
                <p>• &lt;80% attendance: 30% performance penalty</p>
                <p>• &lt;90% attendance: 15% performance penalty</p>
                <p>• ≥90% attendance: No penalty</p>
              </div>
            </div>
          </div>
        </div>
      </ExpandableSection>

      {/* Technical Keywords Dictionary */}
      <ExpandableSection
        title="Technical Keywords & Weights Dictionary"
        icon={Code}
        isExpanded={expandedSections.keywords}
        onToggle={() => toggleSection('keywords')}
      >
        <div className="mt-6">
          <p className="text-gray-600 mb-6">
            Our NLP engine uses a comprehensive dictionary of technical keywords with weighted importance scores. 
            These weights are based on the complexity and impact typically associated with each term.
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Critical & High Impact */}
            <div className="bg-red-50 p-6 rounded-lg border border-red-200">
              <h4 className="text-lg font-semibold text-red-800 mb-4 flex items-center gap-2">
                🚨 Critical Impact (2.5-3.0)
              </h4>
              <div className="space-y-2 text-sm">
                {Object.entries(techWeights)
                  .filter(([_, weight]) => weight >= 2.5)
                  .sort(([_, a], [__, b]) => b - a)
                  .map(([keyword, weight]) => (
                    <div key={keyword} className="flex justify-between items-center">
                      <span className="text-red-700 font-medium">{keyword}</span>
                      <span className="bg-red-200 text-red-800 px-2 py-1 rounded text-xs font-semibold">
                        {weight.toFixed(1)}
                      </span>
                    </div>
                  ))}
              </div>
            </div>

            {/* High Impact */}
            <div className="bg-orange-50 p-6 rounded-lg border border-orange-200">
              <h4 className="text-lg font-semibold text-orange-800 mb-4 flex items-center gap-2">
                ⚡ High Impact (2.0-2.4)
              </h4>
              <div className="space-y-2 text-sm">
                {Object.entries(techWeights)
                  .filter(([_, weight]) => weight >= 2.0 && weight < 2.5)
                  .sort(([_, a], [__, b]) => b - a)
                  .map(([keyword, weight]) => (
                    <div key={keyword} className="flex justify-between items-center">
                      <span className="text-orange-700 font-medium">{keyword}</span>
                      <span className="bg-orange-200 text-orange-800 px-2 py-1 rounded text-xs font-semibold">
                        {weight.toFixed(1)}
                      </span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Medium Impact */}
            <div className="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
              <h4 className="text-lg font-semibold text-yellow-800 mb-4 flex items-center gap-2">
                🔧 Medium Impact (1.5-1.9)
              </h4>
              <div className="space-y-2 text-sm">
                {Object.entries(techWeights)
                  .filter(([_, weight]) => weight >= 1.5 && weight < 2.0)
                  .sort(([_, a], [__, b]) => b - a)
                  .map(([keyword, weight]) => (
                    <div key={keyword} className="flex justify-between items-center">
                      <span className="text-yellow-700 font-medium">{keyword}</span>
                      <span className="bg-yellow-200 text-yellow-800 px-2 py-1 rounded text-xs font-semibold">
                        {weight.toFixed(1)}
                      </span>
                    </div>
                  ))}
              </div>
            </div>

            {/* Standard Impact */}
            <div className="bg-green-50 p-6 rounded-lg border border-green-200 md:col-span-2 lg:col-span-3">
              <h4 className="text-lg font-semibold text-green-800 mb-4 flex items-center gap-2">
                📝 Standard Impact (1.0-1.4)
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {Object.entries(techWeights)
                  .filter(([_, weight]) => weight >= 1.0 && weight < 1.5)
                  .sort(([_, a], [__, b]) => b - a)
                  .map(([keyword, weight]) => (
                    <div key={keyword} className="flex justify-between items-center bg-white p-2 rounded border border-green-200">
                      <span className="text-green-700 font-medium text-sm">{keyword}</span>
                      <span className="bg-green-200 text-green-800 px-2 py-1 rounded text-xs font-semibold">
                        {weight.toFixed(1)}
                      </span>
                    </div>
                  ))}
              </div>
            </div>
          </div>

          <div className="mt-6 bg-blue-50 p-4 rounded-lg border border-blue-200">
            <h5 className="font-semibold text-blue-800 mb-2">Keyword Scoring Logic</h5>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Keywords are matched using word boundaries to avoid false positives</li>
              <li>• Multiple keyword matches in a single message are cumulative</li>
              <li>• Code blocks (```) and links (http/github) receive additional bonuses</li>
              <li>• Case-insensitive matching with regex pattern recognition</li>
              <li>• Weights are calibrated based on typical impact and complexity</li>
            </ul>
          </div>
        </div>
      </ExpandableSection>

      {/* Performance Quadrant System */}
      <ExpandableSection
        title="Performance Quadrant Classification"
        icon={Target}
        isExpanded={expandedSections.quadrants}
        onToggle={() => toggleSection('quadrants')}
      >
        <div className="mt-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Quadrant Visualization */}
            <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
              <h4 className="text-lg font-semibold text-gray-800 mb-4">Quadrant Matrix</h4>
              <div className="grid grid-cols-2 gap-2 aspect-square">
                <div className="bg-green-100 border-2 border-green-300 p-4 rounded-lg flex flex-col items-center justify-center text-center">
                  <div className="text-2xl mb-2">🌟</div>
                  <div className="font-semibold text-green-800">Q1: Stars</div>
                  <div className="text-xs text-green-600 mt-1">High Impact<br/>High Visibility</div>
                </div>
                <div className="bg-amber-100 border-2 border-amber-300 p-4 rounded-lg flex flex-col items-center justify-center text-center">
                  <div className="text-2xl mb-2">💎</div>
                  <div className="font-semibold text-amber-800">Q2: Hidden Gems</div>
                  <div className="text-xs text-amber-600 mt-1">High Impact<br/>Low Visibility</div>
                </div>
                <div className="bg-blue-100 border-2 border-blue-300 p-4 rounded-lg flex flex-col items-center justify-center text-center">
                  <div className="text-2xl mb-2">🔗</div>
                  <div className="font-semibold text-blue-800">Q3: Connectors</div>
                  <div className="text-xs text-blue-600 mt-1">Low Impact<br/>High Visibility</div>
                </div>
                <div className="bg-gray-100 border-2 border-gray-300 p-4 rounded-lg flex flex-col items-center justify-center text-center">
                  <div className="text-2xl mb-2">🌱</div>
                  <div className="font-semibold text-gray-800">Q4: Developing</div>
                  <div className="text-xs text-gray-600 mt-1">Low Impact<br/>Low Visibility</div>
                </div>
              </div>
            </div>

            {/* Quadrant Details */}
            <div className="space-y-4">
              <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                <h5 className="font-semibold text-green-800 mb-2 flex items-center gap-2">
                  🌟 Quadrant 1: Stars (Top Performers)
                </h5>
                <p className="text-sm text-green-700 mb-2">High technical impact with strong team visibility</p>
                <ul className="text-xs text-green-600 space-y-1">
                  <li>• Above-median impact AND visibility scores</li>
                  <li>• Strong technical contributions with good communication</li>
                  <li>• Natural team leaders and mentors</li>
                  <li>• Should be considered for promotion/leadership roles</li>
                </ul>
              </div>

              <div className="bg-amber-50 p-4 rounded-lg border border-amber-200">
                <h5 className="font-semibold text-amber-800 mb-2 flex items-center gap-2">
                  💎 Quadrant 2: Hidden Gems (High Potential)
                </h5>
                <p className="text-sm text-amber-700 mb-2">Strong technical contributors who need more recognition</p>
                <ul className="text-xs text-amber-600 space-y-1">
                  <li>• Above-median impact, below-median visibility</li>
                  <li>• Excellent technical skills but quiet communication style</li>
                  <li>• May need encouragement to share knowledge more</li>
                  <li>• Prime candidates for mentoring and visibility programs</li>
                </ul>
              </div>

              <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                <h5 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
                  🔗 Quadrant 3: Connectors (Communication Focused)
                </h5>
                <p className="text-sm text-blue-700 mb-2">Great communicators who could increase technical output</p>
                <ul className="text-xs text-blue-600 space-y-1">
                  <li>• Below-median impact, above-median visibility</li>
                  <li>• Strong in meetings, communication, and collaboration</li>
                  <li>• May benefit from technical skill development</li>
                  <li>• Good candidates for project management or coordination roles</li>
                </ul>
              </div>

              <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <h5 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                  🌱 Quadrant 4: Developing (Growth Opportunity)
                </h5>
                <p className="text-sm text-gray-700 mb-2">Early career or developers needing support</p>
                <ul className="text-xs text-gray-600 space-y-1">
                  <li>• Below-median impact AND visibility scores</li>
                  <li>• May be new team members still learning</li>
                  <li>• Could benefit from mentoring and structured development</li>
                  <li>• Focus on both technical skills and communication</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="mt-6 bg-purple-50 p-4 rounded-lg border border-purple-200">
            <h5 className="font-semibold text-purple-800 mb-2">Classification Algorithm</h5>
            <div className="bg-purple-900 text-purple-100 p-3 rounded font-mono text-sm">
              if (impact_z &gt; 0 && visibility_z &gt; 0) → Quadrant 1 (Stars)<br/>
              if (impact_z &gt; 0 && visibility_z ≤ 0) → Quadrant 2 (Hidden Gems)<br/>
              if (impact_z ≤ 0 && visibility_z &gt; 0) → Quadrant 3 (Connectors)<br/>
              if (impact_z ≤ 0 && visibility_z ≤ 0) → Quadrant 4 (Developing)
            </div>
          </div>
        </div>
      </ExpandableSection>

      {/* NLP & AI Analysis */}
      <ExpandableSection
        title="NLP & AI Analysis Engine"
        icon={Brain}
        isExpanded={expandedSections.nlp}
        onToggle={() => toggleSection('nlp')}
      >
        <div className="mt-6 space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-6 rounded-lg border border-blue-200">
              <h4 className="text-lg font-semibold text-blue-800 mb-4 flex items-center gap-2">
                <Brain size={20} />
                NLP Component Analysis
              </h4>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Technical Impact:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">20%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Meeting Engagement:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">20%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Leadership Influence:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">15%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Knowledge Sharing:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">15%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Problem Solving:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">12%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Collaboration:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">10%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Urgency Priority:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">4%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-blue-700">Engagement:</span>
                  <span className="bg-blue-200 text-blue-800 px-2 py-1 rounded font-semibold">4%</span>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg border border-gray-200">
              <h4 className="text-lg font-semibold text-gray-800 mb-4">Advanced NLP Features</h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">•</span>
                  <span><strong>Semantic Analysis:</strong> Word boundary matching with context awareness</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">•</span>
                  <span><strong>Sentiment Detection:</strong> Positive/negative sentiment impact analysis</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">•</span>
                  <span><strong>Code Recognition:</strong> Automatic detection of code blocks and technical links</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">•</span>
                  <span><strong>Quality Assessment:</strong> Message length and structure analysis</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">•</span>
                  <span><strong>Collaboration Detection:</strong> @mentions and team interaction patterns</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 font-bold">•</span>
                  <span><strong>Meeting Participation:</strong> Automatic scoring based on meeting attendance patterns</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="bg-gray-50 p-6 rounded-lg border border-gray-200">
            <h4 className="text-lg font-semibold text-gray-800 mb-4">NLP Processing Pipeline</h4>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div className="bg-white p-4 rounded border border-gray-300 text-center">
                <div className="text-2xl mb-2">📝</div>
                <div className="font-medium text-sm">Input Processing</div>
                <div className="text-xs text-gray-600 mt-1">Normalize message formats</div>
              </div>
              <div className="bg-white p-4 rounded border border-gray-300 text-center">
                <div className="text-2xl mb-2">🧹</div>
                <div className="font-medium text-sm">Text Cleaning</div>
                <div className="text-xs text-gray-600 mt-1">Remove HTML, normalize case</div>
              </div>
              <div className="bg-white p-4 rounded border border-gray-300 text-center">
                <div className="text-2xl mb-2">🔍</div>
                <div className="font-medium text-sm">Feature Extraction</div>
                <div className="text-xs text-gray-600 mt-1">Identify keywords, patterns</div>
              </div>
              <div className="bg-white p-4 rounded border border-gray-300 text-center">
                <div className="text-2xl mb-2">⚖️</div>
                <div className="font-medium text-sm">Weighted Scoring</div>
                <div className="text-xs text-gray-600 mt-1">Apply component weights</div>
              </div>
              <div className="bg-white p-4 rounded border border-gray-300 text-center">
                <div className="text-2xl mb-2">📊</div>
                <div className="font-medium text-sm">Final Score</div>
                <div className="text-xs text-gray-600 mt-1">Normalize to 0-10 scale</div>
              </div>
            </div>
          </div>

          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <h5 className="font-semibold text-yellow-800 mb-2 flex items-center gap-2">
              <Info size={16} />
              Hybrid Scoring Approach
            </h5>
            <p className="text-sm text-yellow-700 mb-2">
              DevLens uses a hybrid approach combining advanced NLP analysis with traditional keyword-based scoring:
            </p>
            <div className="bg-yellow-900 text-yellow-100 p-3 rounded font-mono text-sm">
              Final_Score = (NLP_Analysis × 0.8) + (Legacy_Keywords × 0.2)
            </div>
            <p className="text-xs text-yellow-600 mt-2">
              This ensures stability while leveraging advanced AI capabilities for more nuanced analysis.
            </p>
          </div>
        </div>
      </ExpandableSection>

      {/* Footer */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-200 text-center">
        <p className="text-gray-600 text-sm">
          DevLens methodology is continuously refined based on research in software engineering metrics, 
          team dynamics, and developer productivity. All formulas and weights are calibrated using real-world data 
          and validated through statistical analysis.
        </p>
        <div className="mt-4 flex items-center justify-center gap-4 text-xs text-gray-500">
          <span>📊 Statistical Validation</span>
          <span>🔬 Research-Based</span>
          <span>⚡ Real-Time Processing</span>
          <span>🎯 Actionable Insights</span>
        </div>
      </div>
    </div>
  );
};

export default Methodology;