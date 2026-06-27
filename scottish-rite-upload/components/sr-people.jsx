
// Officers, News, Gallery sections

// ── OFFICERS ───────────────────────────────────────────────────────────────
const SROfficers = () => {
  const officers = [
    { title: 'Thrice Potent Master', name: 'Ill. John A. Martinez, 33°', body: 'Lodge of Perfection' },
    { title: 'Wise Master', name: 'Ill. Robert T. Collins, 32°', body: 'Chapter of Rose Croix' },
    { title: 'Commander', name: 'Ill. David L. Hernandez, 32°', body: 'Council of Kadosh' },
    { title: 'Master of Kadosh', name: 'Ill. William R. Stone, 32°', body: 'Consistory' },
    { title: 'Secretary General', name: 'Ill. Frank E. Torres, 33°', body: 'Valley of Tucson' },
    { title: 'Treasurer General', name: 'Bro. James C. Wheeler, 32°', body: 'Valley of Tucson' },
    { title: 'Personal Representative', name: 'Ill. Thomas B. Garcia, 33°', body: 'Supreme Council' },
    { title: 'Almoner', name: 'Bro. Michael D. Ruiz, 32°', body: 'Valley of Tucson' },
  ];

  return (
    <section id="officers" data-screen-label="Officers" style={{ background: 'var(--navy)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <SectionHeader light eyebrow="Leadership" title="Officers of the Valley" subtitle="Our Valley is guided by dedicated Brothers who serve with honor and commitment." />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '1.25rem' }}>
          {officers.map((o, i) => (
            <div key={i} style={{
              border: '1px solid rgba(184,149,58,0.25)',
              borderTop: '3px solid var(--gold)',
              borderRadius: 8, padding: '1.5rem',
              background: 'rgba(255,255,255,0.03)',
              transition: 'background 0.25s, transform 0.25s',
            }}
              onMouseOver={e => { e.currentTarget.style.background = 'rgba(184,149,58,0.08)'; e.currentTarget.style.transform = 'translateY(-3px)'; }}
              onMouseOut={e => { e.currentTarget.style.background = 'rgba(255,255,255,0.03)'; e.currentTarget.style.transform = 'none'; }}>
              <div style={{ width: 48, height: 48, borderRadius: '50%', background: 'rgba(184,149,58,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>
                <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="var(--gold)" strokeWidth="1.5">
                  <circle cx="11" cy="8" r="4"/><path d="M3 20c0-4 3.6-7 8-7s8 3 8 7"/>
                </svg>
              </div>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.7rem', letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--gold)', margin: '0 0 0.35rem', fontWeight: 700 }}>{o.title}</p>
              <p style={{ fontFamily: 'var(--font-display)', fontSize: '1.05rem', fontWeight: 600, color: '#fff', margin: '0 0 0.25rem' }}>{o.name}</p>
              <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.8rem', color: 'rgba(255,255,255,0.4)', margin: 0 }}>{o.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

// ── GALLERY ────────────────────────────────────────────────────────────────
const SRGallery = () => {
  const [lightbox, setLightbox] = React.useState(null);
  const photos = [
    { label: 'Reunion Ceremony', aspect: '4/3' },
    { label: 'Cathedral Exterior', aspect: '3/4' },
    { label: 'Degree Conferral', aspect: '4/3' },
    { label: 'Brotherhood Dinner', aspect: '4/3' },
    { label: 'Officer Installation', aspect: '3/4' },
    { label: 'Temple Interior', aspect: '4/3' },
    { label: 'Annual Banquet', aspect: '4/3' },
    { label: 'Charitable Event', aspect: '4/3' },
  ];

  const hues = [210, 220, 215, 225, 205, 218, 212, 222];

  return (
    <section id="gallery" data-screen-label="Gallery" style={{ background: 'var(--cream)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <SectionHeader eyebrow="Photo Gallery" title="Life in Our Valley" subtitle="Moments of brotherhood, ceremony, and service from the Valley of Tucson." />
        <div style={{ columns: '3 220px', gap: '1rem' }}>
          {photos.map((p, i) => (
            <div key={i}
              onClick={() => setLightbox(i)}
              style={{
                marginBottom: '1rem', breakInside: 'avoid',
                borderRadius: 8, overflow: 'hidden', cursor: 'pointer',
                position: 'relative',
              }}>
              <div style={{
                background: `repeating-linear-gradient(${30 + i * 15}deg, hsl(${hues[i]},18%,${78 - i * 2}%) 0px, hsl(${hues[i]},18%,${78 - i * 2}%) 12px, hsl(${hues[i]},14%,${85 - i * 2}%) 12px, hsl(${hues[i]},14%,${85 - i * 2}%) 24px)`,
                aspectRatio: p.aspect,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                position: 'relative',
                transition: 'filter 0.25s',
              }}>
                <div style={{ background: 'rgba(255,255,255,0.75)', padding: '0.4rem 0.75rem', borderRadius: 4 }}>
                  <span style={{ fontFamily: 'monospace', fontSize: '0.72rem', color: '#555' }}>{p.label}</span>
                </div>
                <div style={{
                  position: 'absolute', inset: 0,
                  background: 'rgba(26,26,46,0)', display: 'flex', alignItems: 'center', justifyContent: 'center',
                  transition: 'background 0.25s',
                }} className="sr-gallery-overlay"
                  onMouseOver={e => e.currentTarget.style.background = 'rgba(26,26,46,0.4)'}
                  onMouseOut={e => e.currentTarget.style.background = 'rgba(26,26,46,0)'}>
                  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="white" strokeWidth="2" style={{ opacity: 0, transition: 'opacity 0.25s' }} className="sr-zoom-icon">
                    <circle cx="14" cy="14" r="7"/><line x1="19" y1="19" x2="28" y2="28"/>
                    <line x1="11" y1="14" x2="17" y2="14"/><line x1="14" y1="11" x2="14" y2="17"/>
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lightbox */}
      {lightbox !== null && (
        <div onClick={() => setLightbox(null)} style={{
          position: 'fixed', inset: 0, zIndex: 2000,
          background: 'rgba(0,0,0,0.92)', display: 'flex', alignItems: 'center', justifyContent: 'center',
          cursor: 'zoom-out',
        }}>
          <button onClick={e => { e.stopPropagation(); setLightbox(l => (l - 1 + photos.length) % photos.length); }}
            style={{ position: 'fixed', left: '2rem', top: '50%', transform: 'translateY(-50%)', background: 'rgba(255,255,255,0.1)', border: 'none', color: '#fff', width: 48, height: 48, borderRadius: '50%', cursor: 'pointer', fontSize: '1.4rem' }}>‹</button>
          <div onClick={e => e.stopPropagation()} style={{
            maxWidth: '80vw', maxHeight: '80vh',
            background: `repeating-linear-gradient(${30 + lightbox * 15}deg, hsl(${hues[lightbox]},18%,78%) 0px, hsl(${hues[lightbox]},18%,78%) 12px, hsl(${hues[lightbox]},14%,85%) 12px, hsl(${hues[lightbox]},14%,85%) 24px)`,
            borderRadius: 8, width: 600, height: 400,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <div style={{ background: 'rgba(255,255,255,0.8)', padding: '0.5rem 1rem', borderRadius: 4 }}>
              <span style={{ fontFamily: 'monospace', fontSize: '0.85rem', color: '#444' }}>{photos[lightbox].label}</span>
            </div>
          </div>
          <button onClick={e => { e.stopPropagation(); setLightbox(l => (l + 1) % photos.length); }}
            style={{ position: 'fixed', right: '2rem', top: '50%', transform: 'translateY(-50%)', background: 'rgba(255,255,255,0.1)', border: 'none', color: '#fff', width: 48, height: 48, borderRadius: '50%', cursor: 'pointer', fontSize: '1.4rem' }}>›</button>
          <div style={{ position: 'fixed', bottom: '2rem', color: 'rgba(255,255,255,0.5)', fontFamily: 'var(--font-body)', fontSize: '0.85rem' }}>
            {lightbox + 1} / {photos.length} — {photos[lightbox].label}
          </div>
        </div>
      )}
    </section>
  );
};

// ── NEWS ───────────────────────────────────────────────────────────────────
const SRNews = () => {
  const posts = [
    { date: 'April 10, 2026', category: 'Charity', title: 'Valley Raises $18,000 for RiteCare Childhood Language Program', excerpt: 'Thanks to the generosity of our Brothers and their families, this year\'s spring gala exceeded all expectations and will fund two full years of speech therapy services.' },
    { date: 'March 28, 2026', category: 'Degrees', title: 'Spring Reunion Welcomes 14 New 32° Master Masons', excerpt: 'On a beautiful Tucson morning, the Valley conferred the degrees of the Scottish Rite upon 14 deserving candidates, strengthening our Brotherhood.' },
    { date: 'March 1, 2026', category: 'Community', title: 'Valley Partners with Tucson Unified School District', excerpt: 'Our new partnership will bring reading and literacy support to underserved elementary schools across Southern Arizona starting this fall.' },
  ];

  return (
    <section id="news" data-screen-label="News" style={{ background: 'var(--navy)', padding: '6rem 1.5rem' }}>
      <div style={{ maxWidth: 1100, margin: '0 auto' }}>
        <SectionHeader light eyebrow="Latest News" title="From the Valley" subtitle="" />
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.5rem' }}>
          {posts.map((p, i) => (
            <article key={i} style={{
              background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.09)',
              borderRadius: 8, overflow: 'hidden',
              transition: 'transform 0.25s, box-shadow 0.25s', cursor: 'pointer',
            }}
              onMouseOver={e => { e.currentTarget.style.transform = 'translateY(-5px)'; e.currentTarget.style.boxShadow = '0 16px 40px rgba(0,0,0,0.3)'; }}
              onMouseOut={e => { e.currentTarget.style.transform = 'none'; e.currentTarget.style.boxShadow = 'none'; }}>
              <div style={{
                height: 160,
                background: `repeating-linear-gradient(${40 + i * 20}deg, rgba(184,149,58,0.08) 0px, rgba(184,149,58,0.08) 8px, transparent 8px, transparent 16px)`,
                borderBottom: '1px solid rgba(255,255,255,0.07)',
              }}/>
              <div style={{ padding: '1.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.7rem', fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--gold)' }}>{p.category}</span>
                  <span style={{ color: 'rgba(255,255,255,0.25)', fontSize: '0.7rem' }}>·</span>
                  <span style={{ fontFamily: 'var(--font-body)', fontSize: '0.78rem', color: 'rgba(255,255,255,0.4)' }}>{p.date}</span>
                </div>
                <h3 style={{ fontFamily: 'var(--font-display)', fontSize: '1.2rem', fontWeight: 600, color: '#fff', margin: '0 0 0.75rem', lineHeight: 1.3 }}>{p.title}</h3>
                <p style={{ fontFamily: 'var(--font-body)', fontSize: '0.88rem', color: 'rgba(255,255,255,0.55)', lineHeight: 1.65, margin: 0 }}>{p.excerpt}</p>
                <div style={{ marginTop: '1.25rem', color: 'var(--gold)', fontFamily: 'var(--font-body)', fontSize: '0.82rem', fontWeight: 600 }}>Read more →</div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
};

Object.assign(window, { SROfficers, SRGallery, SRNews });
