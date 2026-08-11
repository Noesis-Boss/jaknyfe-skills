import React from 'react'

export const Footer = () => {
  const logo = `${import.meta.env.BASE_URL}ksa-logo.png`
  return (
    <footer style={{
      background: 'var(--navy)', padding: '3rem 1.5rem 2rem',
      borderTop: '1px solid rgba(184,149,58,0.15)',
    }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        {/* Logo divider */}
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <img src={logo} alt="Knights of St. Andrew" style={{ width: 60, height: 'auto', opacity: 0.5 }} />
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: '2fr 1fr 1fr',
          gap: '3rem', marginBottom: '2.5rem',
        }}>
          {/* About column */}
          <div>
            <h4 style={{
              fontFamily: 'var(--font-display)', fontSize: '1.1rem',
              color: '#fff', margin: '0 0 1rem', fontWeight: 600,
            }}>Knights of St. Andrew</h4>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '0.88rem',
              color: 'rgba(255,255,255,0.4)', lineHeight: 1.65, margin: 0,
            }}>
              An elite service organization of 32° Scottish Rite Masons in the Valley of Tucson, dedicated to service, leadership, and the chivalric virtues of the 29th Degree.
            </p>
          </div>

          {/* Links column */}
          <div>
            <h4 style={{
              fontFamily: 'var(--font-body)', fontSize: '0.72rem',
              fontWeight: 700, letterSpacing: '0.15em',
              textTransform: 'uppercase', color: 'var(--gold)', margin: '0 0 1rem',
            }}>Quick Links</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {[
                { label: 'About the KSA', href: '#about' },
                { label: 'The Nine Virtues', href: '#virtues' },
                { label: 'Our History', href: '#history' },
                { label: 'Activities', href: '#activities' },
                { label: 'Join the Order', href: '#join' },
              ].map(link => (
                <a key={link.href} href={link.href} style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.88rem',
                  color: 'rgba(255,255,255,0.45)', textDecoration: 'none',
                  transition: 'color 0.2s',
                }}
                  onMouseEnter={e => (e.target as HTMLElement).style.color = 'var(--gold)'}
                  onMouseLeave={e => (e.target as HTMLElement).style.color = 'rgba(255,255,255,0.45)'}
                >{link.label}</a>
              ))}
            </div>
          </div>

          {/* Contact column */}
          <div>
            <h4 style={{
              fontFamily: 'var(--font-body)', fontSize: '0.72rem',
              fontWeight: 700, letterSpacing: '0.15em',
              textTransform: 'uppercase', color: 'var(--gold)', margin: '0 0 1rem',
            }}>Contact</h4>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '0.88rem',
              color: 'rgba(255,255,255,0.45)', lineHeight: 1.65, margin: '0 0 0.5rem',
            }}>
              Valley of Tucson<br />
              Scottish Rite Cathedral<br />
              160 S Scott Ave<br />
              Tucson, AZ 85701
            </p>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '0.88rem',
              color: 'rgba(255,255,255,0.45)', margin: '0.5rem 0 0',
            }}>
              <a href="mailto:ksa@tucsonscottishrite.org" style={{
                color: 'var(--gold)', textDecoration: 'none',
              }}>ksa@tucsonscottishrite.org</a>
            </p>
          </div>
        </div>

        {/* Bottom bar */}
        <div style={{
          borderTop: '1px solid rgba(255,255,255,0.06)',
          paddingTop: '1.5rem',
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          flexWrap: 'wrap', gap: '1rem',
        }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.78rem',
            color: 'rgba(255,255,255,0.25)', margin: 0,
          }}>
            © {new Date().getFullYear()} Knights of St. Andrew — Valley of Tucson. All rights reserved.
          </p>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.78rem',
            color: 'rgba(255,255,255,0.25)', margin: 0,
          }}>
            Ancient & Accepted Scottish Rite · Orient of Arizona · Southern Jurisdiction
          </p>
        </div>
      </div>
    </footer>
  )
}
