import React, { useState } from 'react';
import { Phone, Mail, MapPin, Send, CheckCircle2 } from 'lucide-react';

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    setTimeout(() => setSubmitted(false), 4000);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-10">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Contact Builder Support</h1>
        <p className="text-sm text-slate-500">Need bulk procurement assistance or customized fleet logistics? Reach our team.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
        <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <h3 className="font-bold text-slate-900 text-lg">Send us a Message</h3>
          {submitted ? (
            <div className="p-4 bg-emerald-50 text-emerald-800 rounded-2xl text-xs font-semibold flex items-center space-x-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-600" />
              <span>Thank you! Your query has been received. Our site manager will call you within 2 hours.</span>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4 text-xs font-semibold">
              <div>
                <label className="block text-slate-700 mb-1">Your Name</label>
                <input required type="text" className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-amber-500" placeholder="Anand Sharma" />
              </div>
              <div>
                <label className="block text-slate-700 mb-1">Phone Number</label>
                <input required type="tel" className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 focus:ring-2 focus:ring-amber-500" placeholder="+91 98765 43210" />
              </div>
              <div>
                <label className="block text-slate-700 mb-1">Project Message</label>
                <textarea required rows={3} className="w-full px-3.5 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-amber-500" placeholder="Site location, required materials or tonnages..." />
              </div>
              <button type="submit" className="w-full py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold rounded-xl shadow-md transition">
                Send Query
              </button>
            </form>
          )}
        </div>

        <div className="space-y-4 text-xs">
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-bold text-slate-900 text-base">Direct Channels</h3>
            <div className="space-y-3 text-slate-600">
              <div className="flex items-center space-x-3">
                <Phone className="w-5 h-5 text-amber-500" />
                <span>+91 (080) 4567-8900 (Toll-Free)</span>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-5 h-5 text-amber-500" />
                <span>support@smartbuild.com</span>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="w-5 h-5 text-amber-500" />
                <span>Smart Build Towers, Outer Ring Road, Bellandur, Bangalore 560103</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
