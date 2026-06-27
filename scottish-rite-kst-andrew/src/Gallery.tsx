import React from 'react'

type Icon = 'cross' | 'crown' | 'sword' | 'cathedral' | 'compass' | 'chalice'

interface ArchiveItem {
  year: string
  title: string
  caption: string
  hue: number
  icon: Icon
}

const items: ArchiveItem[] = [
  {
    year: '1993',
    title: 'The Charter Night',
    caption:
      'Sir Robert B. Neman and sixteen founding Knights assemble beneath the Saltire at the Tucson Consistory.',
    hue: 42,
    icon: 'crown',
  },
  {
    year: '1998',
    title: 'First Spring Reunion',
    caption:
      'Thirty-two new Sir Knights are dubbed. The Chapter takes its first formal Honor Guard post.',
    hue: 145,
    icon: 'cross',
  },
  {
    year: '2004',
    title: 'RiteCare Founding',
    caption:
      'The Tucson Chapter pledges $5,000 to found the RiteCare Speech & Language Clinic at the University of Arizona.',
    hue: 18,
    icon: 'chalice',
  },
  {
    year: '2008',
    title: 'Cathedral Restoration',
    caption:
      'After the October fire, the Chapter contributes 2,100 volunteer hours to the Cathedral restoration.',
    hue: 0,
    icon: 'cathedral',
  },
  {
    year: '2014',
    title: 'Charity Banquet Record',
    caption:
      'The annual banquet raises $87,000 in a single evening — a Valley of Tucson record that still stands.',
    hue: 200,
    icon: 'compass',
  },
  {
    year: '2023',
    title: 'The Centennial Salute',
    caption:
      'The Chapter marches in the Valley of Tucson Centennial Parade — 412 strong, in full regalia.',
    hue: 270,
    icon: 'sword',
  },
]

const IconSvg = ({ icon }: { icon: Icon }) => {
  const stroke = 'var(--gold)'
  const common = {
    width: 56,
    height: 56,
    viewBox: '0 0 64 64',
    fill: 'none',
    stroke,
    strokeWidth: 1.4,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
  }
  switch (icon) {
    case 'cross':
      return (
        <svg {...common}>
          <line x1="32" y1="8" x2="32" y2="56" />
          <line x1="12" y1="20" x2="52" y2="20" />
        </svg>
      )
    case 'crown':
      return (
        <svg {...common}>
          <path d="M10 44 L14 22 L24 32 L32 16 L40 32 L50 22 L54 44 Z" />
          <line x1="10" y1="50" x2="54" y2="50" />
          <circle cx="14" cy="20" r="1.5" fill={stroke} />
          <circle cx="50" cy="20" r="1.5" fill={stroke} />
          <circle cx="32" cy="14" r="1.5" fill={stroke} />
        </svg>
      )
    case 'sword':
      return (
        <svg {...common}>
          <line x1="32" y1="6" x2="32" y2="48" />
          <line x1="22" y1="16" x2="42" y2="16" />
          <line x1="26" y1="48" x2="38" y2="48" />
          <line x1="32" y1="48" x2="32" y2="58" />
        </svg>
      )
    case 'cathedral':
      return (
        <svg {...common}>
          <path d="M10 50 L10 30 L16 30 L16 18 L24 12 L24 30 L40 30 L40 12 L48 18 L48 30 L54 30 L54 50 Z" />
          <line x1="10" y1="50" x2="54" y2="50" />
          <rect x="29" y="36" width="6" height="14" />
          <circle cx="32" cy="9" r="1" fill={stroke} />
        </svg>
      )
    case 'compass':
      return (
        <svg {...common}>
          <circle cx="32" cy="32" r="20" />
          <polygon points="32,16 36,32 32,48 28,32" fill={stroke} fillOpacity="0.2" />
          <circle cx="32" cy="32" r="2" fill={stroke} />
        </svg>
      )
    case 'chalice':
      return (
        <svg {...common}>
          <path d="M20 14 L44 14 L40 30 Q32 38 24 30 Z" />
          <line x1="32" y1="30" x2="32" y2="46" />
          <line x1="24" y1="50" x2="40" y2="50" />
        </svg>
      )
  }
}

const Card = ({ item, idx, onOpen }: { item: ArchiveItem; idx: number; onOpen: () => void }) => {
  const [ref, setRef] = React.useState<HTMLDivElement | null>(null)
  const [visible, setVisible] = React.useState(false)

  React.useEffect(() => {
    if (!ref) return
    const obs = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setVisible(true)
          obs.disconnect()
        }
      },
      { threshold: 0.15 },
    )
    obs.observe(ref)
    return () => obs.disconnect()
  }, [ref])

  return (
    <button
      ref={setRef as any}
      onClick={onOpen}
      className="archive-card"
      style={{
        all: 'unset',
        cursor: 'pointer',
        display: 'block',
        position: 'relative',
        background: '#fff',
        border: '1px solid rgba(10,22,40,0.08)',
        borderRadius: 4,
        overflow: 'hidden',
        boxShadow: '0 4px 16px -10px rgba(10,22,40,0.2)',
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(28px)',
        transition: `opacity 0.6s ease ${idx * 80}ms, transform 0.6s ease ${idx * 80}ms, box-shadow 0.3s ease`,
      }}
      onMouseEnter={e => {
        e.currentTarget.style.boxShadow = '0 14px 32px -12px rgba(184,149,58,0.4)'
      }}
      onMouseLeave={e => {
        e.currentTarget.style.boxShadow = '0 4px 16px -10px rgba(10,22,40,0.2)'
      }}
    >
      <div
        style={{
          aspectRatio: '4 / 3',
          position: 'relative',
          background: `linear-gradient(135deg, hsl(${item.hue} 35% 18%) 0%, hsl(${item.hue} 30% 8%) 100%)`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          overflow: 'hidden',
        }}
      >
        {/* Decorative saltire behind the icon */}
        <svg
          aria-hidden
          viewBox="0 0 100 100"
          preserveAspectRatio="none"
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            opacity: 0.18,
          }}
        >
          <line x1="0" y1="100" x2="100" y2="0" stroke="var(--gold)" strokeWidth="0.6" />
          <line x1="0" y1="0" x2="100" y2="100" stroke="var(--gold)" strokeWidth="0.6" />
        </svg>
        <div
          style={{
            position: 'relative',
            zIndex: 1,
            padding: '1rem',
            transition: 'transform 0.4s ease',
          }}
          className="archive-icon-wrap"
        >
          <IconSvg icon={item.icon} />
        </div>
        {/* Year stamp */}
        <div
          style={{
            position: 'absolute',
            top: 10,
            left: 10,
            fontFamily: 'var(--font-display)',
            fontSize: '0.95rem',
            fontWeight: 700,
            color: 'var(--gold)',
            letterSpacing: '0.1em',
            padding: '0.25rem 0.55rem',
            background: 'rgba(10,22,40,0.7)',
            border: '1px solid rgba(184,149,58,0.4)',
            borderRadius: 3,
          }}
        >
          {item.year}
        </div>
      </div>
      <div style={{ padding: '1rem 1.1rem 1.2rem' }}>
        <h3
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '1.1rem',
            color: 'var(--navy)',
            margin: 0,
            lineHeight: 1.3,
          }}
        >
          {item.title}
        </h3>
        <p
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '0.9rem',
            fontStyle: 'italic',
            color: 'var(--text-muted)',
            margin: '0.5rem 0 0',
            lineHeight: 1.5,
          }}
        >
          {item.caption}
        </p>
        <div
          style={{
            marginTop: '0.8rem',
            fontFamily: 'var(--font-body)',
            fontSize: '0.7rem',
            fontWeight: 700,
            letterSpacing: '0.18em',
            textTransform: 'uppercase',
            color: 'var(--gold)',
            display: 'flex',
            alignItems: 'center',
            gap: 6,
          }}
        >
          Read the entry
          <span style={{ display: 'inline-block', transition: 'transform 0.2s' }} className="archive-arrow">
            →
          </span>
        </div>
      </div>
    </button>
  )
}

export const Gallery = () => {
  const [open, setOpen] = React.useState<ArchiveItem | null>(null)

  return (
    <section
      id="archive"
      style={{
        background: 'var(--cream)',
        padding: '6rem 1.5rem',
        position: 'relative',
        borderTop: '1px solid rgba(10,22,40,0.08)',
      }}
    >
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.72rem',
              fontWeight: 700,
              letterSpacing: '0.3em',
              textTransform: 'uppercase',
              color: 'var(--crimson)',
              marginBottom: '0.6rem',
            }}
          >
            The Chronicles
          </p>
          <h2
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(2rem, 4vw, 2.8rem)',
              color: 'var(--navy)',
              marginBottom: '0.75rem',
            }}
          >
            From the Archive
          </h2>
          <div
            style={{
              width: 60,
              height: 1.5,
              background: 'var(--gold)',
              margin: '0 auto 1rem',
            }}
          />
          <p
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: '1.05rem',
              fontStyle: 'italic',
              color: 'var(--text-muted)',
              maxWidth: 600,
              margin: '0 auto',
            }}
          >
            Six moments etched in the Chapter's memory. Tap any to read the full account.
          </p>
        </div>

        <div
          className="archive-grid"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
            gap: '1.4rem',
          }}
        >
          {items.map((it, i) => (
            <Card key={it.year + it.title} item={it} idx={i} onOpen={() => setOpen(it)} />
          ))}
        </div>
      </div>

      {open && (
        <div
          onClick={() => setOpen(null)}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(10,22,40,0.78)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1.5rem',
            animation: 'fadeIn 0.25s ease',
          }}
        >
          <div
            onClick={e => e.stopPropagation()}
            style={{
              background: 'var(--cream)',
              maxWidth: 520,
              width: '100%',
              borderRadius: 6,
              padding: '2rem 1.8rem',
              position: 'relative',
              borderTop: '3px solid var(--gold)',
              boxShadow: '0 30px 60px -20px rgba(0,0,0,0.5)',
              animation: 'zoomIn 0.25s ease',
            }}
          >
            <button
              onClick={() => setOpen(null)}
              aria-label="Close"
              style={{
                position: 'absolute',
                top: 12,
                right: 12,
                background: 'transparent',
                border: 'none',
                cursor: 'pointer',
                color: 'var(--navy)',
                fontSize: '1.4rem',
                lineHeight: 1,
                padding: 4,
              }}
            >
              ×
            </button>
            <div
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '0.9rem',
                fontWeight: 700,
                color: 'var(--gold)',
                letterSpacing: '0.2em',
                marginBottom: '0.4rem',
              }}
            >
              ANNO {open.year}
            </div>
            <h3
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '1.6rem',
                color: 'var(--navy)',
                margin: '0 0 0.8rem',
                lineHeight: 1.2,
              }}
            >
              {open.title}
            </h3>
            <p
              style={{
                fontFamily: 'var(--font-display)',
                fontSize: '1.05rem',
                fontStyle: 'italic',
                color: 'var(--text-body)',
                lineHeight: 1.6,
                margin: 0,
              }}
            >
              {open.caption}
            </p>
            <div
              style={{
                marginTop: '1.4rem',
                paddingTop: '1rem',
                borderTop: '1px solid rgba(10,22,40,0.08)',
                fontFamily: 'var(--font-body)',
                fontSize: '0.8rem',
                color: 'var(--text-muted)',
                lineHeight: 1.6,
              }}
            >
              The full account, including minutes, photographs, and the names of the Brethren present, is preserved in the Chapter Ledger. Members in good standing may request a transcription from the Recorder.
            </div>
          </div>
        </div>
      )}
    </section>
  )
}
