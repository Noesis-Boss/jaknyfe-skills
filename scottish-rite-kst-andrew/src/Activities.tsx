import React from 'react'

const ActIcon = ({ d }: { d: string }) => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" stroke="var(--gold)" strokeWidth="1.8">
    <path d={d} />
  </svg>
)

export const Activities = () => {
  const activities = [
    {
      icon: 'M14 4v4M14 20v4M6 12h4M18 12h4',
      title: 'Reunion Support',
      text: 'Greeting candidates, registration, setup and signage, running errands, and staffing every department of the Reunion — Costume, Makeup, Props, Credentials, Kitchen, and more.',
    },
    {
      icon: 'M4 14h20M14 4v20',
      title: 'Honor Guard & Ceremonies',
      text: 'Serving as the Valley\'s official honor guard at installations, ring ceremonies, and public events. Presenting colors, escorting dignitaries, and forming arches of steel.',
    },
    {
      icon: 'M14 6l8 14H6z',
      title: 'Degree Exemplification',
      text: 'Exemplifying the 29th Degree — Knight of Saint Andrew — to new candidates. Bringing chivalric tradition to life through dramatic presentation.',
    },
    {
      icon: 'M6 14l6-8 6 8 4-6',
      title: 'Charity & Outreach',
      text: 'Raising funds for RiteCare childhood language programs, supporting community service projects, and participating in parades and civic activities across Southern Arizona.',
    },
    {
      icon: 'M14 4c5.5 0 10 4.5 10 10s-4.5 10-10 10S4 19.5 4 14M14 4v10l6 4',
      title: 'Mentorship & Fellowship',
      text: 'Guiding Squires — newer members — through the work of the Chapter before elevation to Knighthood. Fostering brotherhood among 32° Masons year-round.',
    },
    {
      icon: 'M4 20l6-6 4 4 10-12',
      title: 'Valley Operations',
      text: 'Assisting the General Secretary, supporting stated meetings, maintaining the Temple, and stepping in wherever hands are needed. No task too small, no call unanswered.',
    },
  ]

  return (
    <section id="activities" style={{ background: 'var(--green-deep)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
            letterSpacing: '0.2em', textTransform: 'uppercase',
            color: 'var(--gold)', marginBottom: '0.75rem',
          }}>What We Do</p>
          <h2 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2rem, 4vw, 2.8rem)',
            fontWeight: 600, color: '#fff', margin: '0 0 1rem', lineHeight: 1.15,
          }}>Our Mission in Action</h2>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '1.05rem',
            color: 'rgba(255,255,255,0.5)', maxWidth: 560, margin: '0 auto', lineHeight: 1.7,
          }}>
            From Reunion service to community outreach, the KSA is the working heart of the Valley.
          </p>
          <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.5rem auto 0', borderRadius: 1 }} />
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '1.5rem',
        }}>
          {activities.map((a, i) => (
            <div key={i} style={{
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: 8, padding: '2rem 1.5rem',
              transition: 'transform 0.25s, background 0.25s',
            }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLElement).style.transform = 'translateY(-4px)'
                (e.currentTarget as HTMLElement).style.background = 'rgba(184,149,58,0.08)'
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLElement).style.transform = 'none'
                (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.04)'
              }}
            >
              <div style={{
                width: 52, height: 52, borderRadius: '50%',
                background: 'rgba(184,149,58,0.12)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                marginBottom: '1.25rem',
              }}>
                <svg width="26" height="26" viewBox="0 0 28 28" fill="none" stroke="var(--gold)" strokeWidth="1.8">
                  <path d={a.icon} />
                </svg>
              </div>
              <h3 style={{
                fontFamily: 'var(--font-display)', fontSize: '1.2rem',
                fontWeight: 600, color: '#fff', margin: '0 0 0.75rem',
              }}>{a.title}</h3>
              <p style={{
                fontFamily: 'var(--font-body)', fontSize: '0.92rem',
                color: 'rgba(255,255,255,0.5)', lineHeight: 1.7, margin: 0,
              }}>{a.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
