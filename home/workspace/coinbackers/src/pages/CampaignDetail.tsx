import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  ArrowLeft, 
  Coins, 
  TrendingUp, 
  Users, 
  Clock, 
  AlertCircle,
  CheckCircle2
} from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface Campaign { 
  id: string; 
  title: string; 
  description: string; 
  goal: number; 
  pledged: number; 
  backers?: number;
  daysLeft?: number;
  imageUrl?: string;
  creatorWallet?: string;
}

const SUPPORTED_CURRENCIES = [
  { symbol: "eth", name: "Ethereum", color: "bg-blue-500" },
  { symbol: "btc", name: "Bitcoin", color: "bg-orange-500" },
  { symbol: "sol", name: "Solana", color: "bg-purple-500" },
  { symbol: "usdc", name: "USDC", color: "bg-blue-400" },
  { symbol: "xrp", name: "XRP", color: "bg-slate-700" },
  { symbol: "ada", name: "Cardano", color: "bg-blue-800" },
  { symbol: "doge", name: "Dogecoin", color: "bg-yellow-500" },
  { symbol: "matic", name: "Polygon", color: "bg-purple-700" },
  { symbol: "link", name: "Chainlink", color: "bg-blue-600" },
  { symbol: "ltc", name: "Litecoin", color: "bg-slate-400" },
];

export default function CampaignDetail() {
  const { id } = useParams();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [pledgeAmount, setPledgeAmount] = useState("");
  const [currency, setCurrency] = useState("eth");
  const [loading, setLoading] = useState(true);
  const [pledging, setPledging] = useState(false);
  const [usdEquivalent, setUsdEquivalent] = useState<number | null>(null);
  const [success, setSuccess] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`/api/campaigns/${id}`)
      .then((r) => r.json())
      .then((data) => {
        setCampaign(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    if (pledgeAmount && !isNaN(Number(pledgeAmount))) {
      const timer = setTimeout(() => {
        fetch(`/api/price?symbol=${currency}`)
          .then(r => r.json())
          .then(data => {
            if (data.usdPrice) {
              setUsdEquivalent(Number(pledgeAmount) * data.usdPrice);
            }
          });
      }, 500);
      return () => clearTimeout(timer);
    } else {
      setUsdEquivalent(null);
    }
  }, [pledgeAmount, currency]);

  const handlePledge = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pledgeAmount || !usdEquivalent) return;
    setError("");
    if (!confirming) {
      setConfirming(true);
      return;
    }
    setPledging(true);
    try {
      const ethereum = (window as Window & { ethereum?: { request: (args: { method: string; params?: unknown[] }) => Promise<unknown> } }).ethereum;
      if (!ethereum) throw new Error("A browser wallet is required to sign your pledge.");
      const address = ((await ethereum.request({ method: "eth_requestAccounts" })) as string[])[0];
      if (!address) throw new Error("No wallet account selected.");
      const challengeRes = await fetch(`/api/campaigns/${id}/pledge/challenge`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ address, amount: usdEquivalent }),
      });
      if (!challengeRes.ok) {
        const err = await challengeRes.json();
        throw new Error(err.error || "Could not start pledge signing.");
      }
      const { message } = await challengeRes.json();
      const signature = (await ethereum.request({ method: "personal_sign", params: [message, address] })) as string;
      const res = await fetch(`/api/campaigns/${id}/pledge`, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ amount: usdEquivalent, address, message, signature }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Your pledge could not be recorded.");
      }
      const updated = await res.json();
      setCampaign(updated);
      setSuccess(true);
      setPledgeAmount("");
      setConfirming(false);
      setTimeout(() => setSuccess(false), 5000);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Your pledge could not be recorded. Check your connection and try again.");
    } finally {
      setPledging(false);
    }
  };

  if (loading) return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>
  );
  
  if (!campaign) return (
    <div className="max-w-7xl mx-auto px-6 py-20 text-center">
      <h2 className="text-2xl font-bold mb-4">Campaign not found</h2>
      <Button asChild>
        <Link to="/explore">Back to Explore</Link>
      </Button>
    </div>
  );

  const progress = Math.min((campaign.pledged / campaign.goal) * 100, 100);
  const shareUrl = typeof window !== "undefined" ? window.location.href : `https://coinbackers.com/campaign/${campaign.id}`;

  return (
    <div className="bg-slate-50 min-h-screen py-12 px-6">
      <div className="max-w-5xl mx-auto">
        <Link to="/explore" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-medium mb-8 group">
          <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Explore
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            <div className="rounded-3xl overflow-hidden bg-slate-200 aspect-video shadow-sm">
              <img 
                src={campaign.imageUrl || `/api/artwork/${encodeURIComponent(campaign.title)}`} 
                onError={(e) => {
                  const img = e.currentTarget;
                  const fallback = `/api/artwork/${encodeURIComponent(campaign.title)}`;
                  if (!img.src.endsWith(fallback)) img.src = fallback;
                }}
                alt={campaign.title}
                className="w-full h-full object-cover"
              />
            </div>

            <div className="bg-white rounded-3xl p-8 border border-slate-100 shadow-sm">
              <h1 className="text-3xl font-bold text-slate-900 mb-4">{campaign.title}</h1>
              <div className="flex flex-wrap gap-4 mb-8">
                <Badge className="bg-indigo-50 text-indigo-600 border-indigo-100 px-3 py-1">Technology</Badge>
                {campaign.creatorWallet ? (
                  <span className="inline-flex items-center gap-2 bg-emerald-50 text-emerald-700 border border-emerald-100 rounded-full px-3 py-1 text-xs font-medium">
                    <span className="w-5 h-5 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[9px] font-bold">
                      {campaign.creatorWallet.slice(2, 4).toUpperCase()}
                    </span>
                    Verified creator {campaign.creatorWallet.slice(0, 6)}…{campaign.creatorWallet.slice(-4)}
                  </span>
                ) : (
                  <Badge className="bg-emerald-50 text-emerald-600 border-emerald-100 px-3 py-1">Verified Creator</Badge>
                )}
              </div>
              
              <div className="flex items-center gap-3 border-t border-slate-100 pt-6 mb-8">
                <span className="text-sm font-semibold text-slate-700">Share</span>
                <a
                  href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(`Back "${campaign.title}" on CoinBackers`) }&url=${encodeURIComponent(shareUrl)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-full bg-slate-900 text-white px-4 py-2 text-xs font-semibold hover:bg-slate-700 transition-colors"
                  aria-label="Share on X"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-3.5 h-3.5" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                  Share on X
                </a>
                <a
                  href={`https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(`Back "${campaign.title}" on CoinBackers`)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-full text-white px-4 py-2 text-xs font-semibold transition-opacity hover:opacity-90" style={{ backgroundColor: "#0ea5e9" }}
                  aria-label="Share on Telegram"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor" className="w-3.5 h-3.5" aria-hidden="true"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
                  Share on Telegram
                </a>
              </div>

              <div className="prose prose-slate max-w-none">
                <h3 className="text-xl font-bold mb-4">About this project</h3>
                <p className="text-slate-600 leading-relaxed whitespace-pre-wrap">
                  {campaign.description}
                </p>
              </div>
            </div>
          </div>

          {/* Sidebar / Pledge Card */}
          <div className="space-y-6">
            <Card className="rounded-3xl border-slate-100 shadow-lg sticky top-8 overflow-hidden">
              <CardHeader className="bg-slate-900 text-white pb-8">
                <CardTitle className="text-3xl font-bold">${campaign.pledged.toLocaleString()}</CardTitle>
                <CardDescription className="text-slate-400">
                  pledged of ${campaign.goal.toLocaleString()} goal
                </CardDescription>
                <div className="mt-6">
                  <Progress value={progress} className="h-3 bg-slate-800" />
                  <div className="flex justify-between mt-2 text-xs font-medium">
                    <span className="text-indigo-400">{Math.round(progress)}% funded</span>
                    <span className="text-slate-500">{campaign.backers || 0} backers</span>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-8">
                <div className="grid grid-cols-2 gap-4 mb-8">
                  <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">Backers</div>
                    <div className="text-xl font-bold text-slate-900">{campaign.backers || 0}</div>
                  </div>
                  <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100">
                    <div className="text-slate-400 text-xs uppercase tracking-wider mb-1">Days Left</div>
                    <div className="text-xl font-bold text-slate-900">{campaign.daysLeft || 30}</div>
                  </div>
                </div>

                <form onSubmit={handlePledge} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-slate-700">Pledge with Crypto</label>
                    <div className="flex gap-2">
                      <Select value={currency} onValueChange={setCurrency}>
                        <SelectTrigger className="w-[120px] rounded-xl border-slate-200 bg-white">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {SUPPORTED_CURRENCIES.map(c => (
                            <SelectItem key={c.symbol} value={c.symbol}>
                              <div className="flex items-center gap-2">
                                <div className={`w-2 h-2 rounded-full ${c.color}`} />
                                <span>{c.symbol.toUpperCase()}</span>
                              </div>
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <Input 
                        type="number" 
                        step="any"
                        placeholder="0.00" 
                        value={pledgeAmount}
                        onChange={(e) => setPledgeAmount(e.target.value)}
                        className="flex-grow rounded-xl border-slate-200"
                        required
                      />
                    </div>
                  </div>

                  {usdEquivalent !== null && (
                    <div className="bg-indigo-50 p-4 rounded-2xl border border-indigo-100 flex items-center justify-between">
                      <div className="flex items-center gap-2 text-indigo-700">
                        <TrendingUp className="w-4 h-4" />
                        <span className="text-sm font-medium">Est. Value</span>
                      </div>
                      <span className="font-bold text-indigo-900">${usdEquivalent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
                    </div>
                  )}

                  {success && (
                    <div className="bg-emerald-50 text-emerald-700 p-4 rounded-2xl border border-emerald-100 flex items-center gap-3">
                      <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
                      <span className="text-sm font-medium">Pledge successful! Thank you for your support.</span>
                    </div>
                  )}

                  {error && (
                    <div className="bg-red-50 text-red-700 p-4 rounded-2xl border border-red-100 flex items-center gap-3" role="alert">
                      <AlertCircle className="w-5 h-5 flex-shrink-0" />
                      <span className="text-sm font-medium">{error}</span>
                    </div>
                  )}

                  {confirming && usdEquivalent !== null && (
                    <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 space-y-3">
                      <p className="text-sm font-semibold text-amber-950">Confirm your pledge</p>
                      <p className="text-sm text-amber-800">
                        Pledge {pledgeAmount} {currency.toUpperCase()} (estimated ${usdEquivalent.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}) to this project? Your wallet will ask you to sign this pledge.
                      </p>
                      <div className="flex gap-2">
                        <Button type="submit" className="flex-1 rounded-xl bg-amber-600 hover:bg-amber-700 text-white" disabled={pledging}>
                          {pledging ? "Recording..." : "Confirm pledge"}
                        </Button>
                        <Button type="button" variant="outline" className="rounded-xl" onClick={() => setConfirming(false)} disabled={pledging}>
                          Cancel
                        </Button>
                      </div>
                    </div>
                  )}

                  {!confirming && <Button 
                    type="submit" 
                    disabled={pledging || !pledgeAmount || !usdEquivalent}
                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-6 font-bold shadow-indigo-200 shadow-lg transition-all hover:scale-[1.02] active:scale-[0.98]"
                  >
                    {pledging ? "Processing..." : "Back this project"}
                  </Button>}
                </form>
              </CardContent>
              <CardFooter className="bg-slate-50 border-t border-slate-100 p-6">
                <div className="flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-slate-400 flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-slate-500 leading-relaxed">
                    Pledges are final. By clicking "Back this project" you agree to our terms and conditions. Cryptocurrency values are subject to market volatility.
                  </p>
                </div>
              </CardFooter>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
