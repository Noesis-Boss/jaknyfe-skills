import { motion } from "framer-motion"

const stats = [
  { value: "12+", label: "Years Experience" },
  { value: "4", label: "Titles Shipped" },
  { value: "2M+", label: "Players Worldwide" },
  { value: "35", label: "Team Members" },
]

export default function About() {
  return (
    <section id="about" className="relative py-32 px-6 overflow-hidden">
      {/* Background accent */}
      <div className="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-noesis-purple/5 to-transparent pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left: Visual */}
          <motion.div
            initial={{ opacity: 0, x: -40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="relative aspect-square max-w-lg mx-auto">
              {/* Decorative rings */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-full h-full border border-noesis-border/30 rounded-full" />
              </div>
              <div className="absolute inset-8 flex items-center justify-center">
                <div className="w-full h-full border border-noesis-cyan/10 rounded-full" />
              </div>
              <div className="absolute inset-16 flex items-center justify-center">
                <div className="w-full h-full border border-noesis-magenta/10 rounded-full" />
              </div>

              {/* Center content */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="text-center">
                  <svg width="100" height="100" viewBox="0 0 80 80" className="mx-auto mb-4">
                    <polygon
                      points="40,5 75,65 5,65"
                      fill="none"
                      stroke="url(#aboutLogoGrad)"
                      strokeWidth="2"
                    />
                    <defs>
                      <linearGradient id="aboutLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#00f0ff" />
                        <stop offset="100%" stopColor="#ff00aa" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <span className="font-display text-3xl font-black tracking-[0.3em] text-white">
                    NOESIS
                  </span>
                </div>
              </div>

              {/* Floating dots */}
              <motion.div
                animate={{ y: [-10, 10, -10] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                className="absolute top-12 right-12 w-3 h-3 bg-noesis-cyan rounded-full shadow-[0_0_10px_rgba(0,240,255,0.5)]"
              />
              <motion.div
                animate={{ y: [10, -10, 10] }}
                transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                className="absolute bottom-16 left-12 w-2 h-2 bg-noesis-magenta rounded-full shadow-[0_0_10px_rgba(255,0,170,0.5)]"
              />
              <motion.div
                animate={{ y: [-8, 12, -8] }}
                transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
                className="absolute bottom-32 right-20 w-2 h-2 bg-noesis-gold rounded-full shadow-[0_0_10px_rgba(251,191,36,0.5)]"
              />
            </div>
          </motion.div>

          {/* Right: Content */}
          <motion.div
            initial={{ opacity: 0, x: 40 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            <span className="text-xs font-bold tracking-[0.3em] uppercase text-noesis-magenta mb-4 block">
              Who We Are
            </span>
            <h2 className="font-display text-4xl md:text-5xl font-black text-white mb-8 tracking-tight leading-[1.1]">
              We Don't Just
              <br />
              <span className="bg-gradient-to-r from-noesis-cyan to-noesis-magenta bg-clip-text text-transparent">
                Make Games.
              </span>
            </h2>
            <p className="text-noesis-muted leading-relaxed mb-6 text-lg">
              Noesis Games is an independent studio founded on a simple belief: games are the
              most powerful medium for human connection. We craft experiences that linger
              long after the screen goes dark.
            </p>
            <p className="text-noesis-muted leading-relaxed mb-12">
              From sprawling sci-fi epics to intimate narrative journeys, our team of 35
              passionate developers, artists, and storytellers pour everything into every project.
              No shortcuts. No compromises.
            </p>

            {/* Stats */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
              {stats.map((stat, i) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: 0.4 + i * 0.1, duration: 0.5 }}
                  className="text-center sm:text-left"
                >
                  <div className="font-display text-2xl md:text-3xl font-black text-white mb-1">
                    {stat.value}
                  </div>
                  <div className="text-xs font-semibold tracking-wider uppercase text-noesis-muted">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
