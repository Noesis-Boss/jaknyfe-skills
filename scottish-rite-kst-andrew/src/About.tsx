import React from 'react'

export const About = () => {
  return (
    <section id="about" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
            letterSpacing: '0.2em', textTransform: 'uppercase',
            color: 'var(--green)', marginBottom: '0.75rem',
          }}>The Order</p>
          <h2 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2rem, 4vw, 2.8rem)',
            fontWeight: 600, color: 'var(--navy)', margin: '0 0 1rem', lineHeight: 1.15,
          }}>Knights of Saint Andrew</h2>
          <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.2rem auto', borderRadius: 1 }} />
        </div>

        <div style={{
          display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4rem',
          alignItems: 'center',
        }} className="ksa-two-col">
          <div>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '1.02rem',
              color: 'var(--text-body)', lineHeight: 1.8, marginBottom: '1.25rem',
            }}>
              The <strong>Knights of Saint Andrew</strong> (KSA) is an elite service organization within the Ancient & Accepted Scottish Rite of Freemasonry. Founded in 1993 by Ill. Weldon J. Good, 33°, the KSA was formed to rally "Black Hat" 32° Masons — those who have not yet received the Knight Commander Court of Honor — into active service and fellowship within their Valley.
            </p>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '1.02rem',
              color: 'var(--text-body)', lineHeight: 1.8, marginBottom: '1.25rem',
            }}>
              Inspired by the <strong>29th Degree — Scottish Knight of Saint Andrew</strong>, the order embodies the chivalric virtues of knighthood: patience, self-denial, generosity, compassion, virtue, and honor. Today, over 190 chapters across the Southern Jurisdiction and beyond carry forward this tradition of service.
            </p>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '1.02rem',
              color: 'var(--text-body)', lineHeight: 1.8,
            }}>
              In the <strong>Valley of Tucson</strong>, the KSA serves as a vital service arm — greeting candidates, staffing reunions, supporting degree work, escorting dignitaries, and standing as the Valley's official honor guard.
            </p>
          </div>

          {/* St. Andrew's Cross emblem card */}
          <div style={{
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            padding: '3rem',
          }}>
            <div style={{
              width: 300, height: 340,
              background: 'var(--navy)',
              borderRadius: 12,
              display: 'flex', flexDirection: 'column',
              alignItems: 'center', justifyContent: 'center',
              border: '1px solid rgba(184,149,58,0.25)',
              position: 'relative', overflow: 'hidden',
            }}>
              {/* Corner ornaments */}
              {['top-left','top-right','bottom-left','bottom-right'].map(corner => (
                <div key={corner} style={{
                  position: 'absolute',
                  top: corner.startsWith('top') ? 12 : 'auto',
                  bottom: corner.startsWith('bottom') ? 12 : 'auto',
                  left: corner.endsWith('left') ? 12 : 'auto',
                  right: corner.endsWith('right') ? 12 : 'auto',
                  width: 8, height: 8,
                  borderTop: corner.startsWith('top') ? '1px solid var(--gold)' : 'none',
                  borderBottom: corner.startsWith('bottom') ? '1px solid var(--gold)' : 'none',
                  borderLeft: corner.endsWith('left') ? '1px solid var(--gold)' : 'none',
                  borderRight: corner.endsWith('right') ? '1px solid var(--gold)' : 'none',
                }} />
              ))}

              {/* Saltire cross */}
              <svg width="100" height="100" viewBox="0 0 100 100" fill="none" style={{ marginBottom: '1.5rem' }}>
                <line x1="50" y1="8" x2="50" y2="92" stroke="var(--gold)" strokeWidth="4" />
                <line x1="8" y1="92" x2="92" y2="8" stroke="var(--gold)" strokeWidth="4" />
                <circle cx="50" cy="50" r="28" fill="none" stroke="rgba(184,149,58,0.3)" strokeWidth="1.5" />
                <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(184,149,58,0.12)" strokeWidth="0.8" />
              </svg>

              <p style={{
                fontFamily: 'var(--font-display)', fontSize: '1.1rem',
                color: 'var(--gold)', fontWeight: 600,
                letterSpacing: '0.08em', textAlign: 'center',
                marginBottom: '0.3rem',
              }}>KSA</p>
              <p style={{
                fontFamily: 'var(--font-body)', fontSize: '0.65rem',
                color: 'rgba(255,255,255,0.4)', letterSpacing: '0.18em',
                textTransform: 'uppercase', textAlign: 'center',
              }}>Valley of Tucson</p>
            </div>
          </div>
        </div>

        {/* Stats row */}
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: '1.5rem', marginTop: '4rem',
        }}>
          {[
            { value: '1993', label: 'Founded' },
            { value: '190+', label: 'Active Chapters' },
            { value: '29°', label: 'Inspiring Degree' },
            { value: 'Service', label: 'Our Mission' },
          ].map((s, i) => (
            <div key={i} style={{
              textAlign: 'center', padding: '1.5rem',
              background: '#fff', borderRadius: 8,
              border: '1px solid var(--card-border)',
            }}>
              <div style={{
                fontFamily: 'var(--font-display)', fontSize: '1.8rem',
                fontWeight: 700, color: 'var(--navy)', lineHeight: 1, marginBottom: '0.4rem',
              }}>{s.value}</div>
              <div style={{
                fontFamily: 'var(--font-body)', fontSize: '0.75rem',
                letterSpacing: '0.1em', textTransform: 'uppercase',
                color: 'var(--text-muted)', fontWeight: 600,
              }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
