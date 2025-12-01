import React, { useState } from 'react';
import ChatInterface from './ChatInterface';
import LoadingIndicator from './LoadingIndicator';
import VideoPlayer from './VideoPlayer';
import { FaSignOutAlt } from 'react-icons/fa';
import '../styles/Dashboard.css';

const Dashboard = ({ onLogout }) => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [user] = useState(() => {
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  });

  const handleLogout = () => {
    onLogout();
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-left">
          <img src="/ampora_ai_logo.png" alt="Ampora AI Logo" className="header-logo" />
          <h1>Ampora AI Dashboard</h1>
        </div>
        <div className="header-right">
          <span className="username">Welcome, {user?.username || 'User'}!</span>
          <button className="logout-button" onClick={handleLogout}>
            <FaSignOutAlt /> Logout
          </button>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="dashboard-main">
          <div className="dashboard-left">
            <ChatInterface 
              setIsProcessing={setIsProcessing}
              setVideoUrl={setVideoUrl}
            />
          </div>

          <div className="dashboard-right">
            <LoadingIndicator isActive={isProcessing} />
          </div>
        </div>

        <div className="dashboard-bottom">
          <VideoPlayer videoUrl={videoUrl} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
