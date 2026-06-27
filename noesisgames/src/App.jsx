import { useState, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import Navbar from "./components/Navbar"
import Hero from "./components/Hero"
import Games from "./components/Games"
import About from "./components/About"
import Features from "./components/Features"
import CTA from "./components/CTA"
import Footer from "./components/Footer"
import ParticleField from "./components/ParticleField"

function LoadingScreen({ onComplete }) {
  useEffect(() => {
    const timer = setTimeout(onComplete, 2200)
    return () => clearTimeout(timer)
  }, [onComplete])

  return (
    <motion.div
      className="fixed inset-0 z-[100] flex items-center justify-center bg-noesis-black"
      exit={{ opacity: 0 }}
      transition={{ duration: 0.6, ease: "easeInOut" }}
    >
      <div className="text-center">
        <motion.div
          initial={{ scale: 0.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="mb-6"
        >
          <svg width="80" height="80" viewBox="0 0 80 80" className="mx-auto">
            <motion.polygon
              points="40,5 75,65 5,65"
              fill="none"
              stroke="url(#logoGrad)"
              strokeWidth="2"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1.5, ease: "easeInOut" }}
            />
            <defs>
              <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00f0ff" />
                <stop offset="100%" stopColor="#ff00aa" />
              </linearGradient>
            </defs>
          </svg>
        </motion.div>
        <motion.h2
          className="font-display text-2xl font-bold tracking-[0.3em] text-white"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.6 }}
        >
          NOESIS
        </motion.h2>
        <motion.div
          className="mt-4 h-[2px] w-48 mx-auto bg-noesis-border rounded-full overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <motion.div
            className="h-full bg-gradient-to-r from-noesis-cyan to-noesis-magenta"
            initial={{ width: "0%" }}
            animate={{ width: "100%" }}
            transition={{ delay: 1, duration: 1, ease: "easeInOut" }}
          />
        </motion.div>
      </div>
    </motion.div>
  )
}

export default function App() {
  const [loading, setLoading] = useState(true)

  return (
    <>
      <AnimatePresence mode="wait">
        {loading && <LoadingScreen onComplete={() => setLoading(false)} />}
      </AnimatePresence>

      {!loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          <ParticleField />
          <Navbar />
          <Hero />
          <Games />
          <About />
          <Features />
          <CTA />
          <Footer />
        </motion.div>
      )}
    </>
  )
}
