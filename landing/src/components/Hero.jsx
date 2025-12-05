import React from 'react';
import { FaArrowRight } from 'react-icons/fa';
import '../styles/Hero.css';

const logo = new URL('../../artifacts/ampora_ai_logo.png', import.meta.url).href;

const Hero = () => {
  const handleFreeTrial = () => {
    // Google Forms link for interest form
    const formsLink = 'https://forms.gle/5JB7j16G82VRZr9i8';
    window.open(formsLink, '_blank');
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
          <button className="coming-soon-button" disabled style={{ cursor: 'not-allowed', opacity: 0.6 }}>
            Coming Soon
          </button>
        </div>
        
        <div className="hero-content">
          <h1 className="hero-title">
            AI-Powered Educational Video Generation Platform
          </h1>
          <p className="hero-subtitle">
            Transform any technical concept into a complete video lesson with slides, 
            voiceover, and visual explanations—generated in minutes, not hours.
          </p>
          <p className="hero-description">
            Quality STEM education materials are expensive and time-consuming to create. 
            Ampora AI generates personalized explanations at near-zero cost, making 
            technical education accessible to everyone regardless of financial background. 
            Similar to StatQuest's visual teaching style, but available for any STEM topic 
            with career advancement capabilities built in.
          </p>
          
          <div className="hero-buttons">
            <button className="cta-button primary" onClick={handleFreeTrial}>
              Get Free Trial Access
              <FaArrowRight className="button-icon" />
            </button>
          </div>
          
          <p className="forms-explanation">
            By signing up for early access, you'll help us demonstrate market demand to potential investors 
            and be among the first to experience AI-generated educational videos. Your interest helps us 
            bring accessible, high-quality STEM education to students everywhere.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Hero;
