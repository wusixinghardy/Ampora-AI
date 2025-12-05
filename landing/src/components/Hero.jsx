import React from 'react';
import { FaArrowRight } from 'react-icons/fa';
import '../styles/Hero.css';

const logo = new URL('../../artifacts/ampora_ai_logo.png', import.meta.url).href;

const Hero = () => {
  const handleComingSoon = () => {
    // Will redirect to login/signup when launched
    alert('Coming Soon! This will redirect to signup/login when we officially launch.');
  };

  const handleFreeTrial = () => {
    // Placeholder for Google Forms link
    const formsLink = 'YOUR_GOOGLE_FORMS_LINK_HERE'; // Replace with actual link
    if (formsLink !== 'YOUR_GOOGLE_FORMS_LINK_HERE') {
      window.open(formsLink, '_blank');
    } else {
      alert('Google Forms link will be added here. This collects: Name, Email, Phone, and interest details for investors.');
    }
  };

  return (
    <section className="hero">
      <div className="hero-container">
        <div className="hero-header">
          <img 
            src={logo} 
            alt="Ampora AI Logo" 
            className="hero-logo"
          />
          <button className="coming-soon-button" onClick={handleComingSoon}>
            Coming Soon
          </button>
        </div>
        
        <div className="hero-content">
          <h1 className="hero-title">
            AI-Powered Career Learning Platform
          </h1>
          <p className="hero-subtitle">
            Transform any technical concept into a complete video lesson with slides, 
            voiceover, and visual explanations—generated in minutes, not hours.
          </p>
          <p className="hero-description">
            Quality STEM education materials are expensive and time-consuming to create. 
            Ampora AI generates personalized explanations at near-zero cost, making 
            technical education accessible to everyone regardless of financial background.
          </p>
          
          <div className="hero-buttons">
            <button className="cta-button primary" onClick={handleFreeTrial}>
              Get Free Trial Access
              <FaArrowRight className="button-icon" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;

