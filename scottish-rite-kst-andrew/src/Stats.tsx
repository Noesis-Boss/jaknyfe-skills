import React from 'react'

interface StatProps {
  end: number
  prefix?: string
  suffix?: string
  label: string
  sub?: string
  delay?: number
}

const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3)

const Stat = ({ end, prefix = '', suffix = '', label, sub, delay = 0 }: StatProps) => {
  const [ref, setRef] = React.useState<HTMLDivElement | null>(null)
  const [value, setValue] = React.useState(0)
  const [started, setStarted] = React.useState(false)

  React.useEffect(() => {
    if (!ref) return
    const obs = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setStarted(true)
          obs.disconnect()
        }
      },
      { threshold: 0.4 },
    )
    obs.observe(ref)
    return () => obs.disconnect()
  }, [ref])

  React.useEffect(() => {
    if (!started) return
    let raf = 0
    const start = performance.now()
    const duration = 1800
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration)
      setValue(Math.round(end * easeOutCubic(t)))
      if (t < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [started, end])

  return (
    <div
      ref={setRef}
      className="stat-cell"
      style={{
        textAlign: 'center',
        padding: '1.4rem 0.5rem',
        opacity: started ? 1 : 0,
        transform: started ? 'translateY(0)' : 'translateY(20px)',
        transition: `opacity 0.7s ease ${delay}ms, transform 0.7s ease ${delay}ms`,
      }}
    >
      <div
        style={{
          fontFamily: 'var(--font-display)',
          fontSize: 'clamp(2.6rem, 5vw, 3.6rem)',
          fontWeight: 700,
          color: 'var(--gold)',
          lineHeight: 1,
          letterSpacing: '-0.02em',
          textShadow: '0 2px 10px rgba(184,149,58,0.25)',
        }}
      >
        {prefix}
        {value.toLocaleString()}
        {suffix}
      </div>
      <div
        style={{
          width: 28,
          height: 1,
          background: 'var(--gold)',
          opacity: 0.5,
          margin: '0.7rem auto',
        }}
      />
      <div
        style={{
          fontFamily: 'var(--font-body)',
          fontSize: '0.72rem',
          fontWeight: 700,
          letterSpacing: '0.22em',
          textTransform: 'uppercase',
          color: 'rgba(245,241,232,0.85)',
        }}
      >
        {label}
      </div>
      {sub && (
        <div
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: '0.85rem',
            fontStyle: 'italic',
            color: 'rgba(245,241,232,0.55)',
            marginTop: 6,
          }}
        >
          {sub}
        </div>
      )}
    </div>
  )
}

const stats: StatProps[] = [
  { end: 33, label: 'Years on the Saltire', sub: 'Chartered 1993', delay: 0 },
  { end: 412, label: 'Sir Knights', sub: 'In good standing', delay: 120 },
  { end: 28, prefix: '$', suffix: 'K', label: 'RiteCare Raised (2025)', sub: 'For the children of Tucson', delay: 240 },
  { end: 1800, suffix: '+', label: 'Service Hours', sub: 'Last calendar year', delay: 360 },
]

export const Stats = () => {
  return (
    <section
      id="impact"
      style={{
        position: 'relative',
        background: 'var(--navy)',
        padding: '5rem 1.5rem',
        borderTop: '1px solid rgba(184,149,58,0.18)',
        borderBottom: '1px solid rgba(184,149,58,0.18)',
        overflow: 'hidden',
      }}
    >
      {/* Faint heraldic pattern */}
      <div
        aria-hidden
        style={{
          position: 'absolute',
          inset: 0,
          opacity: 0.04,
          backgroundImage:
            'repeating-linear-gradient(45deg, transparent 0 60px, rgba(184,149,58,0.4) 60px 61px), repeating-linear-gradient(-45deg, transparent 0 60px, rgba(184,149,58,0.4) 60px 61px)',
        }}
      />
      <div
        style={{
          position: 'relative',
          maxWidth: 1100,
          margin: '0 auto',
        }}
      >
        <p
          style={{
            fontFamily: 'var(--font-body)',
            fontSize: '0.72rem',
            fontWeight: 700,
            letterSpacing: '0.3em',
            textTransform: 'uppercase',
            color: 'var(--gold)',
            textAlign: 'center',
            marginBottom: '0.5rem',
          }}
        >
          By the Numbers
        </p>
        <h2
          style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(1.6rem, 3vw, 2.2rem)',
            color: '#fff',
            textAlign: 'center',
            marginBottom: '2.5rem',
          }}
        >
          The Chapter at a Glance
        </h2>
        <div
          className="stats-grid"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '1rem',
          }}
        >
          {stats.map(s => (
            <Stat key={s.label} {...s} />
          ))}
        </div>
      </div>
    </section>
  )
}
