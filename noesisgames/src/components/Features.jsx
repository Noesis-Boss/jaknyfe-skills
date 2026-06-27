import { motion } from "framer-motion"

const features = [
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 2L2 7l10 5 10-5-10-5z" />
        <path d="M2 17l10 5 10-5" />
        <path d="M2 12l10 5 10-5" />
      </svg>
    ),
    title: "Immersive Worlds",
    description: "Hand-crafted environments with obsessive attention to detail. Every texture tells a story.",
    color: "#00f0ff",
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 6v6l4 2" />
      </svg>
    ),
    title: "Dynamic Systems",
    description: "Procedural generation meets hand-tuned design. No two playthroughs are ever the same.",
    color: "#8b5cf6",
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
        <circle cx="9" cy="7" r="4" />
        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
      </svg>
    ),
    title: "Community First",
    description: "Built by players, for players. We listen, iterate, and grow with our community.",
    color: "#ff00aa",
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
      </svg>
    ),
    title: "Award-Winning",
    description: "Recognized by industry peers and players alike for innovation and excellence.",
    color: "#fbbf24",
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="2" ry="2" />
        <line x1="8" y1="21" x2="16" y2="21" />
        <line x1="12" y1="17" x2="12" y2="21" />
      </svg>
    ),
    title: "Cross-Platform",
    description: "Play anywhere. PC, console, or mobile — your progress follows you seamlessly.",
    color: "#00f0ff",
  },
  {
    icon: (
      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      </svg>
    ),
    title: "Rich Narratives",
    description: "Stories that matter. Characters you'll remember. Choices that have real consequences.",
    color: "#8b5cf6",
  },
]

export default function Features() {
  return (
    <section id="features" className="relative py-32 px-6">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-noesis-black via-noesis-dark to-noesis-black pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <span className="text-xs font-bold tracking-[0.3em] uppercase text-noesis-gold mb-4 block">
            Why Noesis
          </span>
          <h2 className="font-display text-4xl md:text-5xl font-black text-white mb-6 tracking-tight">
            Built Different
          </h2>
          <p className="text-noesis-muted max-w-xl mx-auto leading-relaxed">
            Every decision we make serves the player experience. Here's what sets us apart.
          </p>
        </motion.div>

        {/* Features grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-30px" }}
              transition={{ delay: i * 0.1, duration: 0.5 }}
              className="group relative bg-noesis-card/50 border border-noesis-border/50 rounded-lg p-8 hover:border-noesis-cyan/20 transition-all duration-500"
            >
              {/* Icon */}
              <div
                className="mb-6 transition-colors duration-300"
                style={{ color: feature.color }}
              >
                {feature.icon}
              </div>

              {/* Title */}
              <h3 className="font-display text-lg font-bold text-white mb-3 tracking-wide">
                {feature.title}
              </h3>

              {/* Description */}
              <p className="text-sm text-noesis-muted leading-relaxed">
                {feature.description}
              </p>

              {/* Hover glow */}
              <div
                className="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                style={{
                  background: `radial-gradient(ellipse at top left, ${feature.color}06 0%, transparent 60%)`,
                }}
              />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
