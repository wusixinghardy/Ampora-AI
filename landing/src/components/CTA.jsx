import React from 'react';
import { FaArrowRight, FaEnvelope } from 'react-icons/fa';
import '../styles/CTA.css';

const CTA = () => {
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
    <section className="cta-section">
      <div className="cta-container">
        <h2 className="cta-title">Ready to Transform Your Learning?</h2>
        <p className="cta-subtitle">
          Join our waitlist for early access and a free trial when we officially launch.
          Help us show investors the overwhelming demand for accessible AI-powered education.
        </p>
        
        <div className="cta-buttons">
          <button className="cta-button primary large" onClick={handleFreeTrial}>
            <FaEnvelope className="button-icon" />
            Sign Up for Free Trial
          </button>
        </div>
        
        <p className="cta-note">
          By signing up, you'll be among the first to experience AI-generated video lessons 
          and help us demonstrate market demand to potential investors.
        </p>
      </div>
    </section>
  );
};

export default CTA;

