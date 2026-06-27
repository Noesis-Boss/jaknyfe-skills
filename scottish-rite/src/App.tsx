import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import { SRHero } from '../components/sr-hero.jsx';
import { SRAbout } from '../components/sr-sections.jsx';
import { SRDegrees } from '../components/sr-sections.jsx';
import { SREvents } from '../components/sr-sections.jsx';
import { SROfficers } from '../components/sr-people.jsx';
import { SRGallery } from '../components/sr-people.jsx';
import { SRNews } from '../components/sr-people.jsx';
import { SRNav } from '../components/sr-nav.jsx';

const App = () => {
  return (
    <div className="App">
      <SRNav />
      <main>
        <SRHero />
        <SRAbout />
        <SRDegrees />
        <SREvents />
        <SROfficers />
        <SRGallery />
        <SRNews />
      </main>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
export default App;