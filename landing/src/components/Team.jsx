import React from 'react';
import '../styles/Team.css';

const Team = () => {
  // Team members with headshots and enhanced descriptions
  // Vite serves files from public folder, BASE_URL handles the path prefix
  const basePath = import.meta.env.BASE_URL;
  const teamMembers = [
    {
      id: 1,
      name: 'Sixing (Hardy) Wu',
      role: 'Co-Founder & Chief Executive Officer',
      description: 'Brings technical depth in backend and AI integration features combined with strategic business vision to drive Ampora\'s growth and innovation.',
      image: `${basePath}hardy_headshot.jpeg`
    },
    {
      id: 2,
      name: 'Sam Liu',
      role: 'Co-Founder & Chief Operating Officer',
      description: 'Expert in full product lifecycle management and user experience development, ensuring seamless operations and exceptional user satisfaction.',
      image: `${basePath}sam_headshot.jpg`
    },
    {
      id: 3,
      name: 'Robert Jarman',
      role: 'Chief Technology Officer',
      description: 'Lead full stack developer architecting the technical foundation, building scalable systems that power Ampora\'s video generation platform.',
      image: `${basePath}robert_headshot.jpeg`
    }
  ];

  return (
    <section className="team" id="team">
      <div className="team-container">
        <h2 className="section-title">Meet The Team</h2>
        <p className="section-subtitle">
          Passionate innovators building the future of AI-powered educational content
        </p>
        
        <div className="team-members">
          {teamMembers.map((member) => (
            <div key={member.id} className="team-member">
              <div className="member-image-container">
                <img 
                  src={member.image} 
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

        <div className="why-team-section">
          <h3 className="why-team-title">Why We're the Right Team</h3>
          <p className="why-team-text">
            We're living the problem we're solving: We're not outside consultants or business school students with a theory—we're CS students actively struggling through these courses right now. We know exactly which concepts trip students up because they trip us up too. We understand the frustration of watching a professor explain dynamic programming once with pure math notation and never return to it. We know what it's like to scramble at 11pm before a deadline, desperately searching for StatQuest-quality explanations that don't exist for our specific topic.
          </p>
          <p className="why-team-text">
            Our authentic connection to the user base, combined with our technical expertise in AI, full-stack development, and product management, makes us uniquely equipped to build Ampora into the educational platform that students actually need and want to use.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Team;
