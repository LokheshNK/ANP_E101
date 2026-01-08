import React, { useState, useEffect } from 'react';
import { useApp } from '../context/AppContext';
import { 
  Settings as SettingsIcon, 
  Bell, 
  Shield, 
  Users, 
  Download,
  Upload,
  RefreshCw,
  Eye,
  AlertTriangle,
  CheckCircle,
  Save,
  Mail,
  X
} from 'lucide-react';

const Settings = () => {
  const { settings: globalSettings, updateSettings, user } = useApp();
  const [settings, setSettings] = useState(globalSettings || {});
  const [activeTab, setActiveTab] = useState('notifications');
  const [saveStatus, setSaveStatus] = useState('');
  const [showEmailModal, setShowEmailModal] = useState(false);
  const [emailAddress, setEmailAddress] = useState('');
  const [emailSettings, setEmailSettings] = useState({
    email_address: user?.email || '',
    email_alerts: true,
    performance_alerts: true,
    weekly_reports: false,
    team_updates: true,
    critical_issues: true
  });
  const [sendingEmail, setSendingEmail] = useState(false);

  useEffect(() => {
    if (globalSettings) {
      setSettings(globalSettings);
    }
    
    // Load email settings from backend
    if (user?.id) {
      loadEmailSettings();
    }
  }, [globalSettings, user]);

  const loadEmailSettings = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/settings/${user.id}`);
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          setEmailSettings({
            ...data.settings,
            email_address: data.settings.email_address || user.email
          });
          setEmailAddress(data.settings.email_address || user.email);
        }
      }
    } catch (error) {
      console.error('Error loading email settings:', error);
      // Use default with user's login email
      setEmailSettings(prev => ({
        ...prev,
        email_address: user.email
      }));
      setEmailAddress(user.email);
    }
  };

  const saveEmailSettings = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          manager_id: user.id,
          ...emailSettings
        }),
      });

      if (response.ok) {
        return true;
      }
    } catch (error) {
      console.error('Error saving email settings:', error);
    }
    return false;
  };

  const handleSettingChange = (category, setting, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [setting]: value
      }
    }));
  };

  const handleEmailAlertToggle = (value) => {
    if (value && !emailSettings.email_address) {
      setShowEmailModal(true);
    } else {
      setEmailSettings(prev => ({
        ...prev,
        email_alerts: value
      }));
    }
  };

  const handleEmailSave = () => {
    if (emailAddress.trim()) {
      setEmailSettings(prev => ({
        ...prev,
        email_address: emailAddress,
        email_alerts: true
      }));
      setShowEmailModal(false);
    }
  };

  const handleSave = async () => {
    setSaveStatus('saving');
    
    // Save regular settings
    updateSettings(settings);
    
    // Save email settings
    const emailSaved = await saveEmailSettings();
    
    setTimeout(() => {
      setSaveStatus(emailSaved ? 'saved' : 'error');
      setTimeout(() => setSaveStatus(''), 2000);
    }, 1000);
  };

  const sendTestEmail = async (emailType) => {
    setSendingEmail(true);
    
    try {
      // First, save the current email settings to ensure the updated email address is used
      console.log('Saving email settings before sending test email...');
      const saveResponse = await fetch('http://127.0.0.1:8000/api/settings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          manager_id: user.id,
          ...emailSettings
        }),
      });

      if (!saveResponse.ok) {
        throw new Error('Failed to save email settings');
      }

      console.log('Email settings saved successfully');

      // Now send the test email
      const response = await fetch('http://127.0.0.1:8000/api/send-email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email_type: emailType,
          manager_id: user.id
        }),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`✅ ${emailType === 'test' ? 'Test email' : emailType + ' email'} sent successfully to ${emailSettings.email_address}`);
      } else {
        const error = await response.json();
        alert(`❌ Failed to send email: ${error.detail}`);
      }
    } catch (error) {
      alert(`❌ Network error: ${error.message}`);
    }
    
    setSendingEmail(false);
  };

  const handleExportData = () => {
    const dataStr = JSON.stringify(settings, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = 'devlens-settings.json';
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
  };

  const handleImportData = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const importedSettings = JSON.parse(e.target.result);
          setSettings(importedSettings);
          setSaveStatus('imported');
          setTimeout(() => setSaveStatus(''), 2000);
        } catch (error) {
          alert('Invalid settings file');
        }
      };
      reader.readAsText(file);
    }
  };

  const handleClearData = () => {
    if (window.confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
      localStorage.clear();
      window.location.reload();
    }
  };

  const ToggleSwitch = ({ enabled, onChange, label, description }) => (
    <div className="flex items-center justify-between py-3">
      <div>
        <p className="font-medium text-black">{label}</p>
        {description && <p className="text-sm text-gray-600">{description}</p>}
      </div>
      <button
        onClick={() => onChange(!enabled)}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          enabled ? 'bg-green-600' : 'bg-gray-300'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            enabled ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </div>
  );

  const SelectField = ({ value, onChange, options, label, description }) => (
    <div className="py-3">
      <label className="block font-medium text-black mb-1">{label}</label>
      {description && <p className="text-sm text-gray-600 mb-2">{description}</p>}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
      >
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );

  const tabs = [
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'dashboard', label: 'Dashboard', icon: Eye },
    { id: 'analytics', label: 'Analytics', icon: SettingsIcon },
    { id: 'team', label: 'Team', icon: Users },
    { id: 'privacy', label: 'Privacy & Data', icon: Shield }
  ];

  return (
    <div className="p-8">
      {/* Email Modal */}
      {showEmailModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-96">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-black">Email Configuration</h3>
              <button
                onClick={() => setShowEmailModal(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                <X size={20} />
              </button>
            </div>
            <p className="text-sm text-gray-600 mb-4">
              Please enter your email address to receive notifications:
            </p>
            <input
              type="email"
              value={emailAddress}
              onChange={(e) => setEmailAddress(e.target.value)}
              placeholder="your.email@company.com"
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 mb-4"
            />
            <div className="flex gap-3">
              <button
                onClick={handleEmailSave}
                className="flex-1 bg-green-600 text-white p-2 rounded-lg hover:bg-green-700"
              >
                Save & Enable Alerts
              </button>
              <button
                onClick={() => setShowEmailModal(false)}
                className="flex-1 border border-gray-300 text-gray-700 p-2 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-black mb-2">Settings</h1>
        <p className="text-gray-600">Configure your DevLens experience and preferences</p>
      </div>

      <div className="flex gap-8">
        {/* Sidebar Navigation */}
        <div className="w-64 bg-white rounded-xl border border-gray-200 p-4">
          <nav className="space-y-2">
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center gap-3 p-3 rounded-lg text-left transition-all ${
                    activeTab === tab.id
                      ? 'bg-green-100 text-green-700 border border-green-200'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  <Icon size={18} />
                  <span className="font-medium">{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Settings Content */}
        <div className="flex-1 bg-white rounded-xl border border-gray-200">
          <div className="p-6 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-black">
                {tabs.find(tab => tab.id === activeTab)?.label} Settings
              </h2>
              <button
                onClick={handleSave}
                disabled={saveStatus === 'saving'}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
              >
                {saveStatus === 'saving' ? (
                  <RefreshCw size={16} className="animate-spin" />
                ) : saveStatus === 'saved' ? (
                  <CheckCircle size={16} />
                ) : saveStatus === 'imported' ? (
                  <CheckCircle size={16} />
                ) : (
                  <Save size={16} />
                )}
                {saveStatus === 'saving' ? 'Saving...' : 
                 saveStatus === 'saved' ? 'Saved!' : 
                 saveStatus === 'imported' ? 'Imported!' : 'Save Changes'}
              </button>
            </div>
          </div>

          <div className="p-6">
            {/* Notifications Tab */}
            {activeTab === 'notifications' && (
              <div className="space-y-4">
                {/* Email Address Configuration */}
                <div className="py-3 border-b border-gray-200">
                  <label className="block font-medium text-black mb-2">
                    <Mail size={16} className="inline mr-2" />
                    Email Address for Notifications
                  </label>
                  <div className="flex gap-3">
                    <input
                      type="email"
                      value={emailSettings.email_address}
                      onChange={(e) => setEmailSettings(prev => ({...prev, email_address: e.target.value}))}
                      placeholder="your.email@company.com"
                      className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
                    />
                    <button
                      onClick={() => sendTestEmail('test')}
                      disabled={sendingEmail || !emailSettings.email_address}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
                    >
                      {sendingEmail ? 'Sending...' : 'Test Email'}
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Default: Your login email ({user?.email}). You can change this to any email address.
                  </p>
                </div>

                <div className="flex items-center justify-between py-3">
                  <div>
                    <p className="font-medium text-black">Email Alerts</p>
                    <p className="text-sm text-gray-600">
                      Enable email notifications for important updates
                    </p>
                  </div>
                  <button
                    onClick={() => setEmailSettings(prev => ({...prev, email_alerts: !prev.email_alerts}))}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      emailSettings.email_alerts ? 'bg-green-600' : 'bg-gray-300'
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        emailSettings.email_alerts ? 'translate-x-6' : 'translate-x-1'
                      }`}
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between py-3">
                  <div className="flex-1">
                    <p className="font-medium text-black">Performance Alerts</p>
                    <p className="text-sm text-gray-600">Get notified when performance metrics change significantly</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => sendTestEmail('performance')}
                      disabled={sendingEmail || !emailSettings.performance_alerts}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 disabled:opacity-50"
                    >
                      Send Sample
                    </button>
                    <button
                      onClick={() => setEmailSettings(prev => ({...prev, performance_alerts: !prev.performance_alerts}))}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        emailSettings.performance_alerts ? 'bg-green-600' : 'bg-gray-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          emailSettings.performance_alerts ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between py-3">
                  <div className="flex-1">
                    <p className="font-medium text-black">Weekly Reports</p>
                    <p className="text-sm text-gray-600">Receive weekly team performance summaries</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => sendTestEmail('weekly')}
                      disabled={sendingEmail || !emailSettings.weekly_reports}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 disabled:opacity-50"
                    >
                      Send Sample
                    </button>
                    <button
                      onClick={() => setEmailSettings(prev => ({...prev, weekly_reports: !prev.weekly_reports}))}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        emailSettings.weekly_reports ? 'bg-green-600' : 'bg-gray-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          emailSettings.weekly_reports ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between py-3">
                  <div className="flex-1">
                    <p className="font-medium text-black">Team Updates</p>
                    <p className="text-sm text-gray-600">Notifications about team member changes and updates</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => sendTestEmail('team')}
                      disabled={sendingEmail || !emailSettings.team_updates}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 disabled:opacity-50"
                    >
                      Send Sample
                    </button>
                    <button
                      onClick={() => setEmailSettings(prev => ({...prev, team_updates: !prev.team_updates}))}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        emailSettings.team_updates ? 'bg-green-600' : 'bg-gray-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          emailSettings.team_updates ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between py-3">
                  <div className="flex-1">
                    <p className="font-medium text-black">Critical Issues</p>
                    <p className="text-sm text-gray-600">Immediate alerts for critical performance issues</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => sendTestEmail('critical')}
                      disabled={sendingEmail || !emailSettings.critical_issues}
                      className="px-3 py-1 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200 disabled:opacity-50"
                    >
                      Send Sample
                    </button>
                    <button
                      onClick={() => setEmailSettings(prev => ({...prev, critical_issues: !prev.critical_issues}))}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        emailSettings.critical_issues ? 'bg-green-600' : 'bg-gray-300'
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          emailSettings.critical_issues ? 'translate-x-6' : 'translate-x-1'
                        }`}
                      />
                    </button>
                  </div>
                </div>

                {/* Email Preview Section */}
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <h3 className="font-semibold text-black mb-4">📧 Email Notifications</h3>
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-sm text-gray-600 mb-3">
                      All notifications will be sent to: <strong>{emailSettings.email_address}</strong>
                    </p>
                    <div className="flex gap-2 flex-wrap">
                      <button
                        onClick={() => sendTestEmail('test')}
                        disabled={sendingEmail}
                        className="px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 text-sm"
                      >
                        Send Test Email
                      </button>
                      <button
                        onClick={() => sendTestEmail('performance')}
                        disabled={sendingEmail || !emailSettings.performance_alerts}
                        className="px-3 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 text-sm"
                      >
                        Performance Alert Sample
                      </button>
                      <button
                        onClick={() => sendTestEmail('weekly')}
                        disabled={sendingEmail || !emailSettings.weekly_reports}
                        className="px-3 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 disabled:opacity-50 text-sm"
                      >
                        Weekly Report Sample
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Dashboard Tab */}
            {activeTab === 'dashboard' && (
              <div className="space-y-4">
                <SelectField
                  value={settings.dashboard?.refreshInterval}
                  onChange={(value) => handleSettingChange('dashboard', 'refreshInterval', value)}
                  label="Auto Refresh Interval"
                  description="How often the dashboard should update automatically"
                  options={[
                    { value: '1', label: '1 minute' },
                    { value: '5', label: '5 minutes' },
                    { value: '10', label: '10 minutes' },
                    { value: '30', label: '30 minutes' },
                    { value: '0', label: 'Manual only' }
                  ]}
                />
                <SelectField
                  value={settings.dashboard?.defaultView}
                  onChange={(value) => handleSettingChange('dashboard', 'defaultView', value)}
                  label="Default View"
                  description="Which page to show when opening DevLens"
                  options={[
                    { value: 'dashboard', label: 'Dashboard' },
                    { value: 'team-analytics', label: 'Team Analytics' }
                  ]}
                />
                <ToggleSwitch
                  enabled={settings.dashboard?.showAnimations}
                  onChange={(value) => handleSettingChange('dashboard', 'showAnimations', value)}
                  label="Show Animations"
                  description="Enable smooth transitions and animations"
                />
                <ToggleSwitch
                  enabled={settings.dashboard?.compactMode}
                  onChange={(value) => handleSettingChange('dashboard', 'compactMode', value)}
                  label="Compact Mode"
                  description="Show more information in less space"
                />
              </div>
            )}

            {/* Analytics Tab */}
            {activeTab === 'analytics' && (
              <div className="space-y-4">
                <SelectField
                  value={settings.analytics?.trackingPeriod}
                  onChange={(value) => handleSettingChange('analytics', 'trackingPeriod', value)}
                  label="Tracking Period"
                  description="How far back to analyze performance data"
                  options={[
                    { value: '7', label: '7 days' },
                    { value: '30', label: '30 days' },
                    { value: '90', label: '90 days' },
                    { value: '365', label: '1 year' }
                  ]}
                />
                <SelectField
                  value={settings.analytics?.minCommitsThreshold}
                  onChange={(value) => handleSettingChange('analytics', 'minCommitsThreshold', value)}
                  label="Minimum Commits Threshold"
                  description="Minimum commits required to include in analytics"
                  options={[
                    { value: '1', label: '1 commit' },
                    { value: '5', label: '5 commits' },
                    { value: '10', label: '10 commits' },
                    { value: '20', label: '20 commits' }
                  ]}
                />
                <SelectField
                  value={settings.analytics?.impactCalculation}
                  onChange={(value) => handleSettingChange('analytics', 'impactCalculation', value)}
                  label="Impact Calculation Method"
                  description="How to calculate developer impact scores"
                  options={[
                    { value: 'weighted', label: 'Weighted Average' },
                    { value: 'simple', label: 'Simple Average' },
                    { value: 'median', label: 'Median Based' }
                  ]}
                />
                <ToggleSwitch
                  enabled={settings.analytics?.excludeWeekends}
                  onChange={(value) => handleSettingChange('analytics', 'excludeWeekends', value)}
                  label="Exclude Weekends"
                  description="Don't count weekend activity in performance metrics"
                />
                <ToggleSwitch
                  enabled={settings.analytics?.includeDocumentation}
                  onChange={(value) => handleSettingChange('analytics', 'includeDocumentation', value)}
                  label="Include Documentation"
                  description="Count documentation commits in performance analysis"
                />
              </div>
            )}

            {/* Team Tab */}
            {activeTab === 'team' && (
              <div className="space-y-4">
                <ToggleSwitch
                  enabled={settings.team?.autoAssignTeams}
                  onChange={(value) => handleSettingChange('team', 'autoAssignTeams', value)}
                  label="Auto-assign Teams"
                  description="Automatically assign new developers to teams based on their work"
                />
                <ToggleSwitch
                  enabled={settings.team?.allowTeamSwitching}
                  onChange={(value) => handleSettingChange('team', 'allowTeamSwitching', value)}
                  label="Allow Team Switching"
                  description="Let team members change their team assignment"
                />
                <ToggleSwitch
                  enabled={settings.team?.requireApproval}
                  onChange={(value) => handleSettingChange('team', 'requireApproval', value)}
                  label="Require Approval"
                  description="Team changes require manager approval"
                />
                <ToggleSwitch
                  enabled={settings.team?.showSensitiveData}
                  onChange={(value) => handleSettingChange('team', 'showSensitiveData', value)}
                  label="Show Sensitive Data"
                  description="Display detailed performance comparisons between team members"
                />
              </div>
            )}

            {/* Privacy Tab */}
            {activeTab === 'privacy' && (
              <div className="space-y-4">
                <ToggleSwitch
                  enabled={settings.privacy?.anonymizeData}
                  onChange={(value) => handleSettingChange('privacy', 'anonymizeData', value)}
                  label="Anonymize Data"
                  description="Hide developer names in exported reports and analytics"
                />
                <SelectField
                  value={settings.privacy?.retentionPeriod}
                  onChange={(value) => handleSettingChange('privacy', 'retentionPeriod', value)}
                  label="Data Retention Period"
                  description="How long to keep performance data"
                  options={[
                    { value: '90', label: '90 days' },
                    { value: '180', label: '6 months' },
                    { value: '365', label: '1 year' },
                    { value: '730', label: '2 years' },
                    { value: '-1', label: 'Keep forever' }
                  ]}
                />
                <ToggleSwitch
                  enabled={settings.privacy?.shareAnalytics}
                  onChange={(value) => handleSettingChange('privacy', 'shareAnalytics', value)}
                  label="Share Analytics"
                  description="Allow sharing anonymized analytics with DevLens for product improvement"
                />
                <ToggleSwitch
                  enabled={settings.privacy?.exportEnabled}
                  onChange={(value) => handleSettingChange('privacy', 'exportEnabled', value)}
                  label="Enable Data Export"
                  description="Allow exporting performance data and reports"
                />

                {/* Data Management Actions */}
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <h3 className="font-semibold text-black mb-4">Data Management</h3>
                  <div className="flex gap-4">
                    <button 
                      onClick={handleExportData}
                      className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                    >
                      <Download size={16} />
                      Export Data
                    </button>
                    <label className="flex items-center gap-2 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                      <Upload size={16} />
                      Import Data
                      <input
                        type="file"
                        accept=".json"
                        onChange={handleImportData}
                        className="hidden"
                      />
                    </label>
                    <button 
                      onClick={handleClearData}
                      className="flex items-center gap-2 px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors"
                    >
                      <AlertTriangle size={16} />
                      Clear All Data
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;