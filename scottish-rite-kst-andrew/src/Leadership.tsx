import React from 'react'

const officers = [
  { rank: 'Venerable Master', name: 'Sir Knight Joseph Felix, 32° KSA' },
  { rank: 'Senior Warden', name: 'Hon. Gregory Johnson, 32° KCCH KSA' },
  { rank: 'Junior Warden', name: 'Hon. Jon M. Schmidt, 32° KCCH KSA' },
  { rank: 'Treasurer', name: 'Ill. Gerald Lankin, 33°' },
  { rank: 'Secretary', name: 'Bro. Joseph Felix, 32° KSA' },
  { rank: 'Chaplain', name: 'Bro. Michael Candela, 32° KSA' },
]

export const Leadership = () => {
  return (
    <section id="leadership" style={{ background: 'var(--navy)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
            letterSpacing: '0.2em', textTransform: 'uppercase',
            color: 'var(--gold)', marginBottom: '0.75rem',
          }}>Leadership</p>
          <h2 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2rem, 4vw, 2.8rem)',
            fontWeight: 600, color: '#fff', margin: '0 0 1rem', lineHeight: 1.15,
          }}>Officers of the Chapter</h2>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '1.05rem',
            color: 'rgba(255,255,255,0.45)', maxWidth: 480, margin: '0 auto', lineHeight: 1.7,
          }}>
            Led by Brothers who exemplify service, fidelity, and the chivalric virtues of the Order.
          </p>
          <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.5rem auto 0', borderRadius: 1 }} />
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '1.25rem',
        }}>
          {officers.slice(0, 3).map((o, i) => (
            <div key={i} style={{
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(184,149,58,0.2)',
              borderTop: '3px solid var(--gold)',
              borderRadius: 8, padding: '1.5rem',
              transition: 'background 0.25s, transform 0.25s',
            }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLElement).style.background = 'rgba(184,149,58,0.06)'
                (e.currentTarget as HTMLElement).style.transform = 'translateY(-3px)'
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.03)'
                (e.currentTarget as HTMLElement).style.transform = 'none'
              }}
            >
              <div style={{
                width: 48, height: 48, borderRadius: '50%',
                background: 'rgba(184,149,58,0.12)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                marginBottom: '1rem',
              }}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="var(--gold)" strokeWidth="1.5">
                  <circle cx="11" cy="8" r="4" />
                  <path d="M3 20c0-4 3.6-7 8-7s8 3 8 7" />
                </svg>
              </div>
              <p style={{
                fontFamily: 'var(--font-body)', fontSize: '0.7rem',
                letterSpacing: '0.1em', textTransform: 'uppercase',
                color: 'var(--gold)', margin: '0 0 0.35rem', fontWeight: 700,
              }}>{o.rank}</p>
              <p style={{
                fontFamily: 'var(--font-display)', fontSize: '1.05rem',
                fontWeight: 600, color: '#fff', margin: 0,
              }}>{o.name}</p>
            </div>
          ))}
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '1.25rem',
          marginTop: '1.25rem',
        }}>
          {officers.slice(3).map((o, i) => (
            <div key={i} style={{
              background: 'rgba(255,255,255,0.03)',
              border: '1px solid rgba(184,149,58,0.2)',
              borderTop: '3px solid var(--gold)',
              borderRadius: 8, padding: '1.5rem',
              transition: 'background 0.25s, transform 0.25s',
            }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLElement).style.background = 'rgba(184,149,58,0.06)'
                (e.currentTarget as HTMLElement).style.transform = 'translateY(-3px)'
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.03)'
                (e.currentTarget as HTMLElement).style.transform = 'none'
              }}
            >
              <div style={{
                width: 48, height: 48, borderRadius: '50%',
                background: 'rgba(184,149,58,0.12)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                marginBottom: '1rem',
              }}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="var(--gold)" strokeWidth="1.5">
                  <circle cx="11" cy="8" r="4" />
                  <path d="M3 20c0-4 3.6-7 8-7s8 3 8 7" />
                </svg>
              </div>
              <p style={{
                fontFamily: 'var(--font-body)', fontSize: '0.7rem',
                letterSpacing: '0.1em', textTransform: 'uppercase',
                color: 'var(--gold)', margin: '0 0 0.35rem', fontWeight: 700,
              }}>{o.rank}</p>
              <p style={{
                fontFamily: 'var(--font-display)', fontSize: '1.05rem',
                fontWeight: 600, color: '#fff', margin: 0,
              }}>{o.name}</p>
            </div>
          ))}
        </div>

        {/* Nine Virtues strip */}
        <div style={{
          marginTop: '3rem', padding: '2rem',
          background: 'rgba(45,106,79,0.1)',
          border: '1px solid rgba(45,106,79,0.2)',
          borderRadius: 8, textAlign: 'center',
        }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.72rem',
            letterSpacing: '0.15em', textTransform: 'uppercase',
            color: 'var(--gold)', marginBottom: '1rem', fontWeight: 700,
          }}>The Nine Virtues of a Knight of St. Andrew</p>
          <div style={{
            display: 'flex', flexWrap: 'wrap', justifyContent: 'center',
            gap: '0.6rem 1.5rem',
          }}>
            {['Patience', 'Self-Denial', 'Generosity', 'Compassion', 'Virtue', 'Honor', 'Truth', 'Loyalty', 'Courage'].map(v => (
              <span key={v} style={{
                fontFamily: 'var(--font-display)', fontSize: '0.9rem',
                color: '#fff', fontWeight: 500,
              }}>{v}</span>
            )).reduce<React.ReactNode[]>((acc, el, i) => {
              if (i > 0) acc.push(
                <span key={`sep-${i}`} style={{ color: 'var(--gold)', opacity: 0.4 }}>·</span>
              )
              acc.push(el)
              return acc
            }, [])}
          </div>
        </div>
      </div>
    </section>
  )
}
