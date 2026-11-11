import React from 'react';
import { Link } from 'react-router-dom';
import { Building2, Phone, Mail, MapPin, ShieldCheck, Truck, Clock } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#102A43] text-slate-300 pt-16 pb-12 border-t border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Brand Info */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2.5">
              <div className="bg-amber-500 p-2 rounded-xl text-slate-950 font-bold shadow-md">
                <Building2 className="w-6 h-6" />
              </div>
              <span className="text-xl font-black text-white tracking-tight">SMART BUILD</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              India's intelligent construction marketplace connecting builders, contractors, and verified suppliers with transparent pricing and AI material estimation.
            </p>
            <div className="flex items-center space-x-4 pt-2 text-xs font-semibold text-amber-400">
              <span className="flex items-center gap-1"><ShieldCheck className="w-4 h-4" /> 100% Verified Quality</span>
              <span className="flex items-center gap-1"><Truck className="w-4 h-4" /> Direct Site Delivery</span>
            </div>
          </div>

          {/* Popular Categories */}
          <div>
            <h4 className="text-white font-bold text-sm tracking-wider uppercase mb-4">Core Materials</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/materials?category=cement" className="hover:text-amber-400 transition">OPC & PPC Cement</Link></li>
              <li><Link to="/materials?category=steel" className="hover:text-amber-400 transition">Fe550D TMT Steel Rebar</Link></li>
              <li><Link to="/materials?category=bricks" className="hover:text-amber-400 transition">Red Clay & AAC Blocks</Link></li>
              <li><Link to="/materials?category=sand" className="hover:text-amber-400 transition">Manufactured M-Sand & P-Sand</Link></li>
              <li><Link to="/materials?category=gravel" className="hover:text-amber-400 transition">20mm Blue Metal Granite</Link></li>
              <li><Link to="/materials?category=tiles" className="hover:text-amber-400 transition">Vitrified Flooring Tiles</Link></li>
            </ul>
          </div>

          {/* Quick Platform Links */}
          <div>
            <h4 className="text-white font-bold text-sm tracking-wider uppercase mb-4">Platform</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/estimator" className="text-amber-400 hover:text-amber-300 font-semibold transition">AI Material Estimator</Link></li>
              <li><Link to="/materials" className="hover:text-amber-400 transition">Browse Catalog</Link></li>
              <li><Link to="/register" className="hover:text-amber-400 transition">Become a Verified Supplier</Link></li>
              <li><Link to="/about" className="hover:text-amber-400 transition">About SMART BUILD</Link></li>
              <li><Link to="/contact" className="hover:text-amber-400 transition">Customer Help & FAQ</Link></li>
            </ul>
          </div>

          {/* Contact & Support */}
          <div>
            <h4 className="text-white font-bold text-sm tracking-wider uppercase mb-4">Builder Support 24/7</h4>
            <div className="space-y-3 text-sm">
              <div className="flex items-start space-x-3 text-slate-300">
                <Phone className="w-4 h-4 text-amber-400 mt-1 shrink-0" />
                <span>+91 (080) 4567-8900<br /><span className="text-xs text-slate-400">Toll-free construction hotline</span></span>
              </div>
              <div className="flex items-start space-x-3 text-slate-300">
                <Mail className="w-4 h-4 text-amber-400 mt-1 shrink-0" />
                <span>support@smartbuild.com</span>
              </div>
              <div className="flex items-start space-x-3 text-slate-300">
                <MapPin className="w-4 h-4 text-amber-400 mt-1 shrink-0" />
                <span>Smart Build Towers, Outer Ring Road, Bangalore - 560103</span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-slate-700/60 flex flex-col md:flex-row items-center justify-between text-xs text-slate-400 gap-4">
          <p>© 2026 SMART BUILD Technologies Inc. All rights reserved.</p>
          <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 text-slate-300">
            <span>Developed by <strong className="text-amber-400 font-bold">Muruganantham G</strong> (Coimbatore)</span>
            <span>•</span>
            <a href="https://muruganantham-portfolio-13.vercel.app/?utm_source=chatgpt.com" target="_blank" rel="noopener noreferrer" className="text-amber-400 hover:underline font-semibold">Portfolio</a>
            <span>•</span>
            <a href="https://linkedin.com/in/muruganantham-g-7893b2267?utm_source=chatgpt.com" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline font-semibold">LinkedIn</a>
            <span>•</span>
            <a href="https://github.com/murugananthamg71-raji?utm_source=chatgpt.com" target="_blank" rel="noopener noreferrer" className="text-slate-100 hover:underline font-semibold">GitHub</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
