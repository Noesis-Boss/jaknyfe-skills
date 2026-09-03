import React from "react";
import Hero from "../components/ui/hero";
import { Button } from "@/components/ui/button";
import { Link } from "react-router-dom";
import { Coins, TrendingUp, Users, Zap } from "lucide-react";

export default function Home() {
  const coins = [
    ["left-[3%] top-[8%]", "w-24", "rotate-[-18deg]"], ["left-[16%] top-[6%]", "w-16", "rotate-[14deg]"],
    ["left-[30%] top-[10%]", "w-20", "rotate-[-8deg]"], ["right-[29%] top-[7%]", "w-28", "rotate-[18deg]"],
    ["right-[14%] top-[12%]", "w-16", "rotate-[-22deg]"], ["right-[2%] top-[6%]", "w-24", "rotate-[8deg]"],
    ["left-[6%] top-[28%]", "w-16", "rotate-[24deg]"], ["left-[22%] top-[30%]", "w-28", "rotate-[-12deg]"],
    ["left-[38%] top-[27%]", "w-20", "rotate-[20deg]"], ["right-[37%] top-[31%]", "w-16", "rotate-[-20deg]"],
    ["right-[20%] top-[26%]", "w-24", "rotate-[10deg]"], ["right-[5%] top-[32%]", "w-20", "rotate-[-16deg]"],
    ["left-[2%] top-[52%]", "w-28", "rotate-[12deg]"], ["left-[15%] top-[51%]", "w-20", "rotate-[-25deg]"],
    ["left-[32%] top-[49%]", "w-16", "rotate-[16deg]"], ["right-[31%] top-[52%]", "w-24", "rotate-[-8deg]"],
    ["right-[15%] top-[48%]", "w-20", "rotate-[25deg]"], ["right-[1%] top-[55%]", "w-16", "rotate-[-12deg]"],
    ["left-[8%] top-[75%]", "w-20", "rotate-[-14deg]"], ["left-[25%] top-[73%]", "w-24", "rotate-[9deg]"],
    ["left-[43%] top-[78%]", "w-16", "rotate-[-22deg]"], ["right-[35%] top-[74%]", "w-28", "rotate-[14deg]"],
    ["right-[18%] top-[77%]", "w-16", "rotate-[-10deg]"], ["right-[4%] top-[72%]", "w-24", "rotate-[20deg]"],
  ];

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-50">
      <div className="relative z-10">
      <header className="relative z-30 border-b border-slate-100 bg-white text-slate-900 shadow-sm">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8" aria-label="Main navigation">
          <Link to="/" className="flex items-center gap-2 text-lg font-black tracking-tight text-slate-900">
            <Coins className="h-6 w-6 text-indigo-600" aria-hidden="true" />
            CoinBackers
          </Link>
          <div className="hidden items-center gap-7 text-sm font-medium text-slate-600 sm:flex">
            <Link to="/" className="transition-colors hover:text-indigo-600">Home</Link>
            <Link to="/explore" className="transition-colors hover:text-indigo-600">Explore</Link>
            <Link to="/dashboard" className="transition-colors hover:text-indigo-600">Dashboard</Link>
            <Link to="/create" className="rounded-full bg-white px-4 py-2 font-semibold text-indigo-900 transition-colors hover:bg-indigo-100">Start Campaign</Link>
          </div>
          <Link to="/create" className="rounded-full bg-white px-3 py-2 text-xs font-bold text-indigo-900 sm:hidden">Start</Link>
        </nav>
      </header>
      <Hero coins={coins} />
      
      <div className="max-w-7xl mx-auto px-6 py-24 sm:py-32">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <TrendingUp className="w-10 h-10 text-indigo-600 mb-6" />
            <h2 className="text-xl font-bold text-slate-900 mb-4">Market Leading Growth</h2>
            <p className="text-slate-600 leading-relaxed">Join a community of thousands of backers supporting the next generation of decentralized technology.</p>
          </div>
          
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <Users className="w-10 h-10 text-purple-600 mb-6" />
            <h2 className="text-xl font-bold text-slate-900 mb-4">Community Driven</h2>
            <p className="text-slate-600 leading-relaxed">Direct connection between creators and supporters. No middlemen, no unnecessary fees.</p>
          </div>
          
          <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
            <Zap className="w-10 h-10 text-pink-600 mb-6" />
            <h2 className="text-xl font-bold text-slate-900 mb-4">Instant Pledges</h2>
            <p className="text-slate-600 leading-relaxed">Real-time USD conversion for all cryptocurrency pledges. Know exactly how much you're contributing.</p>
          </div>
        </div>

        <div className="mt-32 text-center">
          <h2 className="text-3xl font-bold text-slate-900 mb-6">Ready to launch your dream?</h2>
          <p className="text-lg text-slate-600 mb-10 max-w-2xl mx-auto">Join hundreds of creators who have successfully funded their projects with CoinBackers.</p>
          <div className="flex justify-center gap-6">
            <Button asChild size="lg" className="bg-indigo-600 hover:bg-indigo-700">
              <Link to="/create">Start a Campaign</Link>
            </Button>
            <Button asChild size="lg" variant="outline" className="border-indigo-600 text-indigo-600 hover:bg-indigo-50">
              <Link to="/explore">Explore Projects</Link>
            </Button>
          </div>
        </div>
      </div>

      <footer className="bg-slate-900 text-slate-400 py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="text-white font-bold text-xl">CoinBackers</div>
          <div className="flex gap-8 text-sm">
            <Link to="/" className="hover:text-white transition-colors">Home</Link>
            <Link to="/explore" className="hover:text-white transition-colors">Explore</Link>
            <Link to="/create" className="hover:text-white transition-colors">Start Campaign</Link>
          </div>
          <div className="text-xs">
            © 2026 CoinBackers. Built with Zo Computer.
          </div>
        </div>
      </footer>
      </div>
    </div>
  );
}
