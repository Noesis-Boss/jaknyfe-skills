
// Scottish Rite Hero Component
const SRHero = () => {
  const [visible, setVisible] = React.useState(false);
  React.useEffect(() => { setTimeout(() => setVisible(true), 100); }, []);

  const scrollTo = (href) => {
    const el = document.querySelector(href);
    if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 72, behavior: 'smooth' });
  };

  return (
    <section id="hero" data-screen-label="Hero" style={{ position: 'relative', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden', background: 'var(--navy)' }}>
      {/* Animated geometric background */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', opacity: 0.18 }}>
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', inset: 0 }}>
          <defs>
            <pattern id="heroGrid" width="80" height="80" patternUnits="userSpaceOnUse">
              <path d="M40 0 L80 40 L40 80 L0 40 Z" fill="none" stroke="var(--gold)" strokeWidth="0.5"/>
              <circle cx="40" cy="40" r="3" fill="none" stroke="var(--gold)" strokeWidth="0.5"/>
            </pattern>
            <radialGradient id="heroVignette" cx="50%" cy="50%" r="60%">
              <stop offset="0%" stopColor="var(--navy)" stopOpacity="0"/>
              <stop offset="100%" stopColor="var(--navy)" stopOpacity="1"/>
            </radialGradient>
          </defs>
          <rect width="100%" height="100%" fill="url(#heroGrid)"/>
          <rect width="100%" height="100%" fill="url(#heroVignette)"/>
        </svg>
      </div>

      {/* Stars */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }} className="sr-stars">
        {Array.from({length: 60}).map((_, i) => (
          <div key={i} style={{
            position: 'absolute',
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            width: Math.random() > 0.85 ? 3 : 2,
            height: Math.random() > 0.85 ? 3 : 2,
            borderRadius: '50%',
            background: 'var(--gold)',
            opacity: 0.2 + Math.random() * 0.5,
            animation: `srTwinkle ${2 + Math.random() * 4}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 4}s`,
          }}/>
        ))}
      </div>

      {/* Ornamental ring */}
      <div style={{
        position: 'absolute', width: 480, height: 480,
        borderRadius: '50%',
        border: '1px solid rgba(184,149,58,0.15)',
        top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)',
        animation: 'srSpin 60s linear infinite',
      }}/>
      <div style={{
        position: 'absolute', width: 600, height: 600,
        borderRadius: '50%',
        border: '1px solid rgba(184,149,58,0.08)',
        top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)',
        animation: 'srSpin 90s linear infinite reverse',
      }}/>

      {/* Content */}
      <div style={{
        position: 'relative', zIndex: 2, textAlign: 'center',
        padding: '0 1.5rem', maxWidth: 760,
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(24px)',
        transition: 'opacity 1s ease, transform 1s ease',
      }}>
        <div style={{
          opacity: visible ? 1 : 0,
          transition: 'opacity 0.8s ease 0.2s',
        }}>
          <img src="uploads/logo-1776712250947.png" alt="Scottish Rite of Freemasonry, Valley of Tucson"
            style={{ width: '100%', maxWidth: 520, marginBottom: '2.5rem', filter: 'brightness(0) invert(1) sepia(1) saturate(0.5) brightness(1.1)' }}/>
        </div>

        <div style={{
          width: 60, height: 1, background: 'var(--gold)', margin: '0 auto 2rem',
          opacity: visible ? 1 : 0, transition: 'opacity 0.6s ease 0.6s, width 0.6s ease 0.6s',
        }}/>

        <p style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(1.1rem, 2.5vw, 1.4rem)',
          color: 'rgba(255,255,255,0.75)',
          letterSpacing: '0.12em',
          textTransform: 'uppercase',
          fontStyle: 'italic',
          margin: '0 0 2.5rem',
          fontWeight: 400,
          opacity: visible ? 1 : 0,
          transition: 'opacity 0.8s ease 0.8s',
        }}>
          Building Better Men Since 1882
        </p>

        <div style={{
          display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap',
          opacity: visible ? 1 : 0, transition: 'opacity 0.8s ease 1.1s',
        }}>
          <button onClick={() => scrollTo('#about')} style={{
            background: 'var(--gold)', color: 'var(--navy)',
            border: 'none', cursor: 'pointer',
            fontFamily: 'var(--font-body)', fontWeight: 700,
            fontSize: '0.82rem', letterSpacing: '0.1em', textTransform: 'uppercase',
            padding: '0.85rem 2.2rem', borderRadius: 4,
            transition: 'opacity 0.2s, transform 0.2s',
          }} onMouseOver={e => e.target.style.opacity='0.85'} onMouseOut={e => e.target.style.opacity='1'}>
            Discover Our Valley
          </button>
          <button onClick={() => scrollTo('#membership')} style={{
            background: 'transparent', color: '#fff',
            border: '1px solid rgba(255,255,255,0.4)', cursor: 'pointer',
            fontFamily: 'var(--font-body)', fontWeight: 600,
            fontSize: '0.82rem', letterSpacing: '0.1em', textTransform: 'uppercase',
            padding: '0.85rem 2.2rem', borderRadius: 4,
            transition: 'border-color 0.2s, background 0.2s',
          }} onMouseOver={e => { e.target.style.borderColor='var(--gold)'; e.target.style.background='rgba(184,149,58,0.1)'; }}
             onMouseOut={e => { e.target.style.borderColor='rgba(255,255,255,0.4)'; e.target.style.background='transparent'; }}>
            Become a Member
          </button>
        </div>
      </div>

      {/* Scroll indicator */}
      <div style={{
        position: 'absolute', bottom: '2rem', left: '50%', transform: 'translateX(-50%)',
        display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem',
        opacity: 0.5, animation: 'srBounce 2s ease-in-out infinite',
      }}>
        <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.7rem', letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)' }}>Scroll</span>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="var(--gold)" strokeWidth="1.5">
          <polyline points="2,5 8,11 14,5"/>
        </svg>
      </div>
    </section>
  );
};

Object.assign(window, { SRHero });
