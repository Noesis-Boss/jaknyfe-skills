import React from 'react';
import { createRoot } from 'react-dom/client';
import { SRNav } from './components/sr-nav';
import { SRHero } from './components/sr-hero';
import { SRAbout, SRDegrees, SREvents } from './sr-sections';
import { SROfficers, SRGallery, SRNews } from './components/sr-people';
import { SRMembership, SRDonate, SRContact } from './components/sr-contact';

const App = () => (
  <>
    <SRNav />
    <SRHero />
    <SRAbout />
    <SRDegrees />
    <SREvents />
    <SROfficers />
    <SRGallery />
    <SRNews />
    <SRMembership />
    <SRDonate />
    <SRContact />
    <footer style={{ background: 'var(--navy)', borderTop: '1px solid rgba(184,149,58,0.2)', padding: '3rem 1.5rem 2rem', textAlign: 'center' }}>
      <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.78rem', color: 'rgba(255,255,255,0.3)', margin: 0 }}>
        © {new Date().getFullYear()} Scottish Rite of Freemasonry, Valley of Tucson — Orient of Arizona
      </p>
      <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.78rem', color: 'rgba(255,255,255,0.25)', margin: '0.5rem 0 0' }}>Deus Meumque Jus</p>
    </footer>
  </>
);

const rootEl = document.getElementById('root');
if (rootEl) {
  const root = createRoot(rootEl);
  root.render(<App />);
} else {
  document.body.innerHTML = '<div style="padding:2rem; font-family: system-ui; color: red;">Scottish Rite: root element not found</div>';
}