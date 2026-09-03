import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Coins, DollarSign, Users, Clock } from "lucide-react";

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

export default function Explore() {
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");

  useEffect(() => {
    fetch("/api/campaigns")
      .then((r) => r.json())
      .then((data) => {
        setCampaigns(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const categories = ["All", "Technology", "Sustainability", "Community"];
  const getCategory = (campaign: Campaign) => {
    const text = `${campaign.title} ${campaign.description}`.toLowerCase();
    if (text.includes("ai") || text.includes("assistant") || text.includes("decentralized")) return "Technology";
    if (text.includes("solar") || text.includes("water") || text.includes("eco") || text.includes("sustainable")) return "Sustainability";
    return "Community";
  };
  const filteredCampaigns = useMemo(() => {
    const term = search.trim().toLowerCase();
    return campaigns.filter((campaign) => {
      const matchesSearch = !term || `${campaign.title} ${campaign.description}`.toLowerCase().includes(term);
      return matchesSearch && (category === "All" || getCategory(campaign) === category);
    });
  }, [campaigns, search, category]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  return (
    <div className="bg-slate-50 min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4 lg:px-8" aria-label="Main navigation">
          <Link to="/" className="flex items-center gap-2 text-lg font-bold text-slate-900">
            <Coins className="h-6 w-6 text-indigo-600" />
            CoinBackers
          </Link>
          <Link to="/" className="font-medium text-indigo-600 transition-colors hover:text-indigo-800">
            Back to Main
          </Link>
        </nav>
      </header>
      <main className="py-16 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-end mb-12">
          <div>
            <h1 className="text-4xl font-bold text-slate-900 mb-4">Explore Projects</h1>
            <p className="text-slate-600">Discover and support the next big thing in decentralized innovation.</p>
          </div>
          <div className="hidden md:block">
            <Badge variant="outline" className="text-indigo-600 border-indigo-200 bg-indigo-50 px-4 py-1">
              {filteredCampaigns.length} Projects Live
            </Badge>
          </div>
        </div>

        <div className="mb-10 grid gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm md:grid-cols-[1fr_auto]">
          <label className="sr-only" htmlFor="campaign-search">Search projects</label>
          <input
            id="campaign-search"
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="Search projects"
            className="h-11 rounded-lg border border-slate-200 px-4 text-sm text-slate-900 outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100"
          />
          <div className="flex flex-wrap gap-2" aria-label="Project categories">
            {categories.map((item) => (
              <button
                key={item}
                type="button"
                onClick={() => setCategory(item)}
                aria-pressed={category === item}
                className={`rounded-full px-4 py-2 text-sm font-medium transition ${category === item ? "bg-indigo-600 text-white" : "bg-slate-100 text-slate-600 hover:bg-indigo-50 hover:text-indigo-700"}`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>

        {filteredCampaigns.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-slate-300">
            <p className="text-slate-500 mb-6">No projects match those filters.</p>
            <Button asChild className="bg-indigo-600">
              <Link to="/create">Create Campaign</Link>
            </Button>
          </div>
        ) : (
          <div className="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
            {filteredCampaigns.map((c) => {
              const progress = Math.min((c.pledged / c.goal) * 100, 100);
              return (
                <Card key={c.id} className="group overflow-hidden flex flex-col border-slate-200 hover:border-indigo-300 transition-all hover:shadow-lg">
                  <div className="aspect-video bg-slate-200 relative overflow-hidden">
                    <img 
                      src={c.imageUrl || `/api/artwork/${encodeURIComponent(c.title)}`} 
                      onError={(e) => {
                        const img = e.currentTarget;
                        const fallback = `/api/artwork/${encodeURIComponent(c.title)}`;
                        if (!img.src.endsWith(fallback)) img.src = fallback;
                      }}
                      alt={c.title}
                      className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute top-4 right-4">
                      <Badge className="bg-white/90 text-indigo-600 backdrop-blur-sm border-none">
                        {getCategory(c)}
                      </Badge>
                    </div>
                  </div>
                  <CardHeader className="pb-4">
                    <CardTitle className="text-xl font-bold group-hover:text-indigo-600 transition-colors">
                      {c.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex-grow">
                    <p className="text-slate-600 text-sm line-clamp-3 mb-6 leading-relaxed">
                      {c.description}
                    </p>
                    
                    <div className="space-y-4">
                      <div className="flex justify-between items-end text-sm">
                        <span className="font-bold text-slate-900">${c.pledged.toLocaleString()}</span>
                        <span className="text-slate-500">pledged of ${c.goal.toLocaleString()}</span>
                      </div>
                      <Progress value={progress} className="h-2 bg-slate-100" />
                    </div>
                  </CardContent>
                  <CardFooter className="pt-0 pb-6 grid grid-cols-2 gap-4 border-t border-slate-50 mt-4">
                    <div className="flex items-center gap-2 text-slate-500 text-xs py-2">
                      <Users className="w-3.5 h-3.5" />
                      <span>{c.backers || 0} Backers</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-500 text-xs py-2">
                      <Clock className="w-3.5 h-3.5" />
                      <span>{c.daysLeft || 30} Days left</span>
                    </div>
                    <Button asChild className="col-span-2 bg-slate-900 hover:bg-indigo-600 transition-colors">
                      <Link to={`/campaign/${c.id}`}>View Details</Link>
                    </Button>
                  </CardFooter>
                </Card>
              );
            })}
          </div>
        )}
      </div>
      </main>
    </div>
  );
}
