import React from 'react';
import './App.css';
import Hero from './components/Hero';
import About from './components/About';
import Team from './components/Team';
import Demos from './components/Demos';
import CTA from './components/CTA';
import Footer from './components/Footer';

function App() {
  return (
    <div className="app">
      <Hero />
      <About />
      <Demos />
      <Team />
      <CTA />
      <Footer />
    </div>
  );
}

export default App;



