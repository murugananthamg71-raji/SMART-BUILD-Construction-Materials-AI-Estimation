import React from 'react';
import { Building2, ShieldCheck, Cpu, Truck, Users, Award } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
      <div className="text-center space-y-4 max-w-2xl mx-auto">
        <div className="w-14 h-14 bg-amber-500 rounded-2xl flex items-center justify-center mx-auto text-slate-950 font-bold shadow-md">
          <Building2 className="w-8 h-8" />
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">About SMART BUILD</h1>
        <p className="text-sm text-slate-500 leading-relaxed">
          Pioneering transparent, AI-driven construction material procurement for residential builders, infrastructure contractors, and industrial developers.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-3">
          <Cpu className="w-8 h-8 text-amber-500" />
          <h3 className="font-bold text-slate-900 text-base">Civil Engineering AI</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Eliminate costly material estimation errors. Our rule engine calculates accurate cement, steel, rebar, and aggregate requirements using IS:456 and CPWD standards.
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-3">
          <ShieldCheck className="w-8 h-8 text-emerald-500" />
          <h3 className="font-bold text-slate-900 text-base">Factory Direct & Certified</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Every cement bag and steel rebar on our platform is sourced direct from approved BIS-certified industrial manufacturers with full batch test certificates.
          </p>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-3">
          <Truck className="w-8 h-8 text-blue-500" />
          <h3 className="font-bold text-slate-900 text-base">Heavy Commercial Logistics</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Dedicated fleet network of commercial tippers and trailers delivering straight to your construction plot with milestone status tracking.
          </p>
        </div>
      </div>
    </div>
  );
}
