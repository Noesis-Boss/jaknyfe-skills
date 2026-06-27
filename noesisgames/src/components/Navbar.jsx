import { useState, useEffect } from "react"
import { motion } from "framer-motion"

const navLinks = [
  { label: "Games", href: "#games" },
  { label: "About", href: "#about" },
  { label: "Features", href: "#features" },
  { label: "Contact", href: "#contact" },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50)
    window.addEventListener("scroll", onScroll)
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, delay: 2.4 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${
        scrolled
          ? "bg-noesis-black/80 backdrop-blur-xl border-b border-noesis-border/50"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <a href="#" className="flex items-center gap-3 group">
          <svg width="36" height="36" viewBox="0 0 80 80" className="shrink-0">
            <polygon
              points="40,5 75,65 5,65"
              fill="none"
              stroke="url(#navLogoGrad)"
              strokeWidth="3"
              className="group-hover:stroke-noesis-magenta transition-colors duration-300"
            />
            <defs>
              <linearGradient id="navLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00f0ff" />
                <stop offset="100%" stopColor="#ff00aa" />
              </linearGradient>
            </defs>
          </svg>
          <span className="font-display text-lg font-bold tracking-[0.2em] text-white">
            NOESIS
          </span>
        </a>

        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              className="text-sm font-medium text-noesis-muted hover:text-noesis-cyan transition-colors duration-300 tracking-wider uppercase"
            >
              {link.label}
            </a>
          ))}
          <a
            href="#contact"
            className="ml-4 px-5 py-2 text-sm font-semibold tracking-wider uppercase bg-gradient-to-r from-noesis-cyan to-noesis-magenta text-noesis-black rounded hover:shadow-[0_0_20px_rgba(0,240,255,0.3)] transition-shadow duration-300"
          >
            Play Now
          </a>
        </div>

        {/* Mobile Toggle */}
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="md:hidden flex flex-col gap-1.5 p-2"
          aria-label="Toggle menu"
        >
          <span className={`block w-6 h-0.5 bg-white transition-all duration-300 ${mobileOpen ? "rotate-45 translate-y-2" : ""}`} />
          <span className={`block w-6 h-0.5 bg-white transition-all duration-300 ${mobileOpen ? "opacity-0" : ""}`} />
          <span className={`block w-6 h-0.5 bg-white transition-all duration-300 ${mobileOpen ? "-rotate-45 -translate-y-2" : ""}`} />
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          exit={{ opacity: 0, height: 0 }}
          className="md:hidden bg-noesis-dark/95 backdrop-blur-xl border-t border-noesis-border/50"
        >
          <div className="px-6 py-6 flex flex-col gap-4">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                onClick={() => setMobileOpen(false)}
                className="text-sm font-medium text-noesis-muted hover:text-noesis-cyan transition-colors tracking-wider uppercase py-2"
              >
                {link.label}
              </a>
            ))}
            <a
              href="#contact"
              onClick={() => setMobileOpen(false)}
              className="mt-2 px-5 py-3 text-sm font-semibold tracking-wider uppercase bg-gradient-to-r from-noesis-cyan to-noesis-magenta text-noesis-black rounded text-center"
            >
              Play Now
            </a>
          </div>
        </motion.div>
      )}
    </motion.nav>
  )
}
