
// Scottish Rite Nav Component
const SRNav = ({ theme }) => {
  const [scrolled, setScrolled] = React.useState(false);
  const [menuOpen, setMenuOpen] = React.useState(false);

  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const links = [
    { label: 'About', href: '#about' },
    { label: 'Degrees', href: '#degrees' },
    { label: 'Events', href: '#events' },
    { label: 'Officers', href: '#officers' },
    { label: 'Gallery', href: '#gallery' },
    { label: 'News', href: '#news' },
    { label: 'Join', href: '#membership' },
    { label: 'Contact', href: '#contact' },
  ];

  const scrollTo = (e, href) => {
    e.preventDefault();
    setMenuOpen(false);
    const el = document.querySelector(href);
    if (el) {
      const top = el.getBoundingClientRect().top + window.scrollY - 72;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  };

  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000,
      background: scrolled ? 'var(--nav-bg)' : 'transparent',
      boxShadow: scrolled ? '0 2px 20px rgba(0,0,0,0.18)' : 'none',
      transition: 'background 0.4s ease, box-shadow 0.4s ease',
      backdropFilter: scrolled ? 'blur(12px)' : 'none',
    }}>
      <div style={{
        maxWidth: 1200, margin: '0 auto',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0 2rem', height: 72,
      }}>
        {/* Logo mark */}
        <a href="#hero" onClick={e => scrollTo(e, '#hero')} style={{
          display: 'flex', alignItems: 'center', gap: '0.75rem',
          textDecoration: 'none',
        }}>
          <img src="uploads/logo-1776712250947.png" alt="Scottish Rite" style={{ height: 44, width: 'auto' }} />
        </a>

        {/* Desktop links */}
        <ul style={{
          display: 'flex', gap: '0.15rem', listStyle: 'none', margin: 0, padding: 0,
          '@media(max-width:768px)': { display: 'none' },
        }} className="sr-desktop-nav">
          {links.map(l => (
            <li key={l.href}>
              <a href={l.href} onClick={e => scrollTo(e, l.href)} style={{
                color: scrolled ? 'var(--nav-link)' : 'rgba(255,255,255,0.92)',
                textDecoration: 'none',
                fontFamily: 'var(--font-body)',
                fontSize: '0.82rem',
                fontWeight: 600,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
                padding: '0.4rem 0.65rem',
                borderRadius: 4,
                transition: 'color 0.2s, background 0.2s',
              }} className="sr-nav-link">
                {l.label}
              </a>
            </li>
          ))}
          <li>
            <a href="#donate" onClick={e => scrollTo(e, '#donate')} style={{
              marginLeft: '0.5rem',
              background: 'var(--gold)',
              color: 'var(--navy)',
              textDecoration: 'none',
              fontFamily: 'var(--font-body)',
              fontSize: '0.82rem',
              fontWeight: 700,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              padding: '0.5rem 1.1rem',
              borderRadius: 4,
              transition: 'opacity 0.2s',
            }}>
              Donate
            </a>
          </li>
        </ul>

        {/* Hamburger */}
        <button
          className="sr-hamburger"
          onClick={() => setMenuOpen(m => !m)}
          style={{
            display: 'none', background: 'none', border: 'none', cursor: 'pointer',
            color: scrolled ? 'var(--nav-link)' : '#fff', padding: '0.5rem',
          }}>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            {menuOpen
              ? <><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></>
              : <><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></>
            }
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div style={{
          background: 'var(--nav-bg)',
          borderTop: '1px solid rgba(255,255,255,0.1)',
          padding: '1rem 2rem 1.5rem',
        }}>
          {[...links, { label: 'Donate', href: '#donate' }].map(l => (
            <a key={l.href} href={l.href} onClick={e => scrollTo(e, l.href)} style={{
              display: 'block', color: 'var(--nav-link)', textDecoration: 'none',
              fontFamily: 'var(--font-body)', fontSize: '0.9rem', fontWeight: 600,
              letterSpacing: '0.06em', textTransform: 'uppercase',
              padding: '0.65rem 0', borderBottom: '1px solid rgba(255,255,255,0.07)',
            }}>
              {l.label}
            </a>
          ))}
        </div>
      )}
    </nav>
  );
};

Object.assign(window, { SRNav });
