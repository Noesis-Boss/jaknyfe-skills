import React from "react";
import { cn } from "@/lib/utils";
import { Link } from "react-router-dom";
import { ArrowRight, Rocket, Shield, Globe } from "lucide-react";

export default function Hero({ coins = [] }: { coins?: string[][] }) {
  const pile = [
    ["1%", "5%", 13, -18], ["16%", "14%", 11, 12], ["33%", "4%", 14, -8], ["52%", "12%", 12, 22],
    ["72%", "3%", 15, -14], ["88%", "16%", 11, 16], ["4%", "31%", 15, -20], ["19%", "35%", 12, 8],
    ["37%", "28%", 14, 10], ["57%", "33%", 11, -24], ["76%", "27%", 15, 14], ["92%", "36%", 12, -6],
    ["9%", "55%", 12, 20], ["27%", "49%", 15, -18], ["47%", "55%", 11, 12], ["67%", "48%", 14, -10],
    ["84%", "57%", 12, 16], ["2%", "76%", 14, -12], ["21%", "70%", 11, 24], ["40%", "78%", 15, -20],
    ["59%", "69%", 12, 8], ["76%", "78%", 14, -16], ["91%", "70%", 11, 18], ["48%", "87%", 13, -8],
  ];
  return (
    <section className="relative isolate overflow-hidden bg-gradient-to-br from-indigo-900 via-purple-900 to-slate-900 py-24 sm:py-32">
      {/* Decorative background elements */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <svg
          className="absolute left-[calc(50%-11rem)] top-[-10rem] h-[21.1875rem] max-w-none -translate-x-1/2 blur-3xl sm:left-[calc(50%-30rem)] sm:h-[42.375rem]"
          viewBox="0 0 1155 678"
        >
          <path
            fill="url(#45de2b6b-92d5-4d68-a6a0-9b9b2abad533)"
            fillOpacity=".3"
            d="M317.219 518.975L203.852 678 0 438.341l317.219 80.634 204.172-286.402c1.307 132.337 45.083 346.658 209.733 145.248C936.936 126.058 882.053-94.234 1031.02 41.331c119.18 108.451 130.68 295.337 121.53 375.223L855 299l21.173 362.054-558.954-142.079z"
          />
          <defs>
            <linearGradient
              id="45de2b6b-92d5-4d68-a6a0-9b9b2abad533"
              x1="1155.49"
              x2="-78.208"
              y1=".177"
              y2="474.645"
              gradientUnits="userSpaceOnUse"
            >
              <stop stopColor="#9089FC" />
              <stop offset={1} stopColor="#FF80B5" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      <div className="pointer-events-none absolute inset-0 z-0 overflow-hidden" aria-hidden="true">
          {coins.map(([, , size], index) => (
          <img key={index} src={`/images/coins/coin-${String(index).padStart(2, "0")}.png?v=3`} alt="" style={{ clipPath: "circle(44% at 50% 50%)", left: pile[index][0], top: pile[index][1], width: `${pile[index][2]}rem`, transform: `rotate(${pile[index][3]}deg)`, opacity: 0.1 }} className="absolute" />
        ))}
      </div>

      <div className="relative z-10 mx-auto max-w-7xl px-6 lg:px-8 text-center">
        <div className="mx-auto max-w-2xl">
          <div className="mb-8 flex justify-center">
            <div className="relative rounded-full px-3 py-1 text-sm leading-6 text-indigo-200 ring-1 ring-white/10 hover:ring-white/20">
              New: Multiple cryptocurrencies now supported via Moonpay.{' '}
              <Link to="/explore" className="font-semibold text-white">
                <span className="absolute inset-0" aria-hidden="true" />
                Read more <span aria-hidden="true">&rarr;</span>
              </Link>
            </div>
          </div>
          <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-white to-indigo-200">
            Fuel the Future of Innovation
          </h1>
          <p className="mt-6 text-lg leading-8 text-indigo-100">
            CoinBackers is the premier crypto-first crowdfunding platform. Raise funds for your next big project in USD while giving your backers the freedom to pledge in ETH, BTC, or SOL.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Link
              to="/create"
              className="rounded-md bg-indigo-500 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-400 flex items-center gap-2 transition-all hover:scale-105"
            >
              Start Your Campaign <Rocket className="w-4 h-4" />
            </Link>
            <Link to="/explore" className="text-sm font-semibold leading-6 text-white flex items-center gap-2 hover:text-indigo-200 transition-colors">
              Explore Projects <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>

        <div className="mt-20 grid grid-cols-1 gap-y-12 sm:grid-cols-3 sm:gap-x-12">
          <div className="flex flex-col items-center">
            <div className="rounded-lg bg-white/5 p-3 ring-1 ring-white/10 mb-4">
              <Shield className="h-6 w-6 text-indigo-400" />
            </div>
            <h3 className="text-white font-semibold">Secure Pledges</h3>
            <p className="text-indigo-200 text-sm mt-2">Enterprise-grade security for all transactions.</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="rounded-lg bg-white/5 p-3 ring-1 ring-white/10 mb-4">
              <Globe className="h-6 w-6 text-indigo-400" />
            </div>
            <h3 className="text-white font-semibold">Global Reach</h3>
            <p className="text-indigo-200 text-sm mt-2">Connect with backers from around the world.</p>
          </div>
          <div className="flex flex-col items-center">
            <div className="rounded-lg bg-white/5 p-3 ring-1 ring-white/10 mb-4">
              <Rocket className="h-6 w-6 text-indigo-400" />
            </div>
            <h3 className="text-white font-semibold">Fast Funding</h3>
            <p className="text-indigo-200 text-sm mt-2">Instant settlements and transparent goals.</p>
          </div>
        </div>
      </div>
    </section>
  );
}
