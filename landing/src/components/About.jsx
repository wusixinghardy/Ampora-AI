import React from 'react';
import '../styles/About.css';

const About = () => {
  return (
    <section className="about" id="about">
      <div className="about-container">
        <h2 className="section-title">What is Ampora AI?</h2>
        
        <div className="about-content">
          <div className="about-text">
            <p className="about-paragraph">
              Ampora AI is an educational video generation platform that automatically creates 
              high-quality, StatQuest-style video lessons on STEM topics. Students can input 
              any technical concept (like "explain convolutional neural networks" or "how to 
              prep for a Google SWE interview") and receive a complete video lesson with slides, 
              voiceover, and visual explanations generated in minutes.
            </p>
            
            <p className="about-paragraph">
              Our platform combines the visual teaching excellence of channels like StatQuest and 
              3Blue1Brown with AI-powered personalization, making complex STEM concepts accessible 
              to everyone. Beyond educational content, we also provide career advancement features 
              including interview preparation and skill development resources.
            </p>
            
            <div className="features-grid">
              <div className="feature-card">
                <h3>⚡ Fast Generation</h3>
                <p>Complete video lessons in minutes, not hours</p>
              </div>
              <div className="feature-card">
                <h3>💰 Cost-Effective</h3>
                <p>Near-zero cost compared to traditional content creation</p>
              </div>
              <div className="feature-card">
                <h3>🎯 Personalized</h3>
                <p>AI-generated content tailored to your learning needs</p>
              </div>
              <div className="feature-card">
                <h3>📚 STEM Focused</h3>
                <p>Specialized in technical content with career advancement tools</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;
