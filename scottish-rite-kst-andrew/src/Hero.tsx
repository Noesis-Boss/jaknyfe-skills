import React from 'react'

export const Hero = () => {
  const [visible, setVisible] = React.useState(false)
  React.useEffect(() => { setTimeout(() => setVisible(true), 100) }, [])

  return (
    <section style={{
      position: 'relative', minHeight: '100vh',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      overflow: 'hidden', background: 'var(--navy)',
    }}>
      {/* Animated background with moving constellations */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
        <svg width="100%" height="100%" style={{ opacity: 0.15 }}>
          <defs>
            <radialGradient id="starGlow" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="#fff" stopOpacity="0" />
              <stop offset="70%" stopColor="#fff" stopOpacity="0.3" />
              <stop offset="100%" stopColor="#fff" stopOpacity="0" />
            </radialGradient>
          </defs>
          {/* Animated stars */}
          {[...Array(25)].map((_, i) => (
            <circle
              key={i}
              cx={`${Math.random() * 100}%`}
              cy={`${Math.random() * 100}%`}
              r={`${0.3 + Math.random() * 1.5}px`}
              fill="#fff"
              opacity={`${0.3 + Math.random() * 0.7}`}
              style={{
                animation: `twinkle ${3 + Math.random() * 4}s ease-in-out infinite`,
                animationDelay: `${Math.random() * 5}s`,
              }}
            />
          ))}
          {/* Moving constellation lines */}
          <path
            d="M10,20 L30,40 L50,30 L70,60 L90,20"
            stroke="var(--gold)"
            strokeWidth="0.5"
            fill="none"
            opacity="0.2"
            style={{
              animation: `constellationMove 8s linear infinite`,
            }}
          />
        </svg>
      </div>

      {/* Animated saltire grid */}
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', opacity: 0.06 }}>
        <svg width="100%" height="100%">
          <defs>
            <pattern id="saltireGrid" width="120" height="120" patternUnits="userSpaceOnUse">
              <line x1="0" y1="120" x2="120" y2="0" stroke="var(--gold)" strokeWidth="0.5" />
              <line x1="0" y1="60" x2="60" y2="0" stroke="var(--green-light)" strokeWidth="0.3" />
              <circle cx="60" cy="60" r="4" fill="none" stroke="var(--gold)" strokeWidth="0.4" />
            </pattern>
            <radialGradient id="heroVignette" cx="50%" cy="50%" r="60%">
              <stop offset="0%" stopColor="var(--navy)" stopOpacity="0" />
              <stop offset="100%" stopColor="var(--navy)" stopOpacity="1" />
            </radialGradient>
          </defs>
          <rect width="100%" height="100%" fill="url(#saltireGrid)" />
          <rect width="100%" height="100%" fill="url(#heroVignette)" />
        </svg>
      </div>

      {/* Floating cross particles */}
      {Array.from({ length: 18 }).map((_, i) => (
        <div key={i} style={{
          position: 'absolute',
          left: `${10 + Math.random() * 80}%`,
          top: `${10 + Math.random() * 80}%`,
          opacity: 0.08 + Math.random() * 0.15,
          animation: `breathe ${4 + Math.random() * 6}s ease-in-out infinite`,
          animationDelay: `${Math.random() * 5}s`,
        }}>
          <svg width={14 + Math.random() * 14} height={14 + Math.random() * 14} viewBox="0 0 28 28" fill="none" stroke="var(--gold)" strokeWidth="1.5" style={{ transform: 'rotate(45deg)' }}>
            <line x1="14" y1="2" x2="14" y2="26" />
            <line x1="2" y1="26" x2="26" y2="2" />
          </svg>
        </div>
      ))}

      {/* Ornamental rings */}
      <div style={{
        position: 'absolute', width: 420, height: 420, borderRadius: '50%',
        border: '1px solid rgba(184,149,58,0.12)', top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)', animation: 'spin 80s linear infinite',
      }} />
      <div style={{
        position: 'absolute', width: 540, height: 540, borderRadius: '50%',
        border: '1px solid rgba(45,106,79,0.1)', top: '50%', left: '50%',
        transform: 'translate(-50%, -50%)', animation: 'spin 120s linear infinite reverse',
      }} />

      {/* Content */}
      <div style={{
        position: 'relative', zIndex: 2, textAlign: 'center',
        padding: '0 1.5rem', maxWidth: 800,
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(24px)',
        transition: 'opacity 1s ease, transform 1s ease',
      }}>
        {/* Logo with subtle glow */}
        <div style={{
          margin: '0 auto 2rem',
          opacity: visible ? 1 : 0, transition: 'opacity 0.8s ease 0.3s',
          animation: 'floatCross 6s ease-in-out infinite',
          filter: 'drop-shadow(0 0 8px rgba(184,149,58,0.3))',
        }}>
          <img
            src="/ksa-logo.png"
            alt="Knights of St. Andrew Logo"
            style={{ width: '100%', maxWidth: 180, height: 'auto', display: 'block', margin: '0 auto' }}
          />
        </div>

        <p style={{
          fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
          letterSpacing: '0.25em', textTransform: 'uppercase',
          color: 'var(--green-light)', marginBottom: '1.2rem',
          opacity: visible ? 1 : 0, transition: 'opacity 0.8s ease 0.4s',
        }}>
          Valley of Tucson · Orient of Arizona
        </p>

        <h1 style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(2.4rem, 6vw, 4.2rem)',
          fontWeight: 700, color: '#fff', lineHeight: 1.1,
          marginBottom: '1rem',
          opacity: visible ? 1 : 0, transition: 'opacity 0.8s ease 0.5s',
          position: 'relative',
        }}>
          Knights of<br />
          <span style={{
            background: 'linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 50%, var(--gold) 100%)',
            backgroundSize: '200% auto',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
            animation: 'shimmer 4s linear infinite',
            position: 'relative',
          }}>
            Saint Andrew
          </span>
          {/* Animated highlight effect */}
          <span style={{
            position: 'absolute',
            bottom: '-4px',
            left: '0',
            width: '100%',
            height: '4px',
            background: 'linear-gradient(90deg, transparent, var(--gold), transparent)',
            backgroundSize: '200% 100%',
            animation: 'highlightMove 3s ease-in-out infinite',
          }}></span>
        </h1>

        <div style={{
          width: 60, height: 1.5, background: 'var(--gold)',
          margin: '1.5rem auto',
          opacity: visible ? 1 : 0, transition: 'opacity 0.6s ease 0.7s',
        }} />

        <p style={{
          fontFamily: 'var(--font-display)', fontSize: 'clamp(1rem, 2.2vw, 1.3rem)',
          color: 'rgba(255,255,255,0.65)', fontStyle: 'italic',
          letterSpacing: '0.06em', lineHeight: 1.6,
          maxWidth: 560, margin: '0 auto 2.5rem',
          opacity: visible ? 1 : 0, transition: 'opacity 0.8s ease 0.9s',
        }}>
          \"Love of God, loyalty to superiors, faithful adherence to promise,<br />
          and active resistance to unfair judgment\"
        </p>

        <div style={{
          display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap',
          opacity: visible ? 1 : 0, transition: 'opacity 0.8s ease 1.1s',
        }}>
          <a href="#about" onClick={e => {
            e.preventDefault()
            const el = document.querySelector('#about')
            if (el) window.scrollTo({ top: (el as HTMLElement).offsetTop - 72, behavior: 'smooth' })
          }} style={{
            background: 'var(--gold)', color: 'var(--navy)',
            border: 'none', cursor: 'pointer', textDecoration: 'none',
            fontFamily: 'var(--font-body)', fontWeight: 700,
            fontSize: '0.82rem', letterSpacing: '0.1em', textTransform: 'uppercase',
            padding: '0.85rem 2.2rem', borderRadius: 4,
            transition: 'opacity 0.2s, transform 0.2s, box-shadow 0.2s',
            display: 'inline-block',
            position: 'relative',
            overflow: 'hidden',
          }}
            onMouseEnter={e => { 
              (e.target as HTMLElement).style.opacity = '0.85'; 
              (e.target as HTMLElement).style.transform = 'translateY(-2px)';
              (e.target as HTMLElement).style.boxShadow = '0 4px 12px rgba(184,149,58,0.3)';
            }}
            onMouseLeave={e => { 
              (e.target as HTMLElement).style.opacity = '1'; 
              (e.target as HTMLElement).style.transform = 'none';
              (e.target as HTMLElement).style.boxShadow = 'none';
            }}
          >
            Discover the Order
            <span style={{
              position: 'absolute',
              top: '-50%',
              left: '-50%',
              width: '200%',
              height: '200%',
              background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%)',
              transform: 'translate(-50%, -50%)',
              animation: 'pulse 2s ease-in-out infinite',
            }}></span>
          </a>
          <a href="#join" onClick={e => {
            e.preventDefault()
            const el = document.querySelector('#join')
            if (el) window.scrollTo({ top: (el as HTMLElement).offsetTop - 72, behavior: 'smooth' })
          }} style={{
            background: 'transparent', color: '#fff',
            border: '1px solid rgba(255,255,255,0.4)', cursor: 'pointer', textDecoration: 'none',
            fontFamily: 'var(--font-body)', fontWeight: 600,
            fontSize: '0.82rem', letterSpacing: '0.1em', textTransform: 'uppercase',
            padding: '0.85rem 2.2rem', borderRadius: 4,
            transition: 'border-color 0.2s, background 0.2s, box-shadow 0.2s',
            display: 'inline-block',
            position: 'relative',
            overflow: 'hidden',
          }}
            onMouseEnter={e => { 
              (e.target as HTMLElement).style.borderColor = 'var(--gold)'; 
              (e.target as HTMLElement).style.background = 'rgba(184,149,58,0.1)';
              (e.target as HTMLElement).style.boxShadow = '0 4px 12px rgba(184,149,58,0.2)';
            }}
            onMouseLeave={e => { 
              (e.target as HTMLElement).style.borderColor = 'rgba(255,255,255,0.4)'; 
              (e.target as HTMLElement).style.background = 'transparent';
              (e.target as HTMLElement).style.boxShadow = 'none';
            }}
          >
            Petition to Join
            <span style={{
              position: 'absolute',
              top: '-50%',
              left: '-50%',
              width: '200%',
              height: '200%',
              background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%)',
              transform: 'translate(-50%, -50%)',
              animation: 'pulse 2s ease-in-out infinite',
              animationDelay: '1s',
            }}></span>
          </a>
        </div>

        {/* Animated scroll indicator */}
        <div style={{
          position: 'absolute', bottom: '2rem', left: '50%', transform: 'translateX(-50%)',
          display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem',
          opacity: 0.4, animation: 'pulse 2s ease-in-out infinite',
        }}>
          <span style={{
            fontFamily: 'var(--font-body)', fontSize: '0.65rem',
            letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)',
          }}>Scroll</span>
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="var(--gold)" strokeWidth="1.5">
            <polyline points="2,5 8,11 14,5" />
          </svg>
        </div>
      </div>
    </section>
  )
}
