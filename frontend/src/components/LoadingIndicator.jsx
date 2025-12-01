import React from 'react';
import '../styles/LoadingIndicator.css';

const LoadingIndicator = ({ isActive }) => {
  return (
    <div className="loading-indicator-container">
      <div className="loading-header">
        <h2>Processing Status</h2>
      </div>
      
      <div className="loading-content">
        {isActive ? (
          <>
            <svg
              width="150"
              height="150"
              viewBox="0 0 150 150"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="generating-spin"
            >
              <circle cx="75" cy="75" r="70" stroke="#0EA5E9" strokeWidth="2" fill="none" />
              <circle cx="75" cy="75" r="50" stroke="#0EA5E9" strokeWidth="2" strokeLinecap="round" strokeDasharray="4 4" fill="none" />
              <circle cx="75" cy="75" r="30" stroke="#0EA5E9" strokeWidth="2" strokeLinecap="round" strokeDasharray="8 8" fill="none" />
              <circle cx="75" cy="75" r="15" fill="rgba(14, 165, 233, 0.2)" />
              <circle cx="75" cy="75" r="5" fill="#0EA5E9" />
            </svg>
            <div className="loading-message">
              <h3>Backend Processing...</h3>
              <p>Your video is being generated</p>
              <p>This may take a few moments</p>
            </div>
          </>
        ) : (
          <div className="idle-state">
            <div className="idle-icon">⚡</div>
            <p>Ready to process your request</p>
            <p className="idle-subtitle">Send a message to start generating</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default LoadingIndicator;
