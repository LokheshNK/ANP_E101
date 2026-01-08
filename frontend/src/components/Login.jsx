import React, { useState, useEffect } from 'react';
import { Shield, Eye, EyeOff, Building, User, Lock, Plus } from 'lucide-react';
import { useApp } from '../context/AppContext';
import Register from './Register';

const Login = () => {
  const { login } = useApp();
  const [showRegister, setShowRegister] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    company: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [companies, setCompanies] = useState([]);

  // Fetch companies on component mount
  useEffect(() => {
    const fetchCompanies = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/companies');
        if (response.ok) {
          const data = await response.json();
          console.log('Companies API response:', data); // Debug log
          if (data.success && Array.isArray(data.companies)) {
            setCompanies(data.companies);
          } else {
            throw new Error('Invalid API response format');
          }
        } else {
          throw new Error(`API returned ${response.status}`);
        }
      } catch (error) {
        console.error('Error fetching companies:', error);
        // Fallback to mock data as objects to match API format
        setCompanies([
          { id: 1, name: 'TechCorp Inc.' },
          { id: 2, name: 'Innovate Solutions' },
          { id: 3, name: 'StartupIO' },
          { id: 4, name: 'GLV' }
        ]);
      }
    };

    fetchCompanies();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    const result = await login(formData.email, formData.password, formData.company);
    
    if (!result.success) {
      setError(result.error || 'Login failed');
    }
    
    setIsLoading(false);
  };

  if (showRegister) {
    return <Register onBack={() => setShowRegister(false)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Logo and Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 text-green-600 mb-4">
            <Shield size={40} />
            <h1 className="text-4xl font-black">DEVLENS</h1>
          </div>
          <p className="text-gray-600">Manager Portal</p>
          <p className="text-sm text-gray-500 mt-2">Access your team's performance analytics</p>
        </div>

        {/* Login Form */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Company Selection */}
            <div>
              <label className="block text-sm font-medium text-black mb-2">
                <Building size={16} className="inline mr-2" />
                Company
              </label>
              <select
                name="company"
                value={formData.company}
                onChange={handleInputChange}
                required
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              >
                <option value="">Select your company</option>
                {companies.map(company => (
                  <option key={company.id} value={company.name}>
                    {company.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-black mb-2">
                <User size={16} className="inline mr-2" />
                Email Address
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                placeholder="manager@company.com"
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-medium text-black mb-2">
                <Lock size={16} className="inline mr-2" />
                Password
              </label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                  placeholder="Enter your password"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 pr-12"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-green-600 text-white p-3 rounded-lg font-medium hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>

            {/* Create New Account Button */}
            <button
              type="button"
              onClick={() => setShowRegister(true)}
              className="w-full flex items-center justify-center gap-2 p-3 border border-green-600 text-green-600 rounded-lg hover:bg-green-50 transition-colors"
            >
              <Plus size={16} />
              Create New Company & Manager Account
            </button>
          </form>

          {/* Demo Credentials */}
          <div className="mt-8 p-4 bg-gray-50 rounded-lg">
            <h3 className="font-medium text-black mb-3">Demo Credentials:</h3>
            <div className="space-y-2 text-sm">
              <div className="p-2 bg-white rounded border">
                <p><strong>TechCorp Inc.</strong></p>
                <p>Email: john.smith@techcorp.com</p>
                <p>Password: admin123</p>
              </div>
              <div className="p-2 bg-white rounded border">
                <p><strong>Innovate Solutions</strong></p>
                <p>Email: sarah.johnson@innovate.com</p>
                <p>Password: manager456</p>
              </div>
              <div className="p-2 bg-white rounded border">
                <p><strong>StartupIO</strong></p>
                <p>Email: mike.chen@startup.io</p>
                <p>Password: startup789</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;