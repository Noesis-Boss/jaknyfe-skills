// About, Degrees, Events sections

import React from 'react';
export const Ornament = () => (
  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', margin: '0 0 1.5rem' }}>
    <div style={{ flex: 1, height: 1, background: 'var(--divider)' }}/>
    <svg width="18" height="18" viewBox="0 0 18 18" fill="var(--gold)">
      <polygon points="9,1 11,7 17,7 12,11 14,17 9,13 4,17 6,11 1,7 7,7"/>
    </svg>
    <div style={{ flex: 1, height: 1, background: 'var(--divider)' }}/>
  </div>
);

export const SectionHeader = ({ eyebrow, title, subtitle, light }) => (
  <div style={{ textAlign: 'center', marginBottom: '3.5rem' }}>
    {eyebrow && <p style={{
      fontFamily: 'var(--font-body)', fontSize: '0.75rem', fontWeight: 700,
      letterSpacing: '0.2em', textTransform: 'uppercase',
      color: 'var(--gold)', marginBottom: '0.75rem',
    }}>{eyebrow}</p>}
    <h2 style={{
      fontFamily: 'var(--font-display)',
      fontSize: 'clamp(2rem, 4vw, 2.8rem)',
      fontWeight: 600, margin: '0 0 1rem',
      color: light ? '#fff' : 'var(--navy)',
      lineHeight: 1.15,
    }}>{title}</h2>
    {subtitle && <p style={{
      fontFamily: 'var(--font-body)',
      fontSize: '1.05rem', color: light ? 'rgba(255,255,255,0.7)' : 'var(--text-muted)',
      maxWidth: 560, margin: '0 auto', lineHeight: 1.7,
    }}>{subtitle}</p>}
    <div style={{ width: 48, height: 2, background: 'var(--gold)', margin: '1.5rem auto 0', borderRadius: 1 }}/>
  </div>
);

// ── ABOUT ──────────────────────────────────────────────────────────────────
export const SRAbout = () => {
  const pillars = [
    { icon: '⬟', title: 'Charity', text: "Supporting children's language disorders, scholarships, and community service throughout Southern Arizona." },
    { icon: '⬟', title: 'Justice', text: 'Committed to equity, brotherhood, and the fair treatment of all members of our society.' },
    { icon: '⬟', title: 'Tolerance', text: 'Welcoming men of every background, faith, and walk of life into our Valley.' },
    { icon: '⬟', title: 'Truth', text: 'Dedicating ourselves to the pursuit of knowledge, wisdom, and moral uprightness.' },
  ];

  return (
    <section id="about" data-screen-label="About" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <SectionHeader eyebrow="Our Valley" title="A Brotherhood Rooted in Tucson" subtitle="The Valley of Tucson has been a pillar of Freemasonry in Southern Arizona since 1882, uniting men of character through the 29 degrees of the Scottish Rite." />

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>
          {pillars.map(p => (
            <div key={p.title} className="sr-card-hover sr-card-hover-gold" style={{
              background: 'var(--card-bg)', borderRadius: 8,
              padding: '2rem 1.5rem', textAlign: 'center',
              border: '1px solid var(--card-border)',
            }}>
              <div style={{ width: 48, height: 48, borderRadius: '50%', background: 'rgba(212,168,83,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.25rem' }}>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="var(--gold)">
                  <polygon points="10,2 12.4,7.6 18.5,8.2 14,12.3 15.4,18.3 10,15.1 4.6,18.3 6,12.3 1.5,8.2 7.6,7.6"/>
                </svg>
              </div>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.3rem', fontWeight: 600, color: 'var(--navy)', margin: '0 0 0.75rem' }}>{p.title}</h3>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.65, margin: 0 }}>{p.text}</p>
            </div>
          ))}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4rem', alignItems: 'center' }} className="sr-two-col">
          <div>
            <Ornament />
            <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.9rem', fontWeight: 600, color: 'var(--navy)', margin: '0 0 1.25rem', lineHeight: 1.2 }}>
              The Ancient & Accepted Scottish Rite
            </h3>
            <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.97rem', color: 'var(--text-body)', lineHeight: 1.75, marginBottom: '1rem' }}>
              The Scottish Rite is one of the appendant bodies of Freemasonry that a Master Mason may join for further instruction in the philosophy of the fraternity. The Rite confers degrees from the 4th through the 32nd, with honorary membership at the 33rd.
            </p>
            <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.97rem', color: 'var(--text-body)', lineHeight: 1.75 }}>
              Each degree presents lessons of morality, philosophy, and allegory through dramatic presentation, deepening the candidate's understanding of the values at the heart of Freemasonry.
            </p>
          </div>
          <div style={{
            borderRadius: 8, overflow: 'hidden',
            background: 'repeating-linear-gradient(45deg, var(--stripe-a) 0px, var(--stripe-a) 10px, var(--stripe-b) 10px, var(--stripe-b) 20px)',
            height: 320, display: 'flex', alignItems: 'center', justifyContent: 'center',
            border: '1px solid var(--card-border)',
          }}>
            <div style={{ background: 'rgba(255,255,255,0.8)', padding: '0.6rem 1rem', borderRadius: 4 }}>
              <span style={{ fontFamily: 'monospace', fontSize: '0.8rem', color: '#666' }}>[ Valley of Tucson — historic photo ]</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

// ── DEGREES ────────────────────────────────────────────────────────────────
export const SRDegrees = () => {
  const [active, setActive] = React.useState(null);
  const degrees = [
    { num: '4°–14°', body: 'Lodge of Perfection', title: 'Ancient Craft Degrees', text: 'The first series explores the building of Solomon\'s Temple and teaches lessons of loyalty, duty, and the search for what was lost.' },
    { num: '15°–18°', body: 'Chapter of Rose Croix', title: 'Rose Croix Degrees', text: 'This series focuses on spiritual regeneration and the search for truth, culminating in the Knight of the Rose Croix.' },
    { num: '19°–28°', body: 'Council of Kadosh', title: 'Kadosh Degrees (19°-28°)', text: 'An examination of chivalry, civic duty, and the philosophic and social aspects of Masonry through a medieval lens, preparing for the chivalric virtues of the Knight of St. Andrew.' },
    { num: '29°', body: 'Knight of St. Andrew', title: 'Knight of St. Andrew', text: 'The 29th degree, Knight of St. Andrew, exemplifies the virtues of chivalry, loyalty to God and country, and faithfulness to one\'s obligations. This degree emphasizes the ideals of the Christian knight and the defense of the faith.' },
    { num: '30°', body: 'Council of Kadosh', title: 'Kadosh Degree (30°)', text: 'The Grand Kadosh degree, continuing the exploration of chivalric and philosophical truths.' },
    { num: '31°–32°', body: 'Consistory', title: 'Consistory Degrees', text: 'The culminating degrees of the Scottish Rite, conferring the title of Master of the Royal Secret and the 32° of Sublime Prince.' },
    { num: '33°', body: 'Supreme Council', title: 'Inspector General Honorary', text: 'The highest honor the Scottish Rite can bestow, conferred by the Supreme Council upon Brethren in recognition of outstanding service.' },
  ];
  return (
    <section id="degrees" data-screen-label="Degrees" style={{ background: 'var(--navy)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <SectionHeader light eyebrow="The 29 Degrees" title="Degrees of the Scottish Rite" subtitle="Each degree is a chapter in a journey of self-discovery, moral growth, and brotherhood." />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
          {degrees.map((d, i) => (
            <div key={i} onClick={() => setActive(active === i ? null : i)} className={`sr-degree-card ${active === i ? 'sr-degree-card-active' : ''}`} style={{
              border: `1px solid ${active === i ? 'var(--gold)' : 'rgba(255,255,255,0.1)'}`,
              borderRadius: 8, padding: '1.75rem 1.5rem', cursor: 'pointer',
            }}>
              <div style={{ fontFamily: 'var(--font-display)', fontSize: '2rem', color: 'var(--gold)', fontWeight: 700, marginBottom: '0.5rem' }}>{d.num}</div>
              <div style={{ fontFamily: 'var(--font-body)', fontSize: '0.72rem', letterSpacing: '0.12em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.45)', marginBottom: '0.75rem' }}>{d.body}</div>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.15rem', fontWeight: 600, color: '#fff', margin: '0 0 0.75rem', lineHeight: 1.25 }}>{d.title}</h3>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.88rem', color: 'rgba(255,255,255,0.6)', lineHeight: 1.65, margin: 0, maxHeight: active === i ? 200 : 0, overflow: 'hidden', transition: 'max-height 0.4s ease' }}>{d.text}</p>
              <div style={{ marginTop: active === i ? '1rem' : '0.5rem', color: 'var(--gold)', fontSize: '0.75rem', fontFamily: 'var(--font-body)', transition: 'margin 0.3s' }}>
                {active === i ? '▲ Close' : '▼ Learn more'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// ── EVENTS ─────────────────────────────────────────────────────────────────
export const SREvents = () => {
  const [calModal, setCalModal] = React.useState(false);
  const [events, setEvents] = React.useState([]);
  React.useEffect(() => {
    const container = document.getElementById('calendarwiz-container');
    if (!container || container.dataset.loaded) return;
    container.dataset.loaded = '1';
    const originalWrite = document.write;
    document.write = markup => {
      const parsed = new DOMParser().parseFromString(markup, 'text/html');
      const items = [...parsed.querySelectorAll('a[onclick*="popevent_"]')]
        .map(link => ({ title: link.textContent.trim(), date: link.nextElementSibling?.textContent.trim() }))
        .filter(item => item.title && item.date)
        .slice(0, 6);
      if (items.length) setEvents(items);
    };
    const script = document.createElement('script');
    script.src = '//www.calendarwiz.com/calendars/ucfeeder.php?crd=tucsonscottishrite&theme=Master%20Theme';
    script.onload = script.onerror = () => { document.write = originalWrite; };
    container.appendChild(script);
  }, []);

  return (<>
    <section id="events" data-screen-label="Events" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 900, margin: '0 auto' }}>
        <SectionHeader eyebrow="Calendar" title="Upcoming Events" subtitle="The Valley meets regularly throughout the year. All Master Masons in good standing are welcome." />
        <div id="calendarwiz-container" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem', minHeight: 120 }}>
          {events.map((event, index) => (
            <article key={`${event.title}-${event.date}-${index}`} style={{ background: '#fff', border: '1px solid var(--card-border)', borderTop: '3px solid var(--gold)', borderRadius: 6, padding: '1.25rem', boxShadow: '0 4px 14px rgba(15,31,61,0.06)' }}>
              <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', color: 'var(--navy)', margin: '0 0 0.65rem' }}>{event.title}</h3>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.82rem', color: 'var(--text-muted)', lineHeight: 1.5, margin: 0 }}>{event.date}</p>
            </article>
          ))}
        </div>
        <div style={{ textAlign: 'center', marginTop: '2.5rem' }}>
          <button onClick={() => setCalModal(true)} className="sr-btn-hover sr-btn-hover-outline" style={{
            background: 'none', border: '1px solid var(--navy)', color: 'var(--navy)',
            fontFamily: 'var(--font-body)', fontSize: '0.82rem', fontWeight: 700,
            letterSpacing: '0.1em', textTransform: 'uppercase',
            padding: '0.85rem 2rem', borderRadius: 4, cursor: 'pointer',
          }}>
            View Full Calendar
          </button>
        </div>
      </div>
    </section>
    {calModal && (
      <div onClick={() => setCalModal(false)} style={{ position: 'fixed', inset: 0, zIndex: 2000, background: 'rgba(0,0,0,0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '2rem' }}>
        <div onClick={e => e.stopPropagation()} style={{ background: 'var(--cream)', borderRadius: 10, width: '96vw', height: '94vh', maxWidth: 1400, display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 24px 80px rgba(0,0,0,0.4)' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1.25rem 1.75rem', borderBottom: '1px solid var(--divider)' }}>
            <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.5rem', fontWeight: 600, color: 'var(--navy)', margin: 0 }}>Full Calendar</h3>
            <button onClick={() => setCalModal(false)} aria-label="Close calendar" style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', fontSize: '1.5rem', lineHeight: 1, padding: '0.25rem' }}>×</button>
          </div>
          <iframe
            id="calendarwiz-modal-body"
            title="Full Valley of Tucson calendar"
            src="https://www.calendarwiz.com/calendars/calendar.php?crd=tucsonscottishrite&nolog=1&skiptitle=1&cid[]=285330&cid[]=285329&cid[]=285327&cid[]=285328&cid[]=285324&cid[]=285334"
            style={{ flex: 1, width: '100%', minHeight: 0, border: 0 }}
          />
        </div>
      </div>
    )}
  </>);
};

Object.assign(window, { SRAbout, SRDegrees, SREvents, SectionHeader, Ornament });
