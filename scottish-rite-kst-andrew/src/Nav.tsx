import React from 'react'

export const Nav = () => {
  const [scrolled, setScrolled] = React.useState(false)
  const [menuOpen, setMenuOpen] = React.useState(false)

  React.useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60)
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const links = [
    { href: '#about', label: 'About' },
    { href: '#virtues', label: 'Virtues' },
    { href: '#history', label: 'History' },
    { href: '#activities', label: 'Activities' },
    { href: '#leadership', label: 'Leadership' },
    { href: '#join', label: 'Join' },
  ]

  const scrollTo = (href: string) => {
    setMenuOpen(false)
    const el = document.querySelector(href)
    if (el) window.scrollTo({ top: (el as HTMLElement).offsetTop - 72, behavior: 'smooth' })
  }

  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000,
      background: scrolled ? 'rgba(10,22,40,0.97)' : 'transparent',
      borderBottom: scrolled ? '1px solid rgba(184,149,58,0.2)' : 'none',
      transition: 'background 0.3s, border-bottom 0.3s',
      backdropFilter: scrolled ? 'blur(12px)' : 'none',
    }}>
      <div style={{
        maxWidth: 1100, margin: '0 auto',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: '0.9rem 1.5rem',
      }}>
        <a href="#" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} style={{
          textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.6rem',
        }}>
          <img src="/ksa-logo.png" alt="KSA" style={{ width: 28, height: 28, objectFit: 'contain' }} />
          <span style={{
            fontFamily: 'var(--font-display)', fontSize: '1rem', fontWeight: 700,
            color: '#fff', letterSpacing: '0.04em',
          }}>Tucson KSA</span>
        </a>

        <div style={{
          display: 'flex', gap: '2rem', alignItems: 'center',
        }} className="ksa-nav-links">
          {links.map(l => (
            <a key={l.href} href={l.href} onClick={e => { e.preventDefault(); scrollTo(l.href) }} style={{
              fontFamily: 'var(--font-body)', fontSize: '0.78rem', fontWeight: 600,
              letterSpacing: '0.1em', textTransform: 'uppercase',
              color: 'rgba(255,255,255,0.7)', textDecoration: 'none',
              transition: 'color 0.2s',
            }}
              onMouseEnter={e => (e.target as HTMLElement).style.color = 'var(--gold)'}
              onMouseLeave={e => (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.7)'}
            >{l.label}</a>
          ))}
        </div>

        <button onClick={() => setMenuOpen(!menuOpen)} style={{
          display: 'none', background: 'none', border: 'none', cursor: 'pointer',
        }} className="ksa-menu-btn">
          <svg width="24" height="24" fill="none" stroke="#fff" strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>
      </div>

      {menuOpen && (
        <div style={{
          background: 'var(--navy)', padding: '1rem 1.5rem',
          display: 'flex', flexDirection: 'column', gap: '1rem',
        }}>
          {links.map(l => (
            <a key={l.href} href={l.href} onClick={e => { e.preventDefault(); scrollTo(l.href) }} style={{
              fontFamily: 'var(--font-body)', fontSize: '0.85rem', fontWeight: 600,
              color: 'rgba(255,255,255,0.8)', textDecoration: 'none',
            }}>{l.label}</a>
          ))}
        </div>
      )}
    </nav>
  )
}
