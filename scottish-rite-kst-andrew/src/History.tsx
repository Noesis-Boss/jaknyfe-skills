import React from 'react'

export const History = () => {
  const milestones = [
    {
      year: '1993',
      title: 'The Vision',
      text: 'Ill. Weldon J. Good, 33°, establishes the first Knights of Saint Andrew chapter in Tulsa, Oklahoma, to give "Black Hat" 32° Masons a structured path for active service and fellowship within their Valley.',
    },
    {
      year: '1993–2000',
      title: 'Early Growth',
      text: 'The concept spreads rapidly across the Southern Jurisdiction. Valleys recognize the KSA\'s value in staffing reunions, assisting secretaries, and energizing newer members. Chapters adopt their own by-laws, rituals, and tartan colors.',
    },
    {
      year: '2000–2010',
      title: 'National Expansion',
      text: 'Over 100 chapters are chartered. KSA units appear at major Scottish Rite events as honor guards with distinctive Glengarry hats, tartan ties, and bagpipe corps. The Guthrie Scottish & Medieval Festival becomes a signature KSA event.',
    },
    {
      year: '2010–2020',
      title: 'Modern Era',
      text: 'The KSA evolves beyond reunion support into year-round service: charity drives, RiteCare fundraising, community outreach, degree work exemplification (especially the 29th Degree), and mentorship programs for newer Masons.',
    },
    {
      year: '2020–Present',
      title: 'The Tucson Chapter',
      text: 'The Valley of Tucson\'s KSA chapter carries forward the tradition — greeting candidates, supporting reunions, escorting dignitaries, presenting colors, and standing as the Valley\'s official service and honor guard.',
    },
  ]

  return (
    <section id="history" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
            letterSpacing: '0.2em', textTransform: 'uppercase',
            color: 'var(--green)', marginBottom: '0.75rem',
          }}>Our Story</p>
          <h2 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2rem, 4vw, 2.8rem)',
            fontWeight: 600, color: 'var(--navy)', margin: '0 0 1rem', lineHeight: 1.15,
          }}>History of the Order</h2>
          <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.2rem auto 0', borderRadius: 1 }} />
        </div>

        {/* Timeline */}
        <div style={{ position: 'relative', paddingLeft: '3rem' }}>
          {/* Vertical line */}
          <div style={{
            position: 'absolute', left: 14, top: 0, bottom: 0,
            width: 2, background: 'linear-gradient(to bottom, var(--gold), var(--green), rgba(184,149,58,0.2))',
          }} />

          {milestones.map((m, i) => (
            <div key={i} style={{
              position: 'relative', marginBottom: i === milestones.length - 1 ? 0 : '3rem',
            }}>
              {/* Dot */}
              <div style={{
                position: 'absolute', left: '-3rem', top: 4,
                width: 12, height: 12, borderRadius: '50%',
                background: i === milestones.length - 1 ? 'var(--green-light)' : 'var(--gold)',
                border: '2px solid var(--cream)',
                boxShadow: `0 0 0 3px ${i === milestones.length - 1 ? 'rgba(45,106,79,0.3)' : 'rgba(184,149,58,0.3)'}`,
              }} />

              <div style={{
                background: '#fff', borderRadius: 8,
                padding: '1.5rem 1.75rem',
                border: '1px solid var(--card-border)',
                transition: 'transform 0.2s, box-shadow 0.2s',
              }}
                onMouseEnter={e => {
                  (e.currentTarget as HTMLElement).style.transform = 'translateY(-3px)'
                  (e.currentTarget as HTMLElement).style.boxShadow = '0 8px 24px rgba(0,0,0,0.08)'
                }}
                onMouseLeave={e => {
                  (e.currentTarget as HTMLElement).style.transform = 'none'
                  (e.currentTarget as HTMLElement).style.boxShadow = 'none'
                }}
              >
                <div style={{
                  fontFamily: 'var(--font-display)', fontSize: '1.3rem',
                  fontWeight: 700, color: i === milestones.length - 1 ? 'var(--green)' : 'var(--gold)',
                  marginBottom: '0.35rem',
                }}>{m.year}</div>
                <h3 style={{
                  fontFamily: 'var(--font-display)', fontSize: '1.2rem',
                  fontWeight: 600, color: 'var(--navy)', margin: '0 0 0.6rem',
                }}>{m.title}</h3>
                <p style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.95rem',
                  color: 'var(--text-body)', lineHeight: 1.7, margin: 0,
                }}>{m.text}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
