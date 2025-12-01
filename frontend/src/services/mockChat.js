/**
 * Mock Chat Service
 * 
 * Simulates backend chat API for testing without backend.
 * Can be easily replaced with real backend calls later.
 */

// Configuration - Set to false to use real backend
const USE_MOCK_CHAT = true; // Change this to false when backend is ready

// Simulate network delay
const simulateDelay = (ms = 1000) => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Mock responses based on message content
const getMockResponse = (message) => {
  const lowerMessage = message.toLowerCase();
  
  // Video generation prompts
  if (lowerMessage.includes('video') || lowerMessage.includes('generate') || lowerMessage.includes('create')) {
    return {
      response: "I'm processing your video generation request. This will take a few moments. The backend is working on creating your video content!",
      video_url: null, // Will be set after video is generated
      is_generating: true
    };
  }
  
  // General responses
  if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
    return {
      response: "Hello! I'm Ampora AI. I can help you generate video content. Try asking me to create a video or generate content!",
      video_url: null
    };
  }
  
  if (lowerMessage.includes('help')) {
    return {
      response: "I can help you:\n• Generate video content\n• Create lecture videos\n• Process your requests\n\nTry: 'Create a video about machine learning' or 'Generate a lecture on Python basics'",
      video_url: null
    };
  }
  
  // Default response
  return {
    response: `I understand you said: "${message}". The backend chat service is currently in development. This is a mock response for testing. Once the backend is ready, I'll be able to process your requests and generate videos!`,
    video_url: null
  };
};

/**
 * Mock Chat Service
 */
export const mockChatService = {
  /**
   * Check if mock chat should be used
   */
  useMockChat: () => {
    const envSetting = import.meta.env.VITE_USE_MOCK_CHAT;
    const localStorageSetting = localStorage.getItem('use_mock_chat');
    
    if (localStorageSetting !== null) {
      return localStorageSetting === 'true';
    }
    
    return envSetting === 'true' || USE_MOCK_CHAT;
  },
  
  /**
   * Send chat message (mock or real backend)
   */
  async sendMessage(message, token = null) {
    if (this.useMockChat()) {
      // Mock response
      await simulateDelay(1500); // Simulate processing time
      
      const mockResponse = getMockResponse(message);
      
      // Simulate video generation for certain prompts
      if (mockResponse.is_generating) {
        // Return immediate response
        // In real app, video URL would come later via polling or websocket
        return mockResponse;
      }
      
      return mockResponse;
    } else {
      // Real backend call
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      
      const headers = {
        'Content-Type': 'application/json',
      };
      
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ message })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    }
  }
};

export default mockChatService;
