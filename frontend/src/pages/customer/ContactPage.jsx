import React, { useState } from 'react';
import { Phone, Mail, MapPin, Send, CheckCircle2, Globe, ExternalLink, User } from 'lucide-react';

const LinkedInIcon = (props) => (
  <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
    <path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 8.76a1.53 1.53 0 1 0 0-3.05 1.53 1.53 0 0 0 0 3.05m1.39 9.74v-8.37H5.07v8.37h2.78Z" />
  </svg>
);

const GitHubIcon = (props) => (
  <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
    <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0 0 22 12.017C22 6.484 17.522 2 12 2Z" />
  </svg>
);

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
          {/* Developer Contact Details Card */}
          <div className="bg-white p-6 sm:p-7 rounded-3xl border border-slate-200/90 shadow-sm space-y-5">
            <div>
              <span className="text-[10px] font-bold uppercase tracking-wider text-amber-700 bg-amber-50 px-2.5 py-1 rounded-md border border-amber-200">
                Your Contact Details
              </span>
              <h3 className="font-black text-slate-900 text-xl mt-2.5">Muruganantham G</h3>
              <p className="text-xs font-bold text-amber-600">Full Stack Web Developer</p>
            </div>

            <div className="space-y-2.5 text-slate-700">
              <div className="flex items-center space-x-3">
                <MapPin className="w-4 h-4 text-amber-500 shrink-0" />
                <span className="font-semibold text-slate-700">Coimbatore, Tamil Nadu, India</span>
              </div>
            </div>

            {/* Social & Portfolio Links */}
            <div className="pt-2 border-t border-slate-100 flex flex-col space-y-2">
              <a
                href="https://muruganantham-portfolio-13.vercel.app/?utm_source=chatgpt.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 hover:bg-amber-50 border border-slate-200 hover:border-amber-300 transition group"
              >
                <div className="flex items-center space-x-2.5">
                  <Globe className="w-4 h-4 text-amber-600" />
                  <span className="font-bold text-slate-800 text-xs group-hover:text-amber-700">My Portfolio</span>
                </div>
                <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-amber-600" />
              </a>

              <a
                href="https://linkedin.com/in/muruganantham-g-7893b2267?utm_source=chatgpt.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 transition group"
              >
                <div className="flex items-center space-x-2.5">
                  <LinkedInIcon className="w-4 h-4 text-blue-600" />
                  <span className="font-bold text-slate-800 text-xs group-hover:text-blue-700">LinkedIn Profile</span>
                </div>
                <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
              </a>

              <a
                href="https://github.com/murugananthamg71-raji?utm_source=chatgpt.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-between p-2.5 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 hover:border-slate-300 transition group"
              >
                <div className="flex items-center space-x-2.5">
                  <GitHubIcon className="w-4 h-4 text-slate-900" />
                  <span className="font-bold text-slate-800 text-xs group-hover:text-slate-900">GitHub Profile</span>
                </div>
                <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-slate-900" />
              </a>
            </div>
          </div>

          {/* Direct Channels */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-3">
            <h4 className="font-bold text-slate-900 text-sm">Direct Channels</h4>
            <div className="space-y-2.5 text-slate-600 text-xs">
              <div className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-amber-500 shrink-0" />
                <a href="tel:+918870642691" className="hover:text-amber-600 font-semibold transition">+91 8870642691</a>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-amber-500 shrink-0" />
                <a href="mailto:murugananthamg71@gmail.com" className="hover:text-amber-600 font-semibold transition">murugananthamg71@gmail.com</a>
              </div>
              <div className="flex items-center space-x-3">
                <MapPin className="w-4 h-4 text-amber-500 shrink-0" />
                <span className="font-semibold text-slate-700">Coimbatore - 641105, Tamil Nadu, India</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
