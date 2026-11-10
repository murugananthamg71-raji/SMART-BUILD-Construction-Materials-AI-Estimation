import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../services/api';
import { 
  CheckCircle2, 
  Package, 
  Truck, 
  MapPin, 
  Download, 
  ArrowRight, 
  Building2,
  Clock,
  Loader2
} from 'lucide-react';

export default function OrderConfirmationPage() {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const data = await api.get(`/orders/${id}`);
        setOrder(data);
      } catch (err) {
        console.error('Failed to load order:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrder();
  }, [id]);

  if (loading) {
    return (
      <div className="py-24 text-center">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-amber-500" />
      </div>
    );
  }

  if (!order) {
    return (
      <div className="py-20 text-center space-y-4">
        <h2 className="text-xl font-bold text-slate-800">Order Not Found</h2>
        <Link to="/orders" className="text-amber-600 font-bold text-sm">View Your Orders</Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Success Badge & Headline */}
      <div className="bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 text-center space-y-4 shadow-sm">
        <div className="w-16 h-16 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mx-auto shadow-inner">
          <CheckCircle2 className="w-10 h-10" />
        </div>
        <div className="space-y-1">
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900">Order Confirmed!</h1>
          <p className="text-sm text-slate-500">
            Thank you for ordering with SMART BUILD. Your materials have been reserved and routed to the nearest dispatch yard.
          </p>
        </div>

        <div className="inline-flex items-center space-x-3 bg-slate-50 px-4 py-2 rounded-xl text-xs font-mono font-bold text-slate-800 border border-slate-200">
          <span>Order #: {order.order_number}</span>
          <span className="text-slate-300">|</span>
          <span className="text-emerald-700 uppercase font-semibold">Status: {order.status}</span>
        </div>
      </div>

      {/* Shipment Logistics & Delivery Tracking */}
      {order.delivery && (
        <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <div className="flex items-center space-x-2">
              <Truck className="w-5 h-5 text-amber-500" />
              <h3 className="font-bold text-slate-900 text-base">Shipment & Delivery Status</h3>
            </div>
            <span className="px-3 py-1 bg-amber-50 text-amber-800 font-bold text-xs rounded-full uppercase">
              {order.delivery.status}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-3.5 bg-slate-50 rounded-xl space-y-1">
              <span className="text-slate-400 font-semibold uppercase">Tracking Number</span>
              <div className="font-mono font-bold text-slate-900 text-sm">{order.delivery.tracking_number}</div>
            </div>

            <div className="p-3.5 bg-slate-50 rounded-xl space-y-1">
              <span className="text-slate-400 font-semibold uppercase">Destination Site</span>
              <div className="font-medium text-slate-800">
                {order.delivery_address?.street_address}, {order.delivery_address?.city}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Ordered Line Items */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <h3 className="font-bold text-slate-900 text-base border-b border-slate-100 pb-3">Ordered Materials</h3>
        <div className="divide-y divide-slate-100">
          {order.items.map((item) => (
            <div key={item.id} className="py-3 flex justify-between items-center text-xs">
              <div>
                <div className="font-bold text-slate-900 text-sm">{item.product_name}</div>
                <div className="text-slate-400">Qty: {item.quantity} {item.unit || 'units'} • Supplier: {item.supplier_name || 'Apex Steel'}</div>
              </div>
              <div className="font-bold text-slate-900 text-sm">
                ₹{Number(item.total_price).toLocaleString('en-IN')}
              </div>
            </div>
          ))}
        </div>

        <div className="pt-4 border-t border-slate-100 space-y-2 text-xs font-medium text-slate-600">
          <div className="flex justify-between">
            <span>Material Subtotal</span>
            <span>₹{Number(order.total_amount).toLocaleString('en-IN')}</span>
          </div>
          <div className="flex justify-between">
            <span>GST (18%)</span>
            <span>₹{Number(order.tax_amount).toLocaleString('en-IN')}</span>
          </div>
          <div className="flex justify-between">
            <span>Logistics Freight</span>
            <span>{Number(order.delivery_fee) === 0 ? 'FREE' : `₹${Number(order.delivery_fee).toLocaleString('en-IN')}`}</span>
          </div>
          <div className="pt-2 border-t border-slate-100 flex justify-between items-baseline font-black text-slate-900 text-base">
            <span>Total Amount</span>
            <span>₹{Number(order.net_amount).toLocaleString('en-IN')}</span>
          </div>
        </div>
      </div>

      {/* Action Navigation */}
      <div className="flex flex-col sm:flex-row gap-3">
        <button
          onClick={() => window.print()}
          className="flex-1 flex items-center justify-center space-x-2 py-3 px-4 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl shadow-md transition"
        >
          <Download className="w-4 h-4" />
          <span>Download Tax Invoice</span>
        </button>

        <Link
          to="/materials"
          className="flex-1 flex items-center justify-center space-x-2 py-3 px-4 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl shadow-md transition"
        >
          <span>Continue Ordering</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
