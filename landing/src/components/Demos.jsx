import '../styles/Demos.css';

const Demos = () => {
  return (
    <section className="demos" id="demos">
      <div className="demos-container">
        <h2 className="section-title">See It In Action</h2>
        <p className="section-subtitle">
          Watch our AI generate complete video lessons from simple text prompts
        </p>

        <div className="demos-grid">
          <div className="demo-card">
            <h3>Bubble Sort Algorithm</h3>
            <p className="demo-description">
              A complete video lesson explaining the bubble sort algorithm,
              generated entirely by AI.
            </p>
            <div className="video-wrapper">
              <video
                controls
                className="demo-video"
                poster="/Ampora-AI/ampora_ai_logo.png"
              >
                <source src="/Ampora-AI/Bubble_Sort_Algorithm.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </div>

          <div className="demo-card">
            <h3>Platform Walkthrough</h3>
            <p className="demo-description">
              See how easy it is to generate video content with Ampora AI.
              From prompt to video in minutes.
            </p>
            <div className="video-wrapper">
              <video
                controls
                className="demo-video"
                poster="/Ampora-AI/ampora_ai_logo.png"
              >
                <source src="/Ampora-AI/Balance_Sheet.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Demos;