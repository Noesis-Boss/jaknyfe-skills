import React from 'react'

export const Join = () => {
  const [submitted, setSubmitted] = React.useState(false)

  return (
    <section id="join" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 800, margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
            letterSpacing: '0.2em', textTransform: 'uppercase',
            color: 'var(--green)', marginBottom: '0.75rem',
          }}>Join the Order</p>
          <h2 style={{
            fontFamily: 'var(--font-display)',
            fontSize: 'clamp(2rem, 4vw, 2.8rem)',
            fontWeight: 600, color: 'var(--navy)', margin: '0 0 1rem', lineHeight: 1.15,
          }}>Become a Knight</h2>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '1.05rem',
            color: 'var(--text-muted)', maxWidth: 560, margin: '0 auto', lineHeight: 1.7,
          }}>
            Membership is open to 32° Scottish Rite Masons in good standing within the Valley of Tucson. Submit your petition and begin your journey as a Squire.
          </p>
          <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.5rem auto 0', borderRadius: 1 }} />
        </div>

        {!submitted ? (
          <div style={{
            background: '#fff', borderRadius: 8,
            border: '1px solid #e5e2da', padding: '2.5rem',
            boxShadow: '0 4px 24px rgba(0,0,0,0.06)',
          }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.25rem' }}>
              <div>
                <label style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.78rem',
                  fontWeight: 700, letterSpacing: '0.08em',
                  textTransform: 'uppercase', color: 'var(--text-muted)',
                  display: 'block', marginBottom: '0.5rem',
                }}>First Name</label>
                <input type="text" placeholder="John" style={{
                  width: '100%', padding: '0.75rem 1rem',
                  border: '1px solid #ddd', borderRadius: 4,
                  fontFamily: 'var(--font-body)', fontSize: '0.95rem',
                  outline: 'none', transition: 'border-color 0.2s',
                }} onFocus={e => (e.target as HTMLElement).style.borderColor = 'var(--gold)'}
                   onBlur={e => (e.target as HTMLElement).style.borderColor = '#ddd'} />
              </div>
              <div>
                <label style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.78rem',
                  fontWeight: 700, letterSpacing: '0.08em',
                  textTransform: 'uppercase', color: 'var(--text-muted)',
                  display: 'block', marginBottom: '0.5rem',
                }}>Last Name</label>
                <input type="text" placeholder="Smith" style={{
                  width: '100%', padding: '0.75rem 1rem',
                  border: '1px solid #ddd', borderRadius: 4,
                  fontFamily: 'var(--font-body)', fontSize: '0.95rem',
                  outline: 'none', transition: 'border-color 0.2s',
                }} onFocus={e => (e.target as HTMLElement).style.borderColor = 'var(--gold)'}
                   onBlur={e => (e.target as HTMLElement).style.borderColor = '#ddd'} />
              </div>
              <div>
                <label style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.78rem',
                  fontWeight: 700, letterSpacing: '0.08em',
                  textTransform: 'uppercase', color: 'var(--text-muted)',
                  display: 'block', marginBottom: '0.5rem',
                }}>Email</label>
                <input type="email" placeholder="brother@lodge.org" style={{
                  width: '100%', padding: '0.75rem 1rem',
                  border: '1px solid #ddd', borderRadius: 4,
                  fontFamily: 'var(--font-body)', fontSize: '0.95rem',
                  outline: 'none', transition: 'border-color 0.2s',
                }} onFocus={e => (e.target as HTMLElement).style.borderColor = 'var(--gold)'}
                   onBlur={e => (e.target as HTMLElement).style.borderColor = '#ddd'} />
              </div>
              <div>
                <label style={{
                  fontFamily: 'var(--font-body)', fontSize: '0.78rem',
                  fontWeight: 700, letterSpacing: '0.08em',
                  textTransform: 'uppercase', color: 'var(--text-muted)',
                  display: 'block', marginBottom: '0.5rem',
                }}>Lodge Name & Number</label>
                <input type="text" placeholder="Tucson Lodge No. 4" style={{
                  width: '100%', padding: '0.75rem 1rem',
                  border: '1px solid #ddd', borderRadius: 4,
                  fontFamily: 'var(--font-body)', fontSize: '0.95rem',
                  outline: 'none', transition: 'border-color 0.2s',
                }} onFocus={e => (e.target as HTMLElement).style.borderColor = 'var(--gold)'}
                   onBlur={e => (e.target as HTMLElement).style.borderColor = '#ddd'} />
              </div>
            </div>
            <div style={{ marginTop: '1.25rem' }}>
              <label style={{
                fontFamily: 'var(--font-body)', fontSize: '0.78rem',
                fontWeight: 700, letterSpacing: '0.08em',
                textTransform: 'uppercase', color: 'var(--text-muted)',
                display: 'block', marginBottom: '0.5rem',
              }}>Why do you wish to join the KSA?</label>
              <textarea rows={4} placeholder="Tell us about your interest in service and fellowship..." style={{
                width: '100%', padding: '0.75rem 1rem',
                border: '1px solid #ddd', borderRadius: 4,
                fontFamily: 'var(--font-body)', fontSize: '0.95rem',
                outline: 'none', resize: 'vertical', transition: 'border-color 0.2s',
              }} onFocus={e => (e.target as HTMLElement).style.borderColor = 'var(--gold)'}
                 onBlur={e => (e.target as HTMLElement).style.borderColor = '#ddd'} />
            </div>
            <button
              onClick={() => setSubmitted(true)}
              style={{
                display: 'block', width: '100%', marginTop: '1.5rem',
                padding: '1rem', border: 'none', cursor: 'pointer',
                background: 'var(--green)', color: '#fff',
                fontFamily: 'var(--font-body)', fontSize: '0.85rem',
                fontWeight: 700, letterSpacing: '0.12em',
                textTransform: 'uppercase', borderRadius: 4,
                transition: 'background 0.2s',
              }}
              onMouseEnter={e => (e.target as HTMLElement).style.background = 'var(--green-light)'}
              onMouseLeave={e => (e.target as HTMLElement).style.background = 'var(--green)'}
            >
              Submit Petition
            </button>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '0.78rem',
              color: 'var(--text-muted)', textAlign: 'center', marginTop: '1rem',
            }}>
              Your petition will be reviewed by the Chapter officers. You will be contacted regarding next steps.
            </p>
          </div>
        ) : (
          <div style={{
            textAlign: 'center', padding: '3rem 2rem',
            background: '#fff', borderRadius: 8,
            border: '1px solid #e5e2da',
          }}>
            <div style={{
              width: 64, height: 64, borderRadius: '50%',
              background: 'rgba(45,106,79,0.1)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              margin: '0 auto 1.5rem',
            }}>
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="var(--green)" strokeWidth="2.5">
                <polyline points="8,16 14,22 24,10" />
              </svg>
            </div>
            <h3 style={{
              fontFamily: 'var(--font-display)', fontSize: '1.6rem',
              fontWeight: 600, color: 'var(--navy)', margin: '0 0 1rem',
            }}>Petition Received</h3>
            <p style={{
              fontFamily: 'var(--font-body)', fontSize: '1rem',
              color: 'var(--text-muted)', lineHeight: 1.7, maxWidth: 420, margin: '0 auto',
            }}>
              Thank you, Brother. Your petition has been submitted to the Chapter. A Knight will be in contact with you regarding your journey to the Order.
            </p>
          </div>
        )}
      </div>
    </section>
  )
}
