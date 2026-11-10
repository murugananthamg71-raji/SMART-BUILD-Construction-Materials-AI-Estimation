import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../../services/api';
import { Package, Clock, Truck, ArrowRight, Loader2 } from 'lucide-react';

export default function OrderHistoryPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const data = await api.get('/orders');
        setOrders(data || []);
      } catch (err) {
        console.error('Failed to load orders:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Your Order History</h1>
        <p className="text-sm text-slate-500">Track and manage past construction material purchases and dispatch logs.</p>
      </div>

      {loading ? (
        <div className="py-24 text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto text-amber-500" />
        </div>
      ) : orders.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 space-y-4 max-w-md mx-auto">
          <Package className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="font-bold text-slate-800 text-lg">No Orders Placed Yet</h3>
          <p className="text-xs text-slate-500">Discover construction materials in the catalog and place your first site order.</p>
          <Link
            to="/materials"
            className="inline-block px-5 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl shadow-md transition"
          >
            Browse Materials
          </Link>
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm overflow-hidden divide-y divide-slate-100">
          {orders.map((order) => (
            <div key={order.id} className="p-5 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="space-y-1.5">
                <div className="flex items-center space-x-2.5">
                  <span className="font-mono font-bold text-slate-900 text-base">{order.order_number}</span>
                  <span className={`px-2.5 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider ${
                    order.status === 'delivered'
                      ? 'bg-emerald-100 text-emerald-800'
                      : 'bg-amber-100 text-amber-800'
                  }`}>
                    {order.status}
                  </span>
                </div>
                <div className="text-xs text-slate-500">
                  Ordered on {new Date(order.ordered_at).toLocaleDateString()} • {order.items?.length || 1} material items
                </div>
                {order.delivery && (
                  <div className="flex items-center space-x-1 text-xs text-slate-600">
                    <Truck className="w-3.5 h-3.5 text-amber-500" />
                    <span>Tracking: <strong className="font-mono">{order.delivery.tracking_number}</strong></span>
                  </div>
                )}
              </div>

              <div className="flex items-center space-x-6 w-full sm:w-auto justify-between sm:justify-end">
                <div className="text-right">
                  <div className="text-base font-black text-slate-900">
                    ₹{Number(order.net_amount).toLocaleString('en-IN')}
                  </div>
                  <div className="text-[10px] text-slate-400 uppercase font-semibold">
                    {order.payment_method} • {order.payment_status}
                  </div>
                </div>

                <Link
                  to={`/orders/${order.id}`}
                  className="flex items-center space-x-1.5 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition"
                >
                  <span>Details</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
