import React from 'react';
import { FaArrowRight, FaEnvelope } from 'react-icons/fa';
import '../styles/CTA.css';

const CTA = () => {
  const handleFreeTrial = () => {
    // Google Forms link for interest form
    const formsLink = 'https://forms.gle/5JB7j16G82VRZr9i8';
    window.open(formsLink, '_blank');
  };

  return (
    <section className="cta-section">
      <div className="cta-container">
        <h2 className="cta-title">Ready to Transform How You Learn & Train?</h2>
        <p className="cta-subtitle">
          Join our waitlist for early access to the "Sora" for long-form education. 
          Help us demonstrate the overwhelming demand for instant, high-quality video generation.
        </p>
        
        <div className="cta-buttons">
          <button className="cta-button primary large" onClick={handleFreeTrial}>
            <FaEnvelope className="button-icon" />
            Sign Up for Free Trial
          </button>
        </div>
        
        <div className="forms-explanation-box">
          <h4>Why Sign Up?</h4>
          <p>
            By joining our waitlist, you're helping us prove the market demand for a universal 
            video generation engine that serves both <strong>Higher Education and Enterprise</strong>. 
            Your participation demonstrates that the world is ready to replace expensive, slow video 
            production with AI that instantly turns <strong>text, PDFs, and research papers</strong> into 
            systematic video courses. Be the first to experience the future of scalable knowledge 
            and help us democratize access to deep-dive training for everyone.
          </p>
        </div>
      </div>
    </section>
  );
};

export default CTA;