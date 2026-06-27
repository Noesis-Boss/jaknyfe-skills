import React from 'react'

interface EventItem {
  date: string
  isoDate: string
  title: string
  location: string
  type: 'meeting' | 'reunion' | 'social' | 'ceremony'
  description: string
}

const events: EventItem[] = [
  {
    date: 'July 11, 2026',
    isoDate: '2026-07-11',
    title: 'Summer Stated Meeting',
    location: 'Scottish Rite Cathedral · Tucson',
    type: 'meeting',
    description:
      'Quarterly business meeting — election of Officers for the ensuing term, committee reports, and the traditional brethren’s collation.',
  },
  {
    date: 'August 8, 2026',
    isoDate: '2026-08-08',
    title: 'Annual Picnic & Family Day',
    location: 'Reid Park · DeMeester Pavilion',
    type: 'social',
    description:
      'Sir Knights, wives, children, and grandchildren gather for an afternoon of food, fellowship, and the famous kids-vs-Knights softball game.',
  },
  {
    date: 'September 19, 2026',
    isoDate: '2026-09-19',
    title: 'Fall Reunion — 29° Knight of St. Andrew',
    location: 'Scottish Rite Cathedral · Tucson',
    type: 'reunion',
    description:
      'Conferral of the 29° upon a new class of candidates. Petitions close August 15. Dinner at 6 PM; ceremony at 7:30 PM.',
  },
  {
    date: 'October 10, 2026',
    isoDate: '2026-10-10',
    title: 'Charity Banquet — 33rd Annual',
    location: 'Tucson Convention Center · Ballroom B',
    type: 'social',
    description:
      'Black-tie gala benefiting the RiteCare Speech & Language Clinic. Live auction, distinguished guest speaker, and the traditional Toasts.',
  },
  {
    date: 'November 14, 2026',
    isoDate: '2026-11-14',
    title: 'Memorial Service for Departed Brethren',
    location: 'Scottish Rite Cathedral · Banquet Hall',
    type: 'ceremony',
    description:
      'The Chapter joins the Valley of Tucson in solemn remembrance of those who have laid down their working tools since last we met.',
  },
  {
    date: 'December 12, 2026',
    isoDate: '2026-12-12',
    title: 'Stated Meeting & Installation of Officers',
    location: 'Scottish Rite Cathedral · Tucson',
    type: 'ceremony',
    description:
      'The incoming line of Officers is installed in ancient form. Open installation, followed by the Holiday Reception at the Banquet Hall.',
  },
]

const TYPE_META: Record<EventItem['type'], { label: string; color: string }> = {
  meeting: { label: 'Stated Meeting', color: 'var(--navy)' },
  reunion: { label: 'Reunion', color: 'var(--crimson)' },
  social: { label: 'Social', color: 'var(--green)' },
  ceremony: { label: 'Ceremony', color: 'var(--gold)' },
}

const formatDate = (iso: string) => {
  const d = new Date(iso + 'T12:00:00')
  return {
    weekday: d.toLocaleDateString('en-US', { weekday: 'short' }).toUpperCase(),
    day: d.getDate(),
    month: d.toLocaleDateString('en-US', { month: 'short' }).toUpperCase(),
  }
}

const Card = ({ e, idx, ref }: { e: EventItem; idx: number; ref: (el: HTMLDivElement | null) => void }) => {
  const [visible, setVisible] = React.useState(false)
  const localRef = React.useRef<HTMLDivElement | null>(null)

  React.useEffect(() => {
    const node = localRef.current
    if (!node) return
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true)
          obs.disconnect()
        }
      },
      { threshold: 0.18 },
    )
    obs.observe(node)
    return () => obs.disconnect()
  }, [])

  const setRefs = (el: HTMLDivElement | null) => {
    localRef.current = el
    ref(el)
  }

  const d = formatDate(e.isoDate)
  const meta = TYPE_META[e.type]

  return (
    <div
      ref={setRefs}
      className="event-card"
      style={{
        display: 'grid',
        gridTemplateColumns: '88px 1fr',
        background: '#fff',
        border: '1px solid rgba(10,22,40,0.08)',
        borderRadius: 4,
        overflow: 'hidden',
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateX(0)' : 'translateX(-24px)',
        transition: `opacity 0.6s ease ${idx * 80}ms, transform 0.6s ease ${idx * 80}ms, box-shadow 0.3s ease, border-color 0.3s ease`,
        position: 'relative',
        borderLeft: `3px solid ${meta.color}`,
      }}
    >
      {/* Date block */}
      <div
        style={{
          background: meta.color,
          color: '#fff',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1.4rem 0.5rem',
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.62rem',
            fontWeight: 700,
            letterSpacing: '0.15em',
            opacity: 0.85,
          }}
        >
          {d.weekday}
        </div>
        <div
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '2.1rem',
            fontWeight: 700,
            lineHeight: 1,
            margin: '0.2rem 0',
          }}
        >
          {d.day}
        </div>
        <div
          style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.66rem',
            fontWeight: 700,
            letterSpacing: '0.15em',
            opacity: 0.85,
          }}
        >
          {d.month}
        </div>
      </div>

      {/* Body */}
      <div style={{ padding: '1.2rem 1.4rem 1.3rem', minWidth: 0 }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            marginBottom: '0.4rem',
          }}
        >
          <span
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.62rem',
              fontWeight: 700,
              letterSpacing: '0.2em',
              textTransform: 'uppercase',
              color: meta.color,
              padding: '0.18rem 0.5rem',
              border: `1px solid ${meta.color}`,
              borderRadius: 2,
            }}
          >
            {meta.label}
          </span>
          <span
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.78rem',
              color: 'var(--text-muted)',
              display: 'flex',
              alignItems: 'center',
              gap: 4,
            }}
          >
            <svg width="11" height="11" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4">
              <path d="M8 14s-5-4.5-5-8a5 5 0 0 1 10 0c0 3.5-5 8-5 8z" />
              <circle cx="8" cy="6" r="1.5" />
            </svg>
            {e.location}
          </span>
        </div>
        <h3
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '1.25rem',
            color: 'var(--navy)',
            margin: '0 0 0.5rem',
            lineHeight: 1.25,
          }}
        >
          {e.title}
        </h3>
        <p
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '0.92rem',
            fontStyle: 'italic',
            color: 'var(--text-body)',
            margin: 0,
            lineHeight: 1.5,
          }}
        >
          {e.description}
        </p>
      </div>
    </div>
  )
}

export const Events = () => {
  const [filter, setFilter] = React.useState<'all' | EventItem['type']>('all')
  const [ref, setRef] = React.useState<HTMLDivElement | null>(null)

  const filtered = filter === 'all' ? events : events.filter(e => e.type === filter)

  const filters: { key: 'all' | EventItem['type']; label: string }[] = [
    { key: 'all', label: 'All' },
    { key: 'meeting', label: 'Meetings' },
    { key: 'reunion', label: 'Reunions' },
    { key: 'social', label: 'Social' },
    { key: 'ceremony', label: 'Ceremonies' },
  ]

  return (
    <section
      id="calendar"
      ref={setRef}
      style={{
        background: 'var(--navy-light)',
        padding: '6rem 1.5rem',
        position: 'relative',
        color: 'var(--cream)',
      }}
    >
      <div
        aria-hidden
        style={{
          position: 'absolute',
          inset: 0,
          opacity: 0.06,
          background:
            'radial-gradient(circle at 20% 0%, var(--gold) 0%, transparent 50%), radial-gradient(circle at 80% 100%, var(--green) 0%, transparent 60%)',
        }}
      />
      <div style={{ position: 'relative', maxWidth: 1100, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
          <p
            style={{
              fontFamily: 'var(--font-body)',
              fontSize: '0.72rem',
              fontWeight: 700,
              letterSpacing: '0.3em',
              textTransform: 'uppercase',
              color: 'var(--gold-light)',
              marginBottom: '0.6rem',
            }}
          >
            On the Calendar
          </p>
          <h2
            style={{
              fontFamily: 'var(--font-display)',
              fontSize: 'clamp(2rem, 4vw, 2.8rem)',
              color: '#fff',
              marginBottom: '0.75rem',
            }}
          >
            Coming Together
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
              color: 'rgba(245,241,232,0.7)',
              maxWidth: 580,
              margin: '0 auto',
            }}
          >
            Stated meetings, reunions, and the social occasions that bind us.
          </p>
        </div>

        {/* Filter chips */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '0.5rem',
            marginBottom: '2.5rem',
            flexWrap: 'wrap',
          }}
        >
          {filters.map(f => (
            <button
              key={f.key}
              onClick={() => setFilter(f.key)}
              style={{
                background: filter === f.key ? 'var(--gold)' : 'transparent',
                color: filter === f.key ? 'var(--navy)' : 'rgba(245,241,232,0.85)',
                border: '1px solid',
                borderColor: filter === f.key ? 'var(--gold)' : 'rgba(184,149,58,0.4)',
                padding: '0.5rem 1.2rem',
                borderRadius: 999,
                fontFamily: 'var(--font-body)',
                fontSize: '0.78rem',
                fontWeight: 700,
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              {f.label}
            </button>
          ))}
        </div>

        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))',
            gap: '1rem',
          }}
        >
          {filtered.map((e, i) => (
            <Card key={e.isoDate + e.title} e={e} idx={i} ref={() => {}} />
          ))}
        </div>

        {filtered.length === 0 && (
          <p
            style={{
              textAlign: 'center',
              fontFamily: 'var(--font-display)',
              fontStyle: 'italic',
              color: 'rgba(245,241,232,0.55)',
              marginTop: '2rem',
            }}
          >
            Nothing scheduled in this category. Check back soon.
          </p>
        )}
      </div>
    </section>
  )
}