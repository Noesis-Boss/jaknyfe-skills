import React from 'react'

export const CTA = (): React.ReactElement => {
  return (
    <section className="cta-section">
      <div className="cta-panel">
        <span className="cta-eyebrow">Join the Work</span>
        <h2 className="cta-title">Come to a meeting. Meet the men. See the mission.</h2>
        <p className="cta-text">
          Whether you are a newly raised Master Mason or a seasoned brother looking for renewed
          purpose, the Tucson Knights of St. Andrew welcome you to the next step.
        </p>
        <div className="cta-buttons">
          <a href="#calendar" className="cta-btn cta-btn-primary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
            View Upcoming Events
          </a>
          <a href="mailto:ksa@tucsonscottishrite.org" className="cta-btn cta-btn-secondary">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
              <polyline points="22,6 12,13 2,6" />
            </svg>
            Contact the Knights
          </a>
        </div>
        <div className="cta-details">
          <div className="cta-detail">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
            <span><strong>Scottish Rite Cathedral</strong> · 160 S Scott Ave, Tucson</span>
          </div>
          <div className="cta-detail">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            <span>Stated Meetings <strong>2nd Saturday</strong> · 9:00 AM</span>
          </div>
          <div className="cta-detail">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />
            </svg>
            <span>Knights' Line: <strong>(520) 622-4540</strong></span>
          </div>
        </div>
      </div>
    </section>
  )
}
