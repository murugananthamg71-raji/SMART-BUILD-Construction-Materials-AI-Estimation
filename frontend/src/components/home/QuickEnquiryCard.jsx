import React, { useState } from 'react';
import { 
  Send, 
  CheckCircle2, 
  Phone, 
  MapPin, 
  User, 
  Layers, 
  Clock, 
  MessageSquare, 
  Sparkles, 
  Loader2,
  FileText
} from 'lucide-react';
import api from '../../services/api';

export default function QuickEnquiryCard({ title = "Quick Material Enquiry & Order Booking", subtitle = "Direct wholesale pricing & fast site transit" }) {
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_phone: '',
    delivery_city: '',
    site_address: '',
    material_category: 'Cement (சிமெண்ட்)',
    quantity_description: '',
    urgency: 'immediate',
    notes: ''
  });

  const [loading, setLoading] = useState(false);
  const [submittedResult, setSubmittedResult] = useState(null);
  const [error, setError] = useState('');

  const categories = [
    'Cement (சிமெண்ட்)',
    'Steel / TMT Bars (இரும்பு)',
    'Bricks & Blocks (செங்கல்)',
    'Sand / M-Sand (மணல்)',
    'Gravel & Aggregates (ஜல்லி)',
    'Tiles & Flooring (டைல்ஸ்)',
    'Paint & Finishes (பெயிண்ட்)',
    'Plumbing & Pipes (பிளம்பிங்)',
    'Electrical & Wiring (எலக்ட்ரிக்கல்)',
    'Complete House Material Package (முழு கட்டுமான பொருட்கள்)'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.customer_name.trim() || !formData.customer_phone.trim() || !formData.delivery_city.trim()) {
      setError('Please fill in your name, phone number, and delivery city.');
      return;
    }

    setLoading(true);
    try {
      const res = await api.post('/enquiries', formData);
      setSubmittedResult(res);
      // Reset form
      setFormData({
        customer_name: '',
        customer_phone: '',
        delivery_city: '',
        site_address: '',
        material_category: 'Cement (சிமெண்ட்)',
        quantity_description: '',
        urgency: 'immediate',
        notes: ''
      });
    } catch (err) {
      console.error('Enquiry submission failed:', err);
      setError(err.response?.data?.detail || 'Failed to submit enquiry. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white/95 backdrop-blur-md rounded-3xl p-6 sm:p-7 border border-slate-200/90 shadow-2xl text-slate-900 transition-all">
      {submittedResult ? (
        <div className="py-8 text-center space-y-4">
          <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto shadow-inner animate-bounce">
            <CheckCircle2 className="w-10 h-10" />
          </div>
          <div className="space-y-1">
            <span className="inline-block px-3 py-1 bg-emerald-50 text-emerald-800 text-xs font-bold rounded-full uppercase tracking-wider">
              Enquiry & Booking Confirmed
            </span>
            <h3 className="text-xl sm:text-2xl font-black text-slate-900">
              Order Enquiry Received!
            </h3>
            <p className="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto">
              Thank you, <strong>{submittedResult.customer_name}</strong>. Our verified plant manager will contact you at <strong>{submittedResult.customer_phone}</strong> with wholesale rates within 15 minutes.
            </p>
          </div>

          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/80 text-left text-xs space-y-2">
            <div className="flex justify-between items-center pb-2 border-b border-slate-200">
              <span className="text-slate-500">Booking Reference:</span>
              <span className="font-mono font-black text-amber-600">{submittedResult.enquiry_number}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Material Category:</span>
              <span className="font-bold text-slate-800">{submittedResult.material_category}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Delivery Destination:</span>
              <span className="font-bold text-slate-800">{submittedResult.delivery_city}</span>
            </div>
          </div>

          <div className="pt-2 flex flex-col sm:flex-row gap-2">
            <button
              onClick={() => setSubmittedResult(null)}
              className="flex-1 py-2.5 px-4 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition"
            >
              Book Another Material
            </button>
            <a
              href={`tel:+919000000001`}
              className="py-2.5 px-4 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl transition inline-flex items-center justify-center space-x-1.5"
            >
              <Phone className="w-3.5 h-3.5" />
              <span>Call Helpline</span>
            </a>
          </div>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Card Header */}
          <div className="space-y-1">
            <div className="flex items-center justify-between">
              <div className="inline-flex items-center space-x-1.5 px-2.5 py-1 bg-amber-50 text-amber-800 rounded-lg text-[11px] font-black uppercase tracking-wider border border-amber-200">
                <Sparkles className="w-3 h-3 text-amber-600" />
                <span>Instant Site Booking</span>
              </div>
              <span className="text-[11px] font-semibold text-emerald-600 flex items-center">
                <Clock className="w-3 h-3 mr-1" /> 15-Min Response
              </span>
            </div>
            <h3 className="text-xl font-black text-slate-900 tracking-tight leading-snug">
              {title}
            </h3>
            <p className="text-xs text-slate-500">
              {subtitle}
            </p>
          </div>

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 text-red-600 text-xs rounded-xl">
              {error}
            </div>
          )}

          {/* Input Fields */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Customer Name */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Customer Name *
              </label>
              <div className="relative">
                <User className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  required
                  placeholder="e.g. Ramesh Kumar"
                  value={formData.customer_name}
                  onChange={(e) => setFormData({ ...formData, customer_name: e.target.value })}
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            {/* Mobile Number */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Phone / Mobile *
              </label>
              <div className="relative">
                <Phone className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="tel"
                  required
                  placeholder="+91 98765 43210"
                  value={formData.customer_phone}
                  onChange={(e) => setFormData({ ...formData, customer_phone: e.target.value })}
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Delivery City */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Delivery Site City *
              </label>
              <div className="relative">
                <MapPin className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  required
                  placeholder="e.g. Chennai, Bangalore, Salem"
                  value={formData.delivery_city}
                  onChange={(e) => setFormData({ ...formData, delivery_city: e.target.value })}
                  className="w-full pl-9 pr-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            {/* Material Category */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Material Required *
              </label>
              <div className="relative">
                <select
                  value={formData.material_category}
                  onChange={(e) => setFormData({ ...formData, material_category: e.target.value })}
                  className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  {categories.map((cat, i) => (
                    <option key={i} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {/* Approx Quantity / Requirements */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Quantity / Requirement
              </label>
              <input
                type="text"
                placeholder="e.g. 250 Bags / 3 Tons / 1500 sq.ft"
                value={formData.quantity_description}
                onChange={(e) => setFormData({ ...formData, quantity_description: e.target.value })}
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            {/* Urgency */}
            <div>
              <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
                Required Within
              </label>
              <select
                value={formData.urgency}
                onChange={(e) => setFormData({ ...formData, urgency: e.target.value })}
                className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
              >
                <option value="immediate">Immediate (Within 24 Hours)</option>
                <option value="1_week">Within 3 - 7 Days</option>
                <option value="planning">Planning Phase / Estimation</option>
              </select>
            </div>
          </div>

          {/* Delivery Site Address & Notes */}
          <div>
            <label className="block text-[11px] font-bold text-slate-700 uppercase mb-1">
              Site Address / Landmark (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. Plot #42, Anna Nagar Main Road, near Metro station"
              value={formData.site_address}
              onChange={(e) => setFormData({ ...formData, site_address: e.target.value })}
              className="w-full px-3 py-2 text-xs rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-400 hover:to-amber-300 text-slate-950 font-black text-sm rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center space-x-2 active:scale-98 disabled:opacity-70 cursor-pointer"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                <span>Submitting Enquiry...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Book Order / Get Instant Quote</span>
              </>
            )}
          </button>
        </form>
      )}
    </div>
  );
}
