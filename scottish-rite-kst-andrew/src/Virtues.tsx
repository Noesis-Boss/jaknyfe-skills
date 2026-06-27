import React from 'react'

export const Virtues = () => {
  const [active, setActive] = React.useState<number | null>(null)

  const virtues = [
    {
      title: 'Patience',
      icon: '⏳',
      text: 'The Knight endures trials with steadfast resolve, knowing that wisdom comes through perseverance and measured action.',
    },
    {
      title: 'Self-Denial',
      icon: '🛡',
      text: 'Placing duty above personal desire, the Knight sacrifices comfort for the greater good of his Brethren and community.',
    },
    {
      title: 'Generosity',
      icon: '🤝',
      text: 'A willing heart gives freely — time, talent, and treasure — without expectation of recognition or reward.',
    },
    {
      title: 'Compassion',
      icon: '❤',
      text: 'The Knight sees suffering and moves toward it, offering relief and comfort to all who are in need.',
    },
    {
      title: 'Virtue',
      icon: '✦',
      text: 'Moral excellence is not an endpoint but a daily practice. The Knight strives to walk uprightly before God and man.',
    },
    {
      title: 'Honor',
      icon: '⚔',
      text: 'A Knight\'s word is his bond, his name his most sacred possession. Honor governs every thought, word, and deed.',
    },
    {
      title: 'Loyalty',
      icon: '⚜',
      text: 'Fidelity to God, country, family, and the Fraternity. The Knight remains true even when tested or forsaken.',
    },
    {
      title: 'Truth',
      icon: '☩',
      text: 'The Knight resists unfair judgment and champions honest dealing, believing that truth is the foundation of all virtue.',
    },
    {
      title: 'Service',
      icon: '⚒',
      text: 'Above all, the Knight serves — his Valley, his Brethren, and his community — with humility and willing hands.',
    },
  ]

  return (
    <section id="virtues" style={{ background: 'var(--navy)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
            letterSpacing: '0.2em', textTransform: 'uppercase',
            color: 'var(--green-light)', marginBottom: '0.75rem',
          }}>The Nine Virtues</p>
          <h2 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2rem, 4vw, 2.8rem)',
            fontWeight: 600, color: '#fff', margin: '0 0 1rem', lineHeight: 1.15,
          }}>Virtues of a Knight</h2>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '1.05rem',
            color: 'rgba(255,255,255,0.55)', maxWidth: 560, margin: '0 auto', lineHeight: 1.7,
          }}>
            Drawn from the 29th Degree and the chivalric tradition, these nine virtues define every Knight of Saint Andrew.
          </p>
          <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.5rem auto 0', borderRadius: 1 }} />
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1.25rem',
        }}>
          {virtues.map((v, i) => (
            <div key={i}
              onClick={() => setActive(active === i ? null : i)}
              style={{
                background: active === i ? 'rgba(45,106,79,0.15)' : 'rgba(255,255,255,0.03)',
                border: `1px solid ${active === i ? 'var(--green-light)' : 'rgba(255,255,255,0.08)'}`,
                borderRadius: 8, padding: '1.5rem', cursor: 'pointer',
                transition: 'all 0.3s',
                borderTop: active === i ? '2px solid var(--gold)' : '2px solid transparent',
              }}
              onMouseEnter={e => {
                if (active !== i) {
                  (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.06)'
                  (e.currentTarget as HTMLElement).style.transform = 'translateY(-3px)'
                }
              }}
              onMouseLeave={e => {
                if (active !== i) {
                  (e.currentTarget as HTMLElement).style.background = 'rgba(255,255,255,0.03)'
                  (e.currentTarget as HTMLElement).style.transform = 'none'
                }
              }}
            >
              <div style={{
                fontSize: '1.6rem', marginBottom: '0.75rem',
                filter: active === i ? 'grayscale(0)' : 'grayscale(0.3)',
                transition: 'filter 0.3s',
              }}>{v.icon}</div>
              <h3 style={{
                fontFamily: 'var(--font-display)', fontSize: '1.15rem',
                fontWeight: 600, color: '#fff', margin: '0 0 0.5rem',
              }}>{v.title}</h3>
              <p style={{
                fontFamily: 'var(--font-body)', fontSize: '0.88rem',
                color: 'rgba(255,255,255,0.5)', lineHeight: 1.6, margin: 0,
                maxHeight: active === i ? 200 : 0, overflow: 'hidden',
                transition: 'max-height 0.4s ease, opacity 0.3s',
                opacity: active === i ? 1 : 0,
              }}>{v.text}</p>
              <div style={{
                marginTop: active === i ? '0.75rem' : '0.4rem',
                color: active === i ? 'var(--green-light)' : 'var(--gold)',
                fontSize: '0.72rem', fontFamily: 'var(--font-body)',
                letterSpacing: '0.06em',
                transition: 'margin 0.3s, color 0.3s',
              }}>
                {active === i ? '▲ Close' : '▼ Explore'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
