import { motion } from "framer-motion"

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background gradient orbs */}
      <div className="absolute top-1/4 -left-32 w-96 h-96 bg-noesis-cyan/10 rounded-full blur-[128px] pointer-events-none" />
      <div className="absolute bottom-1/4 -right-32 w-96 h-96 bg-noesis-magenta/10 rounded-full blur-[128px] pointer-events-none" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-noesis-purple/5 rounded-full blur-[200px] pointer-events-none" />

      {/* Grid overlay */}
      <div
        className="absolute inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `linear-gradient(rgba(0,240,255,0.3) 1px, transparent 1px), linear-gradient(90deg, rgba(0,240,255,0.3) 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
        }}
      />

      <div className="relative z-10 text-center px-6 max-w-5xl mx-auto">
        {/* Eyebrow */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2.6, duration: 0.6 }}
          className="mb-6"
        >
          <span className="inline-block px-4 py-1.5 text-xs font-semibold tracking-[0.25em] uppercase text-noesis-cyan border border-noesis-cyan/30 rounded-full bg-noesis-cyan/5">
            Worlds Worth Fighting For
          </span>
        </motion.div>

        {/* Main heading */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 2.8, duration: 0.8 }}
          className="font-display text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-black leading-[0.9] tracking-tight mb-8"
        >
          <span className="text-white">CRAFTING</span>
          <br />
          <span className="bg-gradient-to-r from-noesis-cyan via-noesis-purple to-noesis-magenta bg-clip-text text-transparent">
            LEGENDARY
          </span>
          <br />
          <span className="text-white">GAMES</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 3.1, duration: 0.6 }}
          className="text-lg md:text-xl text-noesis-muted max-w-2xl mx-auto mb-12 leading-relaxed"
        >
          We build immersive experiences that push the boundaries of interactive storytelling.
          Every pixel, every mechanic, every moment — designed to captivate.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 3.4, duration: 0.6 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4"
        >
          <a
            href="#games"
            className="group relative px-8 py-4 bg-gradient-to-r from-noesis-cyan to-noesis-magenta text-noesis-black font-bold text-sm tracking-wider uppercase rounded overflow-hidden transition-shadow duration-300 hover:shadow-[0_0_40px_rgba(0,240,255,0.3)]"
          >
            <span className="relative z-10">Explore Our Games</span>
          </a>
          <a
            href="#about"
            className="px-8 py-4 border border-noesis-border hover:border-noesis-cyan/50 text-noesis-text font-semibold text-sm tracking-wider uppercase rounded transition-all duration-300 hover:shadow-[0_0_20px_rgba(0,240,255,0.1)]"
          >
            Our Story
          </a>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 4, duration: 0.6 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            className="flex flex-col items-center gap-2"
          >
            <span className="text-[10px] tracking-[0.3em] uppercase text-noesis-muted">Scroll</span>
            <svg width="16" height="24" viewBox="0 0 16 24" fill="none" className="text-noesis-cyan/50">
              <rect x="1" y="1" width="14" height="22" rx="7" stroke="currentColor" strokeWidth="1.5" />
              <motion.circle
                cx="8"
                cy="8"
                r="2"
                fill="currentColor"
                animate={{ cy: [8, 16, 8] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              />
            </svg>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
