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
        
        <div className="forms-explanation-box">
          <h4>Why Sign Up?</h4>
          <p>
            By filling out our interest form, you're helping us demonstrate real market demand 
            to potential investors and VCs. Your participation shows that students are actively 
            seeking better educational resources and are willing to support innovative solutions 
            that make STEM education more accessible. When we launch, you'll be among the first 
            to experience AI-generated educational videos and help shape the future of personalized 
            learning. Your interest directly contributes to bringing high-quality, affordable 
            STEM education to students everywhere.
          </p>
        </div>
      </div>
    </section>
  );
};

export default CTA;
