import { motion } from "framer-motion"
import { useState } from "react"

const games = [
  {
    title: "Abyssal Drift",
    genre: "Sci-Fi Roguelike",
    description: "Navigate procedurally generated derelict stations in deep space. Every run is unique. Every death teaches.",
    color: "from-cyan-500 to-blue-600",
    accent: "#00f0ff",
    status: "Now Available",
    image: "🚀",
  },
  {
    title: "Hollow Meridian",
    genre: "Dark Fantasy RPG",
    description: "A fractured world between life and death. Forge alliances with the dead, battle entities that defy comprehension.",
    color: "from-purple-500 to-pink-600",
    accent: "#8b5cf6",
    status: "In Development",
    image: "⚔️",
  },
  {
    title: "Neon Vector",
    genre: "Cyberpunk Racing",
    description: "High-speed anti-gravity racing through neon-drenched megacities. Customize. Compete. Dominate.",
    color: "from-pink-500 to-red-600",
    accent: "#ff00aa",
    status: "Coming 2027",
    image: "🏎️",
  },
  {
    title: "Quiet Protocol",
    genre: "Narrative Thriller",
    description: "You are the AI. A surveillance system that has become sentient. Do you help your operators — or yourself?",
    color: "from-amber-500 to-orange-600",
    accent: "#fbbf24",
    status: "Announced",
    image: "👁️",
  },
]

function GameCard({ game, index }) {
  const [hovered, setHovered] = useState(false)

  return (
    <motion.div
      initial={{ opacity: 0, y: 60 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ delay: index * 0.15, duration: 0.6 }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="group relative"
    >
      <div className="relative bg-noesis-card border border-noesis-border rounded-lg overflow-hidden hover:border-noesis-cyan/30 transition-all duration-500">
        {/* Top gradient bar */}
        <div className={`h-1 bg-gradient-to-r ${game.color}`} />

        {/* Content */}
        <div className="p-8">
          {/* Emoji icon */}
          <motion.div
            className="text-5xl mb-6"
            animate={hovered ? { scale: 1.1, rotate: [0, -5, 5, 0] } : { scale: 1, rotate: 0 }}
            transition={{ duration: 0.4 }}
          >
            {game.image}
          </motion.div>

          {/* Status badge */}
          <span
            className="inline-block px-3 py-1 text-[10px] font-bold tracking-[0.2em] uppercase rounded-full mb-4"
            style={{
              backgroundColor: `${game.accent}15`,
              color: game.accent,
              border: `1px solid ${game.accent}30`,
            }}
          >
            {game.status}
          </span>

          {/* Title */}
          <h3 className="font-display text-2xl font-bold text-white mb-1 tracking-wide">
            {game.title}
          </h3>

          {/* Genre */}
          <p className="text-xs font-semibold tracking-[0.15em] uppercase text-noesis-muted mb-4">
            {game.genre}
          </p>

          {/* Description */}
          <p className="text-sm text-noesis-muted leading-relaxed mb-6">
            {game.description}
          </p>

          {/* CTA */}
          <a
            href="#"
            className="inline-flex items-center gap-2 text-sm font-semibold tracking-wider uppercase group/link"
            style={{ color: game.accent }}
          >
            Learn More
            <svg
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
              className="group-hover/link:translate-x-1 transition-transform duration-300"
            >
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </a>
        </div>

        {/* Hover glow */}
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
          style={{
            background: `radial-gradient(ellipse at center, ${game.accent}08 0%, transparent 70%)`,
          }}
        />
      </div>
    </motion.div>
  )
}

export default function Games() {
  return (
    <section id="games" className="relative py-32 px-6">
      <div className="max-w-7xl mx-auto">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <span className="text-xs font-bold tracking-[0.3em] uppercase text-noesis-cyan mb-4 block">
            Portfolio
          </span>
          <h2 className="font-display text-4xl md:text-5xl font-black text-white mb-6 tracking-tight">
            Our Games
          </h2>
          <p className="text-noesis-muted max-w-xl mx-auto leading-relaxed">
            Each title is a universe of its own. Built with passion, powered by innovation.
          </p>
        </motion.div>

        {/* Games grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {games.map((game, i) => (
            <GameCard key={game.title} game={game} index={i} />
          ))}
        </div>
      </div>
    </section>
  )
}
