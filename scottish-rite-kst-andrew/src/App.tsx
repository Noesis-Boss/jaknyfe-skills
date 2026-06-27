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
  return (
    <div className="app hero-bg">
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
