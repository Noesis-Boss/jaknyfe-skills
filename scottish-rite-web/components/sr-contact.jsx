
// Membership, Donate, Contact, Footer sections

// ── MEMBERSHIP ─────────────────────────────────────────────────────────────
const SRMembership = () => {
  const steps = [
    { num: '01', title: 'Be a Master Mason', text: 'Membership in the Scottish Rite requires that you first be a Master Mason in good standing in a Symbolic Lodge.' },
    { num: '02', title: 'Express Interest', text: 'Contact our Secretary General or speak with any member of the Valley to request a petition for membership.' },
    { num: '03', title: 'Submit a Petition', text: 'Complete the petition form, which is reviewed by the membership committee and voted upon by the Valley.' },
    { num: '04', title: 'Attend a Reunion', text: 'If approved, you will be invited to attend a Reunion, where the degrees are conferred. Welcome, Brother.' },
  ];

  return (
    <section id="membership" data-screen-label="Membership" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1000, margin: '0 auto' }}>
        <SectionHeader eyebrow="Join Us" title="Become a Member of the Valley" subtitle="We welcome all Master Masons who seek to further their Masonic education and strengthen the bonds of brotherhood." />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: '2rem', marginBottom: '3.5rem' }}>
          {steps.map((s, i) => (
            <div key={i} style={{ position: 'relative' }}>
              {i < steps.length - 1 && (
                <div style={{ position: 'absolute', top: 24, left: 'calc(50% + 24px)', right: '-50%', height: 1, background: 'var(--divider)', display: 'none' }} className="sr-step-connector"/>
              )}
              <div style={{ textAlign: 'center' }}>
                <div style={{
                  width: 52, height: 52, borderRadius: '50%',
                  background: 'var(--navy)', color: 'var(--gold)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: 'var(--font-display)', fontSize: '1.1rem', fontWeight: 700,
                  margin: '0 auto 1.25rem',
                }}>{s.num}</div>
                <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, color: 'var(--navy)', margin: '0 0 0.75rem' }}>{s.title}</h3>
                <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.65, margin: 0 }}>{s.text}</p>
              </div>
            </div>
          ))}
        </div>
        <div style={{ textAlign: 'center' }}>
          <a href="#contact" onClick={e => { e.preventDefault(); const el = document.querySelector('#contact'); if(el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 72, behavior:'smooth'}); }}
            style={{
              display: 'inline-block', background: 'var(--navy)', color: 'var(--gold)',
              textDecoration: 'none', fontFamily: 'var(--font-body)', fontWeight: 700,
              fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase',
              padding: '1rem 2.5rem', borderRadius: 4,
              transition: 'opacity 0.2s',
            }}
            onMouseOver={e => e.currentTarget.style.opacity = '0.85'}
            onMouseOut={e => e.currentTarget.style.opacity = '1'}>
            Request a Petition
          </a>
        </div>
      </div>
    </section>
  );
};

// ── DONATE ─────────────────────────────────────────────────────────────────
const SRDonate = () => {
  const programs = [
    { title: 'RiteCare', desc: 'Funding language & learning therapy for children in Southern Arizona.', icon: '♥' },
    { title: 'Scholarships', desc: 'Annual scholarships for deserving students from our community.', icon: '✦' },
    { title: 'Valley Operations', desc: 'Maintaining our Temple and supporting the programs of the Valley.', icon: '◈' },
  ];

  return (
    <section id="donate" data-screen-label="Donate" style={{ background: 'var(--gold-bg)', padding: '6rem 1.5rem', position: 'relative', overflow: 'hidden' }}>
      <div style={{ position: 'absolute', inset: 0, opacity: 0.06 }}>
        <svg width="100%" height="100%"><pattern id="donPat" width="60" height="60" patternUnits="userSpaceOnUse"><circle cx="30" cy="30" r="1.5" fill="var(--navy)"/></pattern><rect width="100%" height="100%" fill="url(#donPat)"/></svg>
      </div>
      <div style={{ maxWidth: 1000, margin: '0 auto', position: 'relative' }}>
        <SectionHeader eyebrow="Support Our Work" title="Your Gift Makes a Difference" subtitle="The Valley of Tucson supports numerous charitable programs that benefit children and our community." />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem', marginBottom: '3rem' }}>
          {programs.map((p, i) => (
            <div key={i} style={{
              background: 'rgba(255,255,255,0.65)', backdropFilter: 'blur(8px)',
              borderRadius: 8, padding: '2rem', border: '1px solid rgba(255,255,255,0.9)',
              textAlign: 'center',
            }}>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--navy)', marginBottom: '0.75rem' }}>{p.icon}</div>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.25rem', fontWeight: 600, color: 'var(--navy)', margin: '0 0 0.5rem' }}>{p.title}</h3>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.6, margin: 0 }}>{p.desc}</p>
            </div>
          ))}
        </div>
        <div style={{ textAlign: 'center' }}>
          <button style={{
            background: 'var(--navy)', color: 'var(--gold)',
            border: 'none', cursor: 'pointer',
            fontFamily: 'var(--font-body)', fontWeight: 700,
            fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase',
            padding: '1rem 2.5rem', borderRadius: 4,
            transition: 'opacity 0.2s',
          }}
            onMouseOver={e => e.target.style.opacity = '0.85'}
            onMouseOut={e => e.target.style.opacity = '1'}>
            Make a Donation
          </button>
        </div>
      </div>
    </section>
  );
};

// ── CONTACT ─────────────────────────────────────────────────────────────────
const SRContact = () => {
  const [form, setForm] = React.useState({ name: '', email: '', subject: '', message: '' });
  const [sent, setSent] = React.useState(false);
  const [errors, setErrors] = React.useState({});

  const validate = () => {
    const e = {};
    if (!form.name.trim()) e.name = 'Required';
    if (!form.email.trim() || !/\S+@\S+\.\S+/.test(form.email)) e.email = 'Valid email required';
    if (!form.message.trim()) e.message = 'Required';
    return e;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setSent(true);
  };

  const inputStyle = (err) => ({
    width: '100%', boxSizing: 'border-box',
    fontFamily: 'var(--font-body)', fontSize: '0.95rem',
    padding: '0.85rem 1rem', borderRadius: 4,
    border: `1px solid ${err ? '#c0392b' : 'var(--card-border-heavy)'}`,
    background: 'var(--card-bg)', color: 'var(--text-body)',
    outline: 'none', transition: 'border-color 0.2s',
  });

  return (
    <section id="contact" data-screen-label="Contact" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <SectionHeader eyebrow="Get in Touch" title="Contact the Valley" subtitle="Whether you have questions about membership, events, or our charitable programs, we'd love to hear from you." />
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.4fr', gap: '4rem', alignItems: 'start' }} className="sr-two-col">
          {/* Info */}
          <div>
            <div style={{ marginBottom: '2rem' }}>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)', marginBottom: '0.4rem' }}>Address</p>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--navy)', lineHeight: 1.5, margin: 0 }}>
                176 N. Stone Avenue<br/>Tucson, Arizona 85701
              </p>
            </div>
            <div style={{ marginBottom: '2rem' }}>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)', marginBottom: '0.4rem' }}>Stated Meetings</p>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--navy)', lineHeight: 1.5, margin: 0 }}>
                First Tuesday of each month<br/>Dinner 6:00 PM · Meeting 7:00 PM
              </p>
            </div>
            <div style={{ marginBottom: '2rem' }}>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)', marginBottom: '0.4rem' }}>Secretary General</p>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--navy)', lineHeight: 1.5, margin: 0 }}>
                Ill. Frank E. Torres, 33°<br/>
                <a href="mailto:secretary@tucsonscottishrite.org" style={{ color: 'var(--gold)', textDecoration: 'none', fontSize: '0.95rem', fontFamily: 'var(--font-body)' }}>secretary@tucsonscottishrite.org</a>
              </p>
            </div>
            <div>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)', marginBottom: '0.4rem' }}>Phone</p>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: '1.1rem', color: 'var(--navy)', margin: 0 }}>(520) 623-9270</p>
            </div>
            {/* Map placeholder */}
            <div style={{
              marginTop: '2rem', borderRadius: 8, overflow: 'hidden', height: 180,
              background: 'repeating-linear-gradient(0deg, hsl(210,20%,88%) 0px, hsl(210,20%,88%) 1px, hsl(210,15%,92%) 1px, hsl(210,15%,92%) 40px), repeating-linear-gradient(90deg, hsl(210,20%,88%) 0px, hsl(210,20%,88%) 1px, hsl(210,15%,92%) 1px, hsl(210,15%,92%) 40px)',
              border: '1px solid var(--card-border)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              position: 'relative',
            }}>
              <div style={{ background: 'rgba(255,255,255,0.85)', padding: '0.4rem 0.8rem', borderRadius: 4 }}>
                <span style={{ fontFamily: 'monospace', fontSize: '0.75rem', color: '#555' }}>[ Map — 176 N. Stone Ave, Tucson ]</span>
              </div>
              <div style={{ position: 'absolute', width: 16, height: 16, background: 'var(--gold)', borderRadius: '50% 50% 50% 0', transform: 'rotate(-45deg)', boxShadow: '0 2px 8px rgba(0,0,0,0.2)' }}/>
            </div>
          </div>

          {/* Form */}
          <div style={{ background: 'var(--card-bg)', borderRadius: 8, padding: '2.5rem', border: '1px solid var(--card-border)' }}>
            {sent ? (
              <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                <div style={{ width: 56, height: 56, borderRadius: '50%', background: 'rgba(184,149,58,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" strokeWidth="2"><polyline points="20,6 9,17 4,12"/></svg>
                </div>
                <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.6rem', color: 'var(--navy)', margin: '0 0 0.75rem' }}>Message Sent</h3>
                <p style={{ fontFamily: 'var(--font-body)', color: 'var(--text-muted)', lineHeight: 1.6 }}>Thank you for reaching out. A member of our Valley will be in touch shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} noValidate>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
                  <div>
                    <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.78rem', fontWeight: 600, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>Full Name *</label>
                    <input value={form.name} onChange={e => { setForm(f => ({...f, name: e.target.value})); setErrors(e2 => ({...e2, name: ''})); }} style={inputStyle(errors.name)} onFocus={e => e.target.style.borderColor='var(--gold)'} onBlur={e => e.target.style.borderColor=errors.name ? '#c0392b' : 'var(--card-border-heavy)'}/>
                    {errors.name && <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#c0392b', margin: '0.25rem 0 0' }}>{errors.name}</p>}
                  </div>
                  <div>
                    <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.78rem', fontWeight: 600, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>Email Address *</label>
                    <input type="email" value={form.email} onChange={e => { setForm(f => ({...f, email: e.target.value})); setErrors(e2 => ({...e2, email: ''})); }} style={inputStyle(errors.email)} onFocus={e => e.target.style.borderColor='var(--gold)'} onBlur={e => e.target.style.borderColor=errors.email ? '#c0392b' : 'var(--card-border-heavy)'}/>
                    {errors.email && <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#c0392b', margin: '0.25rem 0 0' }}>{errors.email}</p>}
                  </div>
                </div>
                <div style={{ marginBottom: '1rem' }}>
                  <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.78rem', fontWeight: 600, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>Subject</label>
                  <select value={form.subject} onChange={e => setForm(f => ({...f, subject: e.target.value}))} style={{...inputStyle(false), appearance: 'none'}}>
                    <option value="">Select a topic…</option>
                    <option>Membership Inquiry</option>
                    <option>Upcoming Events</option>
                    <option>Charitable Programs</option>
                    <option>General Question</option>
                  </select>
                </div>
                <div style={{ marginBottom: '1.5rem' }}>
                  <label style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.78rem', fontWeight: 600, letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>Message *</label>
                  <textarea rows={5} value={form.message} onChange={e => { setForm(f => ({...f, message: e.target.value})); setErrors(e2 => ({...e2, message: ''})); }} style={{...inputStyle(errors.message), resize: 'vertical'}} onFocus={e => e.target.style.borderColor='var(--gold)'} onBlur={e => e.target.style.borderColor=errors.message ? '#c0392b' : 'var(--card-border-heavy)'}/>
                  {errors.message && <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.75rem', color: '#c0392b', margin: '0.25rem 0 0' }}>{errors.message}</p>}
                </div>
                <button type="submit" style={{
                  width: '100%', background: 'var(--navy)', color: 'var(--gold)',
                  border: 'none', cursor: 'pointer',
                  fontFamily: 'var(--font-body)', fontWeight: 700,
                  fontSize: '0.85rem', letterSpacing: '0.1em', textTransform: 'uppercase',
                  padding: '1rem', borderRadius: 4, transition: 'opacity 0.2s',
                }}
                  onMouseOver={e => e.target.style.opacity = '0.85'}
                  onMouseOut={e => e.target.style.opacity = '1'}>
                  Send Message
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

// ── FOOTER ─────────────────────────────────────────────────────────────────
const SRFooter = () => (
  <footer style={{ background: 'var(--navy)', borderTop: '1px solid rgba(184,149,58,0.2)', padding: '3rem 1.5rem 2rem' }}>
    <div style={{ maxWidth: 1100, margin: '0 auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: '3rem', marginBottom: '3rem' }} className="sr-footer-grid">
        <div>
          <img src="uploads/logo-1776712250947.png" alt="Scottish Rite" style={{ height: 48, marginBottom: '1.25rem', filter: 'brightness(0) invert(1) sepia(1) saturate(0.4) brightness(1.1)' }}/>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.9rem', color: 'rgba(255,255,255,0.5)', lineHeight: 1.7, maxWidth: 320, margin: 0 }}>
            The Valley of Tucson — Orient of Arizona. Building better men through Masonic education, charity, and brotherhood since 1882.
          </p>
        </div>
        <div>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)', marginBottom: '1rem' }}>Navigation</p>
          {['About', 'Degrees', 'Events', 'Officers', 'Gallery', 'News', 'Join', 'Donate', 'Contact'].map(l => (
            <a key={l} href={`#${l.toLowerCase()}`} style={{ display: 'block', fontFamily: 'var(--font-body)', fontSize: '0.88rem', color: 'rgba(255,255,255,0.5)', textDecoration: 'none', marginBottom: '0.4rem', transition: 'color 0.2s' }}
              onMouseOver={e => e.target.style.color='var(--gold)'} onMouseOut={e => e.target.style.color='rgba(255,255,255,0.5)'}>{l}</a>
          ))}
        </div>
        <div>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.15em', textTransform: 'uppercase', color: 'var(--gold)', marginBottom: '1rem' }}>Contact</p>
          <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.88rem', color: 'rgba(255,255,255,0.5)', lineHeight: 1.8, margin: 0 }}>
            176 N. Stone Avenue<br/>Tucson, AZ 85701<br/><br/>
            (520) 623-9270<br/>
            <a href="mailto:secretary@tucsonscottishrite.org" style={{ color: 'rgba(255,255,255,0.5)', textDecoration: 'none' }}>secretary@tucsonscottishrite.org</a>
          </p>
        </div>
      </div>
      <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.78rem', color: 'rgba(255,255,255,0.3)', margin: 0 }}>
          © {new Date().getFullYear()} Scottish Rite of Freemasonry, Valley of Tucson — Orient of Arizona, Southern Jurisdiction, USA
        </p>
        <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.78rem', color: 'rgba(255,255,255,0.25)', margin: 0 }}>Deus Meumque Jus</p>
      </div>
    </div>
  </footer>
);

Object.assign(window, { SRMembership, SRDonate, SRContact, SRFooter });
