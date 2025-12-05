import React from 'react';
import '../styles/Footer.css';

const logo = new URL('../../artifacts/ampora_ai_logo.png', import.meta.url).href;

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-brand">
            <img 
              src={logo} 
              alt="Ampora AI" 
              className="footer-logo"
            />
            <p className="footer-tagline">
              AI-Powered Career Learning Platform
            </p>
          </div>
          
          <div className="footer-links">
            <div className="footer-section">
              <h4>Product</h4>
              <a href="#about">About</a>
              <a href="#demos">Demos</a>
              <a href="#team">Team</a>
            </div>
            
            <div className="footer-section">
              <h4>Company</h4>
              <a href="#team">Our Team</a>
              <a href="#contact">Contact</a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>&copy; 2025 Ampora AI. All rights reserved.</p>
          <p className="footer-note">Coming Soon - Join our waitlist for early access</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

