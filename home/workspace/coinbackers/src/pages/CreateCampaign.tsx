import React, { useState, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ArrowLeft, Rocket, Info, Image as ImageIcon, X, Upload } from "lucide-react";

export default function CreateCampaign() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeImage = () => {
    setImage(null);
    setImagePreview(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    
    try {
      let imageUrl = "";
      if (image) {
        const formData = new FormData();
        formData.append("file", image);
        const uploadRes = await fetch("/api/upload", {
          method: "POST",
          body: formData,
        });
        const uploadData = await uploadRes.json();
        if (!uploadRes.ok) throw new Error(uploadData.error || "Image upload failed");
        imageUrl = uploadData.url;
      }

      const id = crypto.randomUUID();
      const creatorWallet = localStorage.getItem("coinbackers-wallet");
      const sessionToken = localStorage.getItem("coinbackers-wallet-session");
      if (!creatorWallet || !sessionToken) throw new Error("Connect and verify your wallet on the Dashboard before creating a campaign");
      const campaign = { 
        id, 
        title, 
        description, 
        goal: Number(goal), 
        pledged: 0,
        backers: 0,
        daysLeft: 30,
        imageUrl,
        creatorWallet
      };

      const campaignRes = await fetch("/api/campaigns", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: `Bearer ${sessionToken}` },
        body: JSON.stringify(campaign),
      });
      if (!campaignRes.ok) {
        const data = await campaignRes.json();
        throw new Error(data.error || "Campaign could not be created");
      }
      navigate(`/campaign/${id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Campaign could not be created");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-50 min-h-screen py-12 px-6">
      <div className="max-w-2xl mx-auto">
        <Link to="/explore" className="inline-flex items-center text-indigo-600 hover:text-indigo-700 font-medium mb-8 group">
          <ArrowLeft className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
          Back to Explore
        </Link>

        <Card className="rounded-3xl border-slate-100 shadow-xl overflow-hidden">
          <CardHeader className="bg-slate-900 text-white p-8">
            <div className="flex items-center gap-3 mb-2">
              <Rocket className="w-6 h-6 text-indigo-400" />
              <CardTitle className="text-2xl font-bold">Start a Campaign</CardTitle>
            </div>
            <CardDescription className="text-slate-400">
              Fill out the details below to launch your crypto-crowdfunded project.
            </CardDescription>
          </CardHeader>
          <CardContent className="p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="title" className="text-sm font-bold text-slate-700">Project Title</Label>
                <Input
                  id="title"
                  placeholder="e.g. The Next-Gen Web3 Social Platform"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="rounded-xl border-slate-200 py-6"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label className="text-sm font-bold text-slate-700">Project Graphic</Label>
                <div 
                  onClick={() => !imagePreview && fileInputRef.current?.click()}
                  className={`relative border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center transition-all ${
                    imagePreview ? "border-indigo-100 bg-slate-50" : "border-slate-200 hover:border-indigo-400 hover:bg-indigo-50/30 cursor-pointer"
                  }`}
                >
                  {imagePreview ? (
                    <div className="relative w-full aspect-video rounded-xl overflow-hidden shadow-sm">
                      <img src={imagePreview} alt="Preview" className="w-full h-full object-cover" />
                      <button 
                        type="button"
                        onClick={(e) => { e.stopPropagation(); removeImage(); }}
                        className="absolute top-2 right-2 bg-white/90 hover:bg-white p-1.5 rounded-full shadow-md transition-colors"
                      >
                        <X className="w-4 h-4 text-slate-600" />
                      </button>
                    </div>
                  ) : (
                    <>
                      <div className="bg-indigo-100 p-3 rounded-2xl mb-3">
                        <Upload className="w-6 h-6 text-indigo-600" />
                      </div>
                      <p className="text-sm font-semibold text-slate-600">Click to upload main graphic</p>
                      <p className="text-xs text-slate-400 mt-1">PNG, JPG or WEBP (Max 5MB)</p>
                    </>
                  )}
                  <input 
                    type="file" 
                    ref={fileInputRef}
                    onChange={handleImageChange}
                    accept="image/*"
                    className="hidden"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="goal" className="text-sm font-bold text-slate-700">Funding Goal (USD)</Label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 font-bold">$</span>
                  <Input
                    id="goal"
                    type="number"
                    placeholder="10,000"
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    className="rounded-xl border-slate-200 py-6 pl-8"
                    required
                  />
                </div>
                <p className="text-[10px] text-slate-400 mt-1">Set your goal in USD. Backers will pledge in crypto based on real-time conversion rates.</p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="description" className="text-sm font-bold text-slate-700">Project Description</Label>
                <Textarea
                  id="description"
                  placeholder="Describe your vision, roadmap, and why people should back you..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="rounded-xl border-slate-200 min-h-[150px] py-4"
                  required
                />
              </div>

              {error && (
                <div role="alert" className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm font-medium text-red-700">
                  {error}
                </div>
              )}

              <Button 
                type="submit" 
                disabled={loading}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white rounded-2xl py-8 text-lg font-bold shadow-indigo-200 shadow-lg transition-all hover:scale-[1.01] active:scale-[0.99]"
              >
                {loading ? "Launching Project..." : "Launch Campaign"}
              </Button>
            </form>
          </CardContent>
          <CardFooter className="bg-slate-50 border-t border-slate-100 p-8">
            <div className="flex items-start gap-4">
              <div className="bg-indigo-100 p-2 rounded-lg">
                <Info className="w-4 h-4 text-indigo-600" />
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">
                By launching a campaign, you agree to our creator terms. Your project will be immediately visible to the public. Ensure your description is clear and your goal is realistic.
              </p>
            </div>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}
