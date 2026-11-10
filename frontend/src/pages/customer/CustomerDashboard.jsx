import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import api from '../../services/api';
import { 
  Package, 
  Clock, 
  CheckCircle2, 
  ShoppingCart, 
  Calculator, 
  Layers, 
  ArrowRight,
  TrendingUp,
  User,
  Truck,
  Loader2
} from 'lucide-react';

export default function CustomerDashboard() {
  const { user } = useAuth();
  const { itemCount } = useCart();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const data = await api.get('/orders');
        setOrders(data || []);
      } catch (err) {
        console.error('Failed to load customer orders:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const totalOrders = orders.length;
  const pendingOrders = orders.filter(o => ['pending', 'confirmed', 'processing', 'ready_for_dispatch', 'shipped', 'out_for_delivery'].includes(o.status)).length;
  const completedOrders = orders.filter(o => o.status === 'delivered').length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm">
        <div className="flex items-center space-x-4">
          <div className="w-14 h-14 rounded-2xl bg-amber-500 text-slate-950 font-black text-xl flex items-center justify-center shadow-md uppercase">
            {user?.name?.charAt(0) || 'C'}
          </div>
          <div>
            <div className="text-xs font-bold text-amber-600 uppercase tracking-wider">Customer Portal</div>
            <h1 className="text-2xl font-black text-slate-900">{user?.name}</h1>
            <p className="text-xs text-slate-500">{user?.email} • {user?.phone || 'No phone set'}</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Link
            to="/estimator"
            className="flex items-center space-x-1.5 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl shadow-sm transition"
          >
            <Calculator className="w-4 h-4" />
            <span>AI Estimator</span>
          </Link>
          <Link
            to="/materials"
            className="flex items-center space-x-1.5 px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition"
          >
            <Layers className="w-4 h-4" />
            <span>Browse Materials</span>
          </Link>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Total Orders</div>
          <div className="text-3xl font-black text-slate-900">{totalOrders}</div>
          <div className="text-[11px] text-slate-500">Lifetime purchases</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-amber-600 uppercase">Active / In-Transit</div>
          <div className="text-3xl font-black text-amber-600">{pendingOrders}</div>
          <div className="text-[11px] text-slate-500">Dispatches underway</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-emerald-600 uppercase">Delivered</div>
          <div className="text-3xl font-black text-emerald-600">{completedOrders}</div>
          <div className="text-[11px] text-slate-500">Completed shipments</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-blue-600 uppercase">Cart Items</div>
          <div className="text-3xl font-black text-blue-600">{itemCount}</div>
          <div className="text-[11px] text-slate-500">Ready to checkout</div>
        </div>
      </div>

      {/* Recent Orders List */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-5">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <Package className="w-5 h-5 text-amber-500" />
            <h2 className="font-bold text-slate-900 text-base">Recent Material Orders</h2>
          </div>
          <Link to="/materials" className="text-xs font-bold text-amber-600 hover:text-amber-500">
            Order More Materials
          </Link>
        </div>

        {loading ? (
          <div className="py-12 text-center">
            <Loader2 className="w-6 h-6 animate-spin text-amber-500 mx-auto" />
          </div>
        ) : orders.length === 0 ? (
          <div className="py-10 text-center space-y-3">
            <Package className="w-8 h-8 text-slate-300 mx-auto" />
            <p className="text-xs text-slate-500">You haven't placed any orders yet.</p>
            <Link to="/materials" className="inline-block text-xs font-bold text-amber-600">
              Browse Materials
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {orders.slice(0, 5).map((order) => (
              <div key={order.id} className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-mono font-bold text-slate-900 text-sm">{order.order_number}</span>
                    <span className="px-2 py-0.5 text-[10px] font-bold rounded-md uppercase bg-amber-50 text-amber-800">
                      {order.status}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500">
                    {new Date(order.ordered_at).toLocaleDateString()} • {order.items?.length || 1} material items
                  </div>
                </div>

                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <div className="font-black text-slate-900 text-sm">₹{Number(order.net_amount).toLocaleString('en-IN')}</div>
                    <div className="text-[10px] text-slate-400 capitalize">{order.payment_method} • {order.payment_status}</div>
                  </div>
                  <Link
                    to={`/orders/${order.id}`}
                    className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
