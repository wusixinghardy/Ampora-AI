import React from 'react';
import { FaDownload } from 'react-icons/fa';
import '../styles/VideoPlayer.css';

const VideoPlayer = ({ videoUrl }) => {
  const handleDownload = async () => {
    if (!videoUrl) return;
    
    try {
      const response = await fetch(videoUrl);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ampora-video-${Date.now()}.mp4`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download failed:', error);
      alert('Failed to download video. Please try again.');
    }
  };

  return (
    <div className="video-player-container">
      <div className="video-header">
        <h2>Generated Video</h2>
        {videoUrl && (
          <button className="download-video-button" onClick={handleDownload} title="Download Video">
            <FaDownload /> Download MP4
          </button>
        )}
      </div>
      
      <div className="video-content">
        {videoUrl ? (
          <div className="video-wrapper">
            <video 
              controls 
              className="video-element"
              key={videoUrl}
            >
              <source src={videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        ) : (
          <div className="no-video-state">
            <div className="no-video-icon">🎬</div>
            <p>No video generated yet</p>
            <p className="no-video-subtitle">Start chatting to generate your first video</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default VideoPlayer;
