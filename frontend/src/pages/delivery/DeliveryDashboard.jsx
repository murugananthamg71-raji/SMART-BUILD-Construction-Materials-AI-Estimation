import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import { 
  Truck, 
  MapPin, 
  Phone, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  Loader2, 
  Package, 
  Navigation,
  ArrowRight
} from 'lucide-react';

export default function DeliveryDashboard() {
  const { user } = useAuth();
  const [deliveries, setDeliveries] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadDeliveries = async () => {
    setLoading(true);
    try {
      const data = await api.get('/deliveries/assigned');
      setDeliveries(data || []);
    } catch (err) {
      console.error('Failed to load deliveries:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDeliveries();
  }, []);

  const handleUpdateStatus = async (deliveryId, newStatus) => {
    try {
      await api.put(`/deliveries/${deliveryId}/status`, {
        status: newStatus
      });
      await loadDeliveries();
    } catch (err) {
      alert('Failed to update delivery status.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="p-3 bg-purple-600 rounded-2xl text-white font-bold shadow-md">
            <Truck className="w-7 h-7" />
          </div>
          <div>
            <div className="text-xs font-bold text-purple-600 uppercase tracking-wider">Logistics Dispatch Partner</div>
            <h1 className="text-2xl font-black text-slate-900">{user?.name}</h1>
            <p className="text-xs text-slate-500">Commercial Fleet Operator • Vehicle: KA-01-MJ-4592</p>
          </div>
        </div>

        <span className="px-3 py-1 bg-emerald-100 text-emerald-800 font-bold text-xs rounded-full">
          Status: Available for Dispatch
        </span>
      </div>

      {/* Assigned Deliveries List */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900">Assigned Site Deliveries ({deliveries.length})</h2>

        {loading ? (
          <div className="py-12 text-center">
            <Loader2 className="w-8 h-8 animate-spin text-amber-500 mx-auto" />
          </div>
        ) : deliveries.length === 0 ? (
          <div className="bg-white rounded-3xl p-10 text-center border border-slate-200 space-y-3">
            <Truck className="w-10 h-10 text-slate-300 mx-auto" />
            <h3 className="font-bold text-slate-800">No Pending Deliveries</h3>
            <p className="text-xs text-slate-500">All assigned material shipments have been completed.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {deliveries.map((d) => (
              <div key={d.id} className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-5 flex flex-col justify-between">
                <div className="space-y-3">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                    <div>
                      <span className="font-mono font-bold text-slate-900 text-sm">{d.tracking_number}</span>
                      <div className="text-[10px] text-slate-400">Order: {d.order_number}</div>
                    </div>
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                      d.status === 'delivered'
                        ? 'bg-emerald-100 text-emerald-800'
                        : d.status === 'out_for_delivery'
                        ? 'bg-amber-100 text-amber-800'
                        : 'bg-blue-100 text-blue-800'
                    }`}>
                      {d.status}
                    </span>
                  </div>

                  {/* Customer Site Destination */}
                  <div className="space-y-2 text-xs">
                    <div className="flex items-start space-x-2 text-slate-700">
                      <MapPin className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
                      <div>
                        <span className="font-bold text-slate-900 block">{d.customer_name}</span>
                        <span>{d.address}, {d.city} {d.postal_code}</span>
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 text-slate-600">
                      <Phone className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span className="font-mono font-bold">{d.customer_phone}</span>
                    </div>
                  </div>
                </div>

                {/* Status Transition Actions */}
                <div className="pt-4 border-t border-slate-100 space-y-2">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Update Delivery Milestone</div>
                  <div className="grid grid-cols-3 gap-2">
                    <button
                      onClick={() => handleUpdateStatus(d.id, 'picked_up')}
                      disabled={d.status === 'picked_up' || d.status === 'delivered'}
                      className="py-2 px-2 rounded-xl text-[11px] font-bold bg-blue-50 text-blue-700 hover:bg-blue-100 disabled:opacity-30 transition"
                    >
                      1. Picked Up
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(d.id, 'out_for_delivery')}
                      disabled={d.status === 'out_for_delivery' || d.status === 'delivered'}
                      className="py-2 px-2 rounded-xl text-[11px] font-bold bg-amber-50 text-amber-700 hover:bg-amber-100 disabled:opacity-30 transition"
                    >
                      2. Out for Delivery
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(d.id, 'delivered')}
                      disabled={d.status === 'delivered'}
                      className="py-2 px-2 rounded-xl text-[11px] font-bold bg-emerald-600 text-white hover:bg-emerald-700 disabled:opacity-30 transition shadow-xs"
                    >
                      3. Confirm Delivered
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
