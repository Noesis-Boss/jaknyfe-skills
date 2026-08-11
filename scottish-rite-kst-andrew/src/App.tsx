import React from 'react'
import './App.css'
import { Nav } from './Nav'
import { Hero } from './Hero'
import { History } from './History'
import { Virtues } from './Virtues'
import { Activities } from './Activities'
import { Leadership } from './Leadership'
import { Events } from './Events'
import { Testimonials } from './Testimonials'
import { CTA } from './CTA'
import { Footer } from './Footer'

export default function App(): React.ReactElement {
  const tartan = `${import.meta.env.BASE_URL}tartan.jpg`

  return (
    <div
      className="app hero-bg"
      style={{
        backgroundImage: `linear-gradient(rgba(10, 22, 40, 0.65), rgba(10, 22, 40, 0.65)), url("${tartan}")`,
      }}
    >
      <Nav />
      <main>
        <Hero />
        <History />
        <Virtues />
        <Activities />
        <Leadership />
        <Events />
        <Testimonials />
        <CTA />
      </main>
      <Footer />
    </div>
  )
}
