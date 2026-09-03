import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { LayoutDashboard, TrendingUp, DollarSign, Wallet, ArrowRight, Clock, Copy, Check } from "lucide-react";

interface Campaign { 
  id: string; 
  title: string; 
  description: string; 
  goal: number; 
  pledged: number; 
  backers?: number;
  daysLeft?: number;
  imageUrl?: string;
}

export default function CreatorDashboard() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [wallet, setWallet] = useState<string | null>(() => localStorage.getItem("coinbackers-wallet"));
  const [verified, setVerified] = useState(() => localStorage.getItem("coinbackers-wallet-verified") === "true");
  const [walletError, setWalletError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const connectWallet = async () => {
    const ethereum = (window as Window & { ethereum?: { request: (args: { method: string }) => Promise<string[]> } }).ethereum;
    setWalletError(null);
    if (!ethereum) { setWalletError("A browser wallet is required for verification."); return; }
    try {
      const address = (await ethereum.request({ method: "eth_requestAccounts" }))[0];
      const challengeRes = await fetch("/api/wallet/challenge", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ address }) });
      const { message } = await challengeRes.json();
      const signature = await ethereum.request({ method: "personal_sign", params: [message, address] } as { method: string; params: string[] }) as unknown as string;
      const verifyRes = await fetch("/api/wallet/verify", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify({ address, message, signature }) });
      if (!verifyRes.ok) throw new Error((await verifyRes.json()).error || "Verification failed");
      setWallet(address); setVerified(true);
      localStorage.setItem("coinbackers-wallet", address);
      localStorage.setItem("coinbackers-wallet-verified", "true");
    } catch (error) { setWalletError(error instanceof Error ? error.message : "Wallet verification failed"); }
  };

  const copyWallet = async () => {
    if (!wallet) return;
    await navigator.clipboard.writeText(wallet);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1200);
  };

  useEffect(() => {
    fetch("/api/campaigns")
      .then((r) => r.json())
      .then((data) => {
        setCampaigns(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const totalPledged = campaigns.reduce((acc, c) => acc + c.pledged, 0);
  const platformFee = totalPledged * 0.10;
  const netPayout = totalPledged - platformFee;

  if (loading) return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  );

  return (
    <div className="bg-slate-50 min-h-screen py-12 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-2 rounded-xl">
            <LayoutDashboard className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-slate-900">Creator Dashboard</h1>
          </div>
          {wallet && verified ? (
            <button type="button" onClick={copyWallet} className="inline-flex items-center gap-2 self-start rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-2 text-sm font-semibold text-emerald-700 sm:self-auto" aria-label="Copy connected wallet address">
              {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              {copied ? "Copied" : wallet}
            </button>
          ) : (
            <button type="button" onClick={connectWallet} className="inline-flex items-center gap-2 self-start rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 sm:self-auto">
              <Wallet className="h-4 w-4" /> Connect Wallet
            </button>
          )}
        </div>
        {walletError && <p role="alert" className="mb-6 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{walletError}</p>}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="rounded-3xl border-slate-100 shadow-sm overflow-hidden">
            <CardHeader className="bg-slate-900 text-white pb-6">
              <CardDescription className="text-slate-400 font-medium uppercase tracking-wider text-xs">Gross Revenue</CardDescription>
              <CardTitle className="text-4xl font-bold">${totalPledged.toLocaleString()}</CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full w-fit text-sm font-medium">
                <TrendingUp className="w-4 h-4" />
                <span>Total from all campaigns</span>
              </div>
            </CardContent>
          </Card>

          <Card className="rounded-3xl border-slate-100 shadow-sm overflow-hidden border-l-4 border-l-amber-500">
            <CardHeader className="pb-4">
              <CardDescription className="text-slate-500 font-medium uppercase tracking-wider text-xs">Platform Fee (10%)</CardDescription>
              <CardTitle className="text-3xl font-bold text-slate-900">-${platformFee.toLocaleString()}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-slate-500">CoinBackers maintenance and processing fee</p>
            </CardContent>
          </Card>

          <Card className="rounded-3xl border-slate-100 shadow-sm overflow-hidden border-l-4 border-l-indigo-600">
            <CardHeader className="bg-indigo-600 text-white pb-6">
              <CardDescription className="text-indigo-100 font-medium uppercase tracking-wider text-xs">Available Payout</CardDescription>
              <CardTitle className="text-4xl font-bold">${netPayout.toLocaleString()}</CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <Button className="w-full bg-slate-900 hover:bg-slate-800 text-white rounded-xl py-6 font-bold flex gap-2">
                <Wallet className="w-5 h-5" />
                Request Payout (USD)
              </Button>
            </CardContent>
          </Card>
        </div>

        <h2 className="text-2xl font-bold text-slate-900 mb-6">Your Campaigns</h2>
        
        {campaigns.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-slate-200">
            <p className="text-slate-500 mb-6">No campaigns found.</p>
            <Button asChild>
              <Link to="/create">Launch your first campaign</Link>
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {campaigns.map((c) => (
              <Card key={c.id} className="rounded-2xl border-slate-100 shadow-sm overflow-hidden hover:border-indigo-200 transition-colors">
                <div className="flex flex-col md:flex-row items-center p-4 gap-6">
                  <div className="w-full md:w-32 h-20 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0">
                    <img 
                      src={c.imageUrl || `https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=2832&auto=format&fit=crop&sig=${c.id}`} 
                      alt={c.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-grow min-w-0 text-center md:text-left">
                    <h3 className="text-lg font-bold text-slate-900 truncate">{c.title}</h3>
                    <div className="flex items-center justify-center md:justify-start gap-4 mt-1">
                      <div className="flex items-center gap-1 text-slate-500 text-xs">
                        <Clock className="w-3.5 h-3.5" />
                        <span>{c.daysLeft || 30} days left</span>
                      </div>
                      <Badge className="bg-indigo-50 text-indigo-600 border-none text-[10px]">Active</Badge>
                    </div>
                  </div>
                  <div className="w-full md:w-64 space-y-2">
                    <div className="flex justify-between text-xs font-bold">
                      <span className="text-slate-900">${c.pledged.toLocaleString()}</span>
                      <span className="text-slate-400">Goal: ${c.goal.toLocaleString()}</span>
                    </div>
                    <Progress value={(c.pledged / c.goal) * 100} className="h-2" />
                  </div>
                  <div className="flex items-center gap-2">
                    <Button variant="outline" size="sm" asChild className="rounded-lg border-slate-200">
                      <Link to={`/campaign/${c.id}`}>View</Link>
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
