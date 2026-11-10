import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  Building2, 
  Calculator, 
  ArrowRight, 
  ShieldCheck, 
  Truck, 
  Sparkles, 
  Star, 
  ChevronRight, 
  CheckCircle2, 
  Layers, 
  Award,
  Users,
  Compass,
  Headphones
} from 'lucide-react';

export default function LandingPage() {
  // Quick interactive mini-estimator state
  const [plotLength, setPlotLength] = useState(40);
  const [plotWidth, setPlotWidth] = useState(30);
  const [plotFloors, setPlotFloors] = useState(2);

  const previewArea = plotLength * plotWidth * plotFloors;
  const previewCement = Math.ceil(previewArea * 0.42);
  const previewSteel = Math.round(previewArea * 3.8);
  const previewBudget = Math.round(previewArea * 1850);

  return (
    <div className="space-y-16 pb-16">
      {/* 1. HERO SECTION */}
      <section className="relative bg-[#102A43] text-white overflow-hidden py-16 sm:py-24 border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-3xl space-y-6">
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
              <Sparkles className="w-4 h-4 text-amber-400" />
              <span>India's #1 AI-Powered Construction Marketplace</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight">
              Build Smarter. Order Better. <span className="text-amber-400">Save More.</span>
            </h1>

            <p className="text-base sm:text-lg text-slate-300 leading-relaxed max-w-2xl">
              Discover certified construction materials, compare wholesale supplier prices, and estimate exact building requirements with our civil engineering AI.
            </p>

            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-4 pt-2">
              <Link
                to="/materials"
                className="inline-flex items-center justify-center px-6 py-3.5 rounded-xl text-base font-bold text-slate-950 bg-amber-500 hover:bg-amber-400 shadow-xl transition-all active:scale-95"
              >
                <span>Explore Materials</span>
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
              <Link
                to="/estimator"
                className="inline-flex items-center justify-center px-6 py-3.5 rounded-xl text-base font-bold text-white bg-slate-800/90 hover:bg-slate-700 border border-slate-600 shadow-md transition-all"
              >
                <Calculator className="w-5 h-5 mr-2 text-amber-400" />
                <span>Calculate Material Requirements</span>
              </Link>
            </div>

            {/* Quick Metrics */}
            <div className="grid grid-cols-3 gap-4 pt-8 border-t border-slate-700/80 max-w-lg">
              <div>
                <div className="text-2xl font-black text-amber-400">20+</div>
                <div className="text-xs text-slate-400">Verified Suppliers</div>
              </div>
              <div>
                <div className="text-2xl font-black text-amber-400">100%</div>
                <div className="text-xs text-slate-400">BIS Certified</div>
              </div>
              <div>
                <div className="text-2xl font-black text-amber-400">₹0</div>
                <div className="text-xs text-slate-400">Free Bulk Shipping</div>
              </div>
            </div>
          </div>
        </div>

        {/* Ambient Building Backdrop */}
        <div className="absolute right-0 bottom-0 opacity-10 pointer-events-none hidden lg:block">
          <Building2 className="w-[500px] h-[500px] text-white" />
        </div>
      </section>

      {/* 2. AI ESTIMATOR PREVIEW SECTION */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-br from-[#102A43] to-[#1E3A5F] rounded-3xl p-6 sm:p-10 text-white shadow-2xl relative overflow-hidden border border-slate-700">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
            <div className="lg:col-span-6 space-y-5">
              <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                <Calculator className="w-3.5 h-3.5 text-amber-400" />
                <span>Civil Engineering Rule Engine</span>
              </div>
              <h2 className="text-3xl sm:text-4xl font-black tracking-tight leading-tight">
                Accurate Material & Cost Estimates in <span className="text-amber-400">Seconds</span>.
              </h2>
              <p className="text-slate-300 text-sm leading-relaxed">
                Stop guessing material wastage. Enter your plot dimensions and number of floors to calculate preliminary requirement quantities for Cement, TMT Steel, Bricks, Sand, and Tiles.
              </p>

              <div className="grid grid-cols-3 gap-3">
                <div className="bg-white/10 backdrop-blur-md p-3.5 rounded-xl border border-white/10">
                  <div className="text-xs text-slate-300">Plot Length</div>
                  <input
                    type="number"
                    value={plotLength}
                    onChange={(e) => setPlotLength(Number(e.target.value))}
                    className="w-full bg-transparent text-lg font-bold text-amber-400 focus:outline-none"
                  />
                  <div className="text-[10px] text-slate-400">feet</div>
                </div>

                <div className="bg-white/10 backdrop-blur-md p-3.5 rounded-xl border border-white/10">
                  <div className="text-xs text-slate-300">Plot Width</div>
                  <input
                    type="number"
                    value={plotWidth}
                    onChange={(e) => setPlotWidth(Number(e.target.value))}
                    className="w-full bg-transparent text-lg font-bold text-amber-400 focus:outline-none"
                  />
                  <div className="text-[10px] text-slate-400">feet</div>
                </div>

                <div className="bg-white/10 backdrop-blur-md p-3.5 rounded-xl border border-white/10">
                  <div className="text-xs text-slate-300">Floors</div>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={plotFloors}
                    onChange={(e) => setPlotFloors(Number(e.target.value))}
                    className="w-full bg-transparent text-lg font-bold text-amber-400 focus:outline-none"
                  />
                  <div className="text-[10px] text-slate-400">levels</div>
                </div>
              </div>

              <Link
                to="/estimator"
                className="inline-flex items-center space-x-2 px-6 py-3 rounded-xl font-bold text-sm text-slate-950 bg-amber-500 hover:bg-amber-400 transition shadow-lg"
              >
                <span>Launch Full Detailed Estimator</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>

            {/* Quick Preview Output Card */}
            <div className="lg:col-span-6 bg-white text-slate-900 rounded-2xl p-6 shadow-2xl space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div>
                  <div className="text-xs text-slate-400 uppercase font-bold tracking-wider">Estimated Built-up Area</div>
                  <div className="text-2xl font-black text-slate-900">{previewArea.toLocaleString('en-IN')} sq.ft</div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-slate-400 uppercase font-bold tracking-wider">Approx Budget</div>
                  <div className="text-2xl font-black text-emerald-600">₹{(previewBudget / 100000).toFixed(1)} Lakhs</div>
                </div>
              </div>

              <div className="space-y-3 text-xs">
                <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 font-medium">
                  <span className="text-slate-600">Cement Bags (OPC/PPC)</span>
                  <span className="font-bold text-slate-900">{previewCement} Bags</span>
                </div>
                <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 font-medium">
                  <span className="text-slate-600">Structural TMT Rebar Steel</span>
                  <span className="font-bold text-slate-900">{previewSteel.toLocaleString('en-IN')} kg</span>
                </div>
                <div className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 font-medium">
                  <span className="text-slate-600">Red Bricks / AAC Blocks</span>
                  <span className="font-bold text-slate-900">{(previewArea * 8.5).toFixed(0)} Pieces</span>
                </div>
              </div>

              <div className="text-[11px] text-slate-400 italic">
                *Preliminary rule-based calculations. Actuals require architectural engineering drawings.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. HOW IT WORKS */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <h2 className="text-3xl font-black text-slate-900 tracking-tight">How SMART BUILD Works</h2>
          <p className="text-sm text-slate-500">From architectural requirement calculation to on-site unloading in 4 simple steps.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-600 flex items-center justify-center font-black text-lg">
              1
            </div>
            <h4 className="font-bold text-slate-900">Estimate Materials</h4>
            <p className="text-xs text-slate-500 leading-relaxed">
              Calculate exact cement, steel, bricks, and sand requirements using our automated rule-based civil estimator.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-blue-500/10 text-blue-600 flex items-center justify-center font-black text-lg">
              2
            </div>
            <h4 className="font-bold text-slate-900">Compare Suppliers</h4>
            <p className="text-xs text-slate-500 leading-relaxed">
              Compare transparent price quotes across certified cement plants, rebar yards, and local quarry suppliers.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-600 flex items-center justify-center font-black text-lg">
              3
            </div>
            <h4 className="font-bold text-slate-900">Order & Pay Securely</h4>
            <p className="text-xs text-slate-500 leading-relaxed">
              Add items to your cart and checkout with Cash on Delivery (COD) or instant Razorpay test sandbox.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/90 shadow-xs space-y-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-600 flex items-center justify-center font-black text-lg">
              4
            </div>
            <h4 className="font-bold text-slate-900">Track Site Delivery</h4>
            <p className="text-xs text-slate-500 leading-relaxed">
              Dedicated commercial trucks deliver straight to your construction plot with live status milestone tracking.
            </p>
          </div>
        </div>
      </section>

      {/* 6. CUSTOMER REVIEWS */}
      <section className="bg-slate-100/70 py-16 border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="text-center max-w-2xl mx-auto space-y-2">
            <h2 className="text-3xl font-black text-slate-900 tracking-tight">Trusted by Builders & Contractors</h2>
            <p className="text-sm text-slate-500">Real verified feedback from residential builders and civil contractors.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/80 space-y-3">
              <div className="flex text-amber-500">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
              </div>
              <p className="text-xs text-slate-600 leading-relaxed italic">
                "SMART BUILD saved us over ₹85,000 on our 3-floor residential project in Whitefield. The AI estimator's cement quantity was within 3% of our structural engineer's BOQ!"
              </p>
              <div className="pt-2 border-t border-slate-100 flex items-center space-x-3">
                <div className="w-9 h-9 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-xs">
                  KV
                </div>
                <div>
                  <div className="font-bold text-xs text-slate-900">Kiran Varma</div>
                  <div className="text-[10px] text-slate-400">Independent Home Builder, Bangalore</div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/80 space-y-3">
              <div className="flex text-amber-500">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
              </div>
              <p className="text-xs text-slate-600 leading-relaxed italic">
                "As a commercial steel supplier, the supplier dashboard makes stock and order management completely seamless. Orders come in with verified quantities and clear delivery directions."
              </p>
              <div className="pt-2 border-t border-slate-100 flex items-center space-x-3">
                <div className="w-9 h-9 rounded-full bg-emerald-600 text-white font-bold flex items-center justify-center text-xs">
                  SP
                </div>
                <div>
                  <div className="font-bold text-xs text-slate-900">Suresh Patel</div>
                  <div className="text-[10px] text-slate-400">Apex Steel Supplies</div>
                </div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200/80 space-y-3">
              <div className="flex text-amber-500">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
              </div>
              <p className="text-xs text-slate-600 leading-relaxed italic">
                "Delivery dispatch updates straight on the phone meant our unloading cranes were ready right on time. Zero site waiting time, verified invoice."
              </p>
              <div className="pt-2 border-t border-slate-100 flex items-center space-x-3">
                <div className="w-9 h-9 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">
                  MN
                </div>
                <div>
                  <div className="font-bold text-xs text-slate-900">Manoj Nambiar</div>
                  <div className="text-[10px] text-slate-400">Civil Contracting Lead</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7. FAQ SECTION */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">Frequently Asked Questions</h2>
          <p className="text-sm text-slate-500">Everything you need to know about material ordering and AI estimation.</p>
        </div>

        <div className="space-y-3 text-sm">
          <div className="bg-white p-5 rounded-xl border border-slate-200">
            <h4 className="font-bold text-slate-900">How accurate is the AI Material Estimator?</h4>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Our estimator uses standard IS civil engineering rules of thumb (IS 456 & CPWD norms) adjusting for building type, floor height, and quality tiers. It provides preliminary planning budgets for procurement before structural drawing finalization.
            </p>
          </div>

          <div className="bg-white p-5 rounded-xl border border-slate-200">
            <h4 className="font-bold text-slate-900">Are materials certified for structural construction?</h4>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              Yes, all suppliers on SMART BUILD are verified and products comply with Bureau of Indian Standards (BIS) grade certification including Tata Tiscon, UltraTech, JSW, and Birla.
            </p>
          </div>

          <div className="bg-white p-5 rounded-xl border border-slate-200">
            <h4 className="font-bold text-slate-900">What payment options are supported?</h4>
            <p className="text-xs text-slate-500 mt-1 leading-relaxed">
              We support Cash on Delivery (COD) on site arrival, as well as digital payments via Razorpay (UPI, Net Banking, Credit/Debit cards).
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
