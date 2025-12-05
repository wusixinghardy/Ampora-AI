import React from 'react';
import { FaArrowRight } from 'react-icons/fa';
import '../styles/Hero.css';

const logo = '/Ampora-AI/ampora_ai_logo.png';

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
          
          {/* Inline styles added to fix squished nav links */}
          <nav className="hero-nav" style={{ display: 'flex', gap: '30px', alignItems: 'center' }}>
            <a href="#about">About</a>
            <a href="#demos">Demos</a>
            <a href="#team">Our Team</a>
          </nav>

          <button className="coming-soon-button" disabled style={{ cursor: 'not-allowed', opacity: 0.6 }}>
            Coming Soon
          </button>
        </div>

        <div className="hero-content">
          <h1 className="hero-title">
            The "Sora" for Education & Enterprise Training
          </h1>
          <p className="hero-subtitle">
            Transform any text, PDF, or technical concept into a systematic, long-form video course—generated instantly with professional voiceovers and visual storytelling.
          </p>
          <p className="hero-description">
            Ampora solves the high cost of video production and the scarcity of personalized content. 
            We are building the engine for universal learning: whether you are a university student needing a 
            guide for a <strong>just-published research paper</strong>, or an enterprise scaling <strong>internal compliance and technical training</strong>, 
            Ampora generates it instantly. Our proprietary AI ensures copyright compliance and pedagogical structure, 
            making deep-dive education accessible, up-to-date, and affordable for everyone.
          </p>

          <div className="hero-buttons">
            <button className="cta-button primary" onClick={handleFreeTrial}>
              Get Free Trial Access
              <FaArrowRight className="button-icon" />
            </button>
          </div>

          <p className="forms-explanation">
            By signing up for early access, you'll help us demonstrate market demand to potential investors.
            Join our waitlist to be the first to experience the future of generative video learning.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Hero;