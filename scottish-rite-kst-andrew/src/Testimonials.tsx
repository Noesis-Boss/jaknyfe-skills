import React from 'react'

interface Testimonial {
  quote: string
  name: string
  title: string
  years: number
  initials: string
}

const testimonials: Testimonial[] = [
  {
    quote:
      'The Knights gave me brothers I never knew I needed. Forty-two years on, the friendships forged in this Order remain the bedrock of my life.',
    name: 'Sir Robert M. Castillo',
    title: 'Past First Knight · 29°',
    years: 42,
    initials: 'RC',
  },
  {
    quote:
      'When the Cathedral burned in 2008, the Chapter was on the grounds before the fire trucks left. That is who we are — not in words, but in deed.',
    name: 'Sir William J. Holloway',
    title: 'Past Commander-in-Chief · Valley of Tucson',
    years: 37,
    initials: 'WH',
  },
  {
    quote:
      'My grandfather was dubbed here in 1962. My father in 1989. I was the third generation to kneel at the Altar in 2019. The Saltire runs in our blood.',
    name: 'Sir Anthony D. Vega',
    title: 'Knight · Third-Generation Member',
    years: 7,
    initials: 'AV',
  },
]

export const Testimonials = (): React.ReactElement => {
  return (
    <section className="testimonials-section">
      <div className="testimonials-inner">
        <div className="testimonials-header">
          <span className="testimonials-eyebrow">From the Brethren</span>
          <h2 className="testimonials-title">What It Means to Wear the Saltire</h2>
          <p className="testimonials-subtitle">
            Three voices — across three generations — on the brotherhood of the Order.
          </p>
        </div>

        <div className="testimonials-grid">
          {testimonials.map((t, idx) => (
            <article key={idx} className="testimonial-card">
              <svg
                className="testimonial-quote-mark"
                viewBox="0 0 32 32"
                aria-hidden="true"
              >
                <path
                  d="M9 8c-3 1-5 4-5 8v8h8v-8H6c0-3 1-5 3-6V8zm14 0c-3 1-5 4-5 8v8h8v-8h-6c0-3 1-5 3-6V8z"
                  fill="currentColor"
                />
              </svg>
              <blockquote className="testimonial-quote">
                <p>{t.quote}</p>
              </blockquote>
              <div className="testimonial-author">
                <div className="testimonial-avatar" aria-hidden="true">
                  {t.initials}
                </div>
                <div className="testimonial-meta">
                  <div className="testimonial-name">{t.name}</div>
                  <div className="testimonial-title">{t.title}</div>
                  <div className="testimonial-years">{t.years} years a Knight</div>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}