import React from 'react';
import '../styles/Team.css';

const logo = new URL('../../artifacts/ampora_ai_logo.png', import.meta.url).href;

const Team = () => {
  // Team members - placeholder images will be added to artifacts folder
  const teamMembers = [
    {
      id: 1,
      name: 'Robert Jarman',
      role: 'DevOps Engineer & Project Manager',
      description: 'Manages infrastructure, deployment, and project coordination'
    },
    {
      id: 2,
      name: 'Hardy',
      role: 'Backend Developer',
      description: 'Builds the AI video generation pipeline and API services'
    },
    {
      id: 3,
      name: 'Sam',
      role: 'Backend Developer',
      description: 'Develops core AI services and integration systems'
    }
  ];

  return (
    <section className="team" id="team">
      <div className="team-container">
        <h2 className="section-title">Meet The Team</h2>
        <p className="section-subtitle">
          Passionate developers building the future of AI-powered education
        </p>
        
        <div className="team-members">
          {teamMembers.map((member) => (
            <div key={member.id} className="team-member">
              <div className="member-image-container">
                <img 
                  src={logo} 
                  alt={`${member.name}`} 
                  className="member-image"
                  onError={(e) => {
                    // Fallback to placeholder if image doesn't exist
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'flex';
                  }}
                />
                <div className="member-placeholder" style={{ display: 'none' }}>
                  <span className="placeholder-icon">👤</span>
                  <p>Photo Coming Soon</p>
                </div>
              </div>
              <div className="member-info">
                <h3 className="member-name">{member.name}</h3>
                <p className="member-role">{member.role}</p>
                <p className="member-description">{member.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Team;

