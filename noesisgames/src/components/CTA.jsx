import { motion } from "framer-motion"
import { useState } from "react"

export default function CTA() {
  const [email, setEmail] = useState("")
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (email) {
      setSubmitted(true)
      setEmail("")
    }
  }

  return (
    <section id="contact" className="relative py-32 px-6 overflow-hidden">
      {/* Background effects */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[400px] bg-gradient-to-r from-noesis-cyan/5 via-noesis-purple/10 to-noesis-magenta/5 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-4xl mx-auto relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          {/* Decorative line */}
          <div className="flex items-center justify-center gap-4 mb-8">
            <div className="w-16 h-px bg-gradient-to-r from-transparent to-noesis-cyan/50" />
            <svg width="24" height="24" viewBox="0 0 80 80">
              <polygon
                points="40,5 75,65 5,65"
                fill="none"
                stroke="currentColor"
                strokeWidth="4"
                className="text-noesis-cyan/50"
              />
            </svg>
            <div className="w-16 h-px bg-gradient-to-l from-transparent to-noesis-magenta/50" />
          </div>

          <h2 className="font-display text-4xl md:text-6xl font-black text-white mb-6 tracking-tight leading-[1.1]">
            Stay in the{" "}
            <span className="bg-gradient-to-r from-noesis-cyan to-noesis-magenta bg-clip-text text-transparent">
              Loop
            </span>
          </h2>

          <p className="text-lg text-noesis-muted max-w-xl mx-auto mb-12 leading-relaxed">
            Get exclusive updates, early access, and behind-the-scenes content from Noesis Games.
            No spam. Just signal.
          </p>

          {/* Newsletter form */}
          {!submitted ? (
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-lg mx-auto">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
                className="flex-1 px-6 py-4 bg-noesis-card border border-noesis-border rounded text-white placeholder:text-noesis-muted/50 focus:outline-none focus:border-noesis-cyan/50 transition-colors duration-300 text-sm"
              />
              <button
                type="submit"
                className="px-8 py-4 bg-gradient-to-r from-noesis-cyan to-noesis-magenta text-noesis-black font-bold text-sm tracking-wider uppercase rounded hover:shadow-[0_0_30px_rgba(0,240,255,0.3)] transition-shadow duration-300 whitespace-nowrap"
              >
                Subscribe
              </button>
            </form>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="inline-flex items-center gap-3 px-8 py-4 bg-noesis-card border border-noesis-cyan/30 rounded"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" className="text-noesis-cyan">
                <path d="M10 0C4.48 0 0 4.48 0 10s4.48 10 10 10 10-4.48 10-10S15.52 0 10 0zm-2 15l-5-5 1.41-1.41L8 12.17l7.59-7.59L17 6l-9 9z" fill="currentColor" />
              </svg>
              <span className="text-sm font-semibold text-white tracking-wider">
                You're in. Welcome to the inner circle.
              </span>
            </motion.div>
          )}

          {/* Social links */}
          <div className="mt-16 flex items-center justify-center gap-6">
            {[
              { name: "Twitter / X", href: "#", icon: "𝕏" },
              { name: "Discord", href: "#", icon: "🎮" },
              { name: "YouTube", href: "#", icon: "▶" },
              { name: "Instagram", href: "#", icon: "📷" },
            ].map((social) => (
              <a
                key={social.name}
                href={social.href}
                aria-label={social.name}
                className="w-12 h-12 flex items-center justify-center rounded-full border border-noesis-border hover:border-noesis-cyan/50 text-noesis-muted hover:text-noesis-cyan transition-all duration-300 text-lg hover:shadow-[0_0_15px_rgba(0,240,255,0.15)]"
              >
                {social.icon}
              </a>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}
