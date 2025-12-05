import React from 'react';
import '../styles/About.css';

const About = () => {
  return (
    <section className="about" id="about">
      <div className="about-container">
        <h2 className="section-title">What is Ampora?</h2>
        
        <div className="about-content">
          <div className="about-text">
            <p className="about-paragraph">
              Ampora is a generative AI platform that transforms text, PDFs, and research papers 
              into systematic, long-form video courses. Unlike standard video tools that create 
              short clips, our engine builds complete, coherent lectures with professional voiceovers 
              and visual storytelling—instantly.
            </p>
            
            <p className="about-paragraph">
              We bridge the gap between higher education and enterprise training. Whether you are 
              a student needing a guide for a just-published research paper, or a company 
              needing to scale internal compliance and technical onboarding, Ampora automates 
              the production of high-quality, copyright-compliant educational video at scale.
            </p>
            
            <div className="features-grid">
              <div className="feature-card">
                <h3>Instant Long-Form</h3>
                <p>Generate full 20+ minute lectures, not just short clips</p>
              </div>
              <div className="feature-card">
                <h3>Universal Input</h3>
                <p>Turn PDFs, codebases, or prompt text into video courses</p>
              </div>
              <div className="feature-card">
                <h3>Enterprise Ready</h3>
                <p>Secure, copyright-compliant generation for internal training</p>
              </div>
              <div className="feature-card">
                <h3>Adaptive Learning</h3>
                <p>Personalized depth and pacing for any skill level</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;