/**
 * Mock Authentication Service
 * 
 * This service simulates backend authentication for testing purposes.
 * It stores users in localStorage and can be easily replaced with real backend calls.
 * 
 * To switch to real backend: Set USE_MOCK_AUTH to false in the config
 */

// Configuration - Set to false to use real backend
const USE_MOCK_AUTH = false; // Changed to false - backend is ready!

// Test accounts (for development/testing)
const TEST_ACCOUNTS = {
  'testuser': {
    username: 'testuser',
    email: 'test@example.com',
    password: 'test123', // In real app, this would be hashed
    id: 'test-user-1',
    createdAt: new Date().toISOString()
  },
  'demo': {
    username: 'demo',
    email: 'demo@example.com',
    password: 'demo123',
    id: 'demo-user-1',
    createdAt: new Date().toISOString()
  }
};

// Storage keys
const STORAGE_KEY_USERS = 'ampora_mock_users';
const STORAGE_KEY_SESSIONS = 'ampora_mock_sessions';

/**
 * Initialize mock storage - creates test accounts if they don't exist
 */
const initializeMockStorage = () => {
  if (typeof window === 'undefined') return;
  
  // Initialize users storage
  let users = JSON.parse(localStorage.getItem(STORAGE_KEY_USERS) || '{}');
  
  // Add test accounts if not present
  Object.keys(TEST_ACCOUNTS).forEach(username => {
    if (!users[username]) {
      users[username] = TEST_ACCOUNTS[username];
    }
  });
  
  localStorage.setItem(STORAGE_KEY_USERS, JSON.stringify(users));
  
  // Initialize sessions storage
  if (!localStorage.getItem(STORAGE_KEY_SESSIONS)) {
    localStorage.setItem(STORAGE_KEY_SESSIONS, JSON.stringify({}));
  }
};

/**
 * Get all mock users from localStorage
 */
const getMockUsers = () => {
  if (typeof window === 'undefined') return {};
  const users = localStorage.getItem(STORAGE_KEY_USERS);
  return users ? JSON.parse(users) : {};
};

/**
 * Generate a simple token (for mock purposes)
 */
const generateMockToken = (userId) => {
  return `mock_token_${userId}_${Date.now()}`;
};

/**
 * Simulate network delay
 */
const simulateDelay = (ms = 500) => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

/**
 * Mock Login
 */
export const mockLogin = async (username, password) => {
  await simulateDelay(800); // Simulate network delay
  
  const users = getMockUsers();
  const user = users[username];
  
  if (!user) {
    throw new Error('User not found. Use test accounts: testuser/test123 or demo/demo123');
  }
  
  if (user.password !== password) {
    throw new Error('Invalid password. Try: test123 or demo123');
  }
  
  const token = generateMockToken(user.id);
  
  // Store session
  const sessions = JSON.parse(localStorage.getItem(STORAGE_KEY_SESSIONS) || '{}');
  sessions[token] = {
    userId: user.id,
    username: user.username,
    expiresAt: Date.now() + (7 * 24 * 60 * 60 * 1000) // 7 days
  };
  localStorage.setItem(STORAGE_KEY_SESSIONS, JSON.stringify(sessions));
  
  return {
    token,
    user: {
      id: user.id,
      username: user.username,
      email: user.email
    }
  };
};

/**
 * Mock Signup
 */
export const mockSignup = async (username, email, password) => {
  await simulateDelay(1000); // Simulate network delay
  
  const users = getMockUsers();
  
  // Check if username already exists
  if (users[username]) {
    throw new Error('Username already exists. Please choose a different username.');
  }
  
  // Check if email already exists
  const existingUser = Object.values(users).find(u => u.email === email);
  if (existingUser) {
    throw new Error('Email already registered. Please use a different email.');
  }
  
  // Validate password
  if (password.length < 6) {
    throw new Error('Password must be at least 6 characters long.');
  }
  
  // Create new user
  const newUser = {
    username,
    email,
    password, // In real app, this would be hashed
    id: `user_${Date.now()}`,
    createdAt: new Date().toISOString()
  };
  
  users[username] = newUser;
  localStorage.setItem(STORAGE_KEY_USERS, JSON.stringify(users));
  
  const token = generateMockToken(newUser.id);
  
  // Store session
  const sessions = JSON.parse(localStorage.getItem(STORAGE_KEY_SESSIONS) || '{}');
  sessions[token] = {
    userId: newUser.id,
    username: newUser.username,
    expiresAt: Date.now() + (7 * 24 * 60 * 60 * 1000)
  };
  localStorage.setItem(STORAGE_KEY_SESSIONS, JSON.stringify(sessions));
  
  return {
    token,
    user: {
      id: newUser.id,
      username: newUser.username,
      email: newUser.email
    }
  };
};

/**
 * Mock Token Validation
 */
export const mockValidateToken = (token) => {
  if (!token) return null;
  
  const sessions = JSON.parse(localStorage.getItem(STORAGE_KEY_SESSIONS) || '{}');
  const session = sessions[token];
  
  if (!session) return null;
  
  // Check if session expired
  if (session.expiresAt < Date.now()) {
    delete sessions[token];
    localStorage.setItem(STORAGE_KEY_SESSIONS, JSON.stringify(sessions));
    return null;
  }
  
  const users = getMockUsers();
  const user = Object.values(users).find(u => u.id === session.userId);
  
  if (!user) return null;
  
  return {
    id: user.id,
    username: user.username,
    email: user.email
  };
};

/**
 * Main Authentication Service
 * This is the interface that components should use
 */
export const authService = {
  /**
   * Check if mock auth should be used
   */
  useMockAuth: () => {
    // Check environment variable or localStorage setting
    const envSetting = import.meta.env.VITE_USE_MOCK_AUTH;
    const localStorageSetting = localStorage.getItem('use_mock_auth');
    
    if (localStorageSetting !== null) {
      return localStorageSetting === 'true';
    }
    
    return envSetting === 'true' || USE_MOCK_AUTH;
  },
  
  /**
   * Login
   */
  async login(username, password) {
    // Initialize storage on first use
    initializeMockStorage();
    
    if (this.useMockAuth()) {
      return await mockLogin(username, password);
    } else {
      // Real backend call
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Login failed');
      }
      
      return await response.json();
    }
  },
  
  /**
   * Signup
   * Future: Add paymentIntentId parameter for Stripe integration
   */
  async signup(username, email, password, paymentIntentId = null) {
    // Initialize storage on first use
    initializeMockStorage();
    
    if (this.useMockAuth()) {
      // For mock, ignore payment for now
      // TODO: Add Stripe payment validation here
      return await mockSignup(username, email, password);
    } else {
      // Real backend call - will include paymentIntentId when Stripe is integrated
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          paymentIntentId // Will be used for Stripe verification
        })
      });
      
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || 'Signup failed');
      }
      
      return await response.json();
    }
  },
  
  /**
   * Validate token
   */
  validateToken(token) {
    if (this.useMockAuth()) {
      return mockValidateToken(token);
    } else {
      // Real backend validation would go here
      // For now, just check if token exists
      return token ? { valid: true } : null;
    }
  }
};

// Export test account info for documentation
export const TEST_ACCOUNT_INFO = {
  accounts: Object.keys(TEST_ACCOUNTS).map(username => ({
    username,
    password: TEST_ACCOUNTS[username].password,
    email: TEST_ACCOUNTS[username].email
  }))
};



