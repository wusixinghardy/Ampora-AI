import React, { useState } from 'react';
import { FaUser, FaLock, FaEnvelope } from 'react-icons/fa';
import { authService } from '../services/mockAuth';
import PaymentStep from './PaymentStep';
import '../styles/LoginSignup.css';

const LoginSignup = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPayment, setShowPayment] = useState(false);
  const [paymentIntentId, setPaymentIntentId] = useState(null);
  const [subscriptionPrice, setSubscriptionPrice] = useState(9.99);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login - using auth service (mock or real backend)
        const result = await authService.login(formData.username, formData.password);
        onLogin(result.token, result.user);
      } else {
        // Signup
        // Validate passwords match
        if (formData.password !== formData.confirmPassword) {
          setError('Passwords do not match');
          setLoading(false);
          return;
        }

        // Validate password strength
        if (formData.password.length < 6) {
          setError('Password must be at least 6 characters long');
          setLoading(false);
          return;
        }

        // Check if test account (bypasses payment)
        const testAccounts = ['testuser', 'demo', 'dev', 'admin'];
        const isTestAccount = testAccounts.includes(formData.username.toLowerCase());
        
        if (isTestAccount) {
          // Test accounts bypass payment
          const result = await authService.signup(
            formData.username,
            formData.email,
            formData.password,
            null
          );
          onLogin(result.token, result.user);
        } else {
          // Show payment step for real accounts
          setShowPayment(true);
        }
      }
    } catch (err) {
      // Handle errors from auth service
      setError(err.message || 'An error occurred. Please try again.');
      console.error('Auth error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-signup-container">
      <div className="login-signup-card">
        <div className="login-signup-header">
          <img src="/ampora_ai_logo.png" alt="Ampora AI Logo" className="login-logo" />
          <h1>Ampora AI</h1>
          <p>Welcome! Please {isLogin ? 'sign in' : 'create an account'} to continue</p>
        </div>

        <div className="login-signup-tabs">
          <button
            className={`tab-button ${isLogin ? 'active' : ''}`}
            onClick={() => {
              setIsLogin(true);
              setError('');
              setFormData({
                username: '',
                email: '',
                password: '',
                confirmPassword: ''
              });
            }}
          >
            Login
          </button>
          <button
            className={`tab-button ${!isLogin ? 'active' : ''}`}
            onClick={() => {
              setIsLogin(false);
              setError('');
              setFormData({
                username: '',
                email: '',
                password: '',
                confirmPassword: ''
              });
            }}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-signup-form">
          <div className="form-group">
            <FaUser className="form-icon" />
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <FaEnvelope className="form-icon" />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          )}

          <div className="form-group">
            <FaLock className="form-icon" />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <FaLock className="form-icon" />
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm Password"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          {!showPayment && (
            <button type="submit" className="submit-button" disabled={loading}>
              {loading ? 'Processing...' : (isLogin ? 'Login' : 'Sign Up')}
            </button>
          )}
        </form>

        {showPayment && (
          <div className="payment-wrapper">
            <PaymentStep
              amount={subscriptionPrice}
              onPaymentSuccess={async (paymentIntentId) => {
                try {
                  setLoading(true);
                  setError('');
                  
                  const result = await authService.signup(
                    formData.username,
                    formData.email,
                    formData.password,
                    paymentIntentId
                  );
                  
                  onLogin(result.token, result.user);
                } catch (err) {
                  setError(err.message || 'Signup failed after payment');
                  setShowPayment(false);
                } finally {
                  setLoading(false);
                }
              }}
              onCancel={() => {
                setShowPayment(false);
                setError('');
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default LoginSignup;
