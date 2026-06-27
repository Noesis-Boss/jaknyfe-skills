import { motion } from "framer-motion"

const footerLinks = {
  Games: [
    { label: "Abyssal Drift", href: "#" },
    { label: "Hollow Meridian", href: "#" },
    { label: "Neon Vector", href: "#" },
    { label: "Quiet Protocol", href: "#" },
  ],
  Company: [
    { label: "About Us", href: "#about" },
    { label: "Careers", href: "#" },
    { label: "Press Kit", href: "#" },
    { label: "Blog", href: "#" },
  ],
  Support: [
    { label: "Help Center", href: "#" },
    { label: "Community", href: "#" },
    { label: "Bug Reports", href: "#" },
    { label: "Contact", href: "#contact" },
  ],
  Legal: [
    { label: "Privacy Policy", href: "#" },
    { label: "Terms of Service", href: "#" },
    { label: "Cookie Policy", href: "#" },
  ],
}

export default function Footer() {
  return (
    <footer className="relative border-t border-noesis-border/30 bg-noesis-black">
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-10">
          {/* Brand column */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="col-span-2 md:col-span-1"
          >
            <div className="flex items-center gap-2 mb-4">
              <svg width="28" height="28" viewBox="0 0 80 80">
                <polygon
                  points="40,5 75,65 5,65"
                  fill="none"
                  stroke="url(#footerLogoGrad)"
                  strokeWidth="3"
                />
                <defs>
                  <linearGradient id="footerLogoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stopColor="#00f0ff" />
                    <stop offset="100%" stopColor="#ff00aa" />
                  </linearGradient>
                </defs>
              </svg>
              <span className="font-display text-sm font-bold tracking-[0.2em] text-white">
                NOESIS
              </span>
            </div>
            <p className="text-xs text-noesis-muted leading-relaxed max-w-[200px]">
              Worlds Worth Fighting For. Independent game studio crafting legendary experiences.
            </p>
          </motion.div>

          {/* Link columns */}
          {Object.entries(footerLinks).map(([category, links], i) => (
            <motion.div
              key={category}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 + i * 0.05, duration: 0.5 }}
            >
              <h4 className="font-display text-xs font-bold tracking-[0.2em] uppercase text-white mb-4">
                {category}
              </h4>
              <ul className="space-y-2.5">
                {links.map((link) => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      className="text-sm text-noesis-muted hover:text-noesis-cyan transition-colors duration-300"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>

        {/* Bottom bar */}
        <div className="mt-16 pt-8 border-t border-noesis-border/20 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-noesis-muted">
            © {new Date().getFullYear()} Noesis Games. All rights reserved.
          </p>
          <p className="text-xs text-noesis-muted/50">
            Crafted with passion and pixels.
          </p>
        </div>
      </div>
    </footer>
  )
}
