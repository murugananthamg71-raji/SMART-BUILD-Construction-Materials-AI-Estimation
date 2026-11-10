import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { 
  ShoppingCart, 
  Trash2, 
  Plus, 
  Minus, 
  ArrowRight, 
  ShieldCheck, 
  Truck, 
  Building2,
  AlertCircle
} from 'lucide-react';

export default function CartPage() {
  const { cart, itemCount, subtotal, taxAmount, deliveryFee, grandTotal, updateQuantity, removeItem, clearCart, loading } = useCart();
  const navigate = useNavigate();

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center space-y-5">
        <div className="w-20 h-20 bg-amber-50 rounded-full flex items-center justify-center mx-auto text-amber-500 shadow-inner">
          <ShoppingCart className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-black text-slate-900">Your Cart is Empty</h2>
        <p className="text-sm text-slate-500 max-w-sm mx-auto">
          Explore our construction materials catalog or use the AI Estimator to calculate required materials for your site.
        </p>
        <div className="flex justify-center gap-3 pt-2">
          <Link
            to="/materials"
            className="px-6 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl shadow-md transition"
          >
            Browse Materials
          </Link>
          <Link
            to="/estimator"
            className="px-6 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl transition"
          >
            AI Estimator
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black text-slate-900 tracking-tight">Shopping Cart</h1>
          <p className="text-sm text-slate-500">Review selected construction materials and delivery charges before checkout.</p>
        </div>
        <button
          onClick={clearCart}
          className="text-xs font-semibold text-red-500 hover:text-red-700 flex items-center space-x-1"
        >
          <Trash2 className="w-4 h-4" />
          <span>Clear Cart</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Cart Items List */}
        <div className="lg:col-span-8 bg-white rounded-3xl border border-slate-200/90 shadow-sm overflow-hidden divide-y divide-slate-100">
          {cart.items.map((item) => (
            <div key={item.id} className="p-4 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                <img
                  src={item.product_image || 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=300&auto=format&fit=crop&q=60'}
                  alt={item.product_name}
                  className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl object-cover bg-slate-100 shrink-0"
                />
                <div className="space-y-1">
                  {item.product_brand && (
                    <span className="text-[10px] font-bold uppercase tracking-wider text-amber-700 bg-amber-50 px-2 py-0.5 rounded-md">
                      {item.product_brand}
                    </span>
                  )}
                  <h4 className="font-bold text-slate-900 text-sm sm:text-base leading-snug">
                    {item.product_name}
                  </h4>
                  <div className="text-xs text-slate-500">
                    ₹{Number(item.unit_price).toLocaleString('en-IN')} per {item.unit}
                  </div>
                </div>
              </div>

              {/* Quantity Controls & Line Total */}
              <div className="flex items-center justify-between sm:justify-end w-full sm:w-auto gap-6">
                <div className="flex items-center border border-slate-200 rounded-xl bg-slate-50 p-1">
                  <button
                    onClick={() => item.quantity > 1 ? updateQuantity(item.id, item.quantity - 1) : removeItem(item.id)}
                    className="p-1 rounded-lg text-slate-600 hover:bg-white transition"
                  >
                    <Minus className="w-3.5 h-3.5" />
                  </button>
                  <span className="px-3 text-xs font-bold text-slate-900">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                    className="p-1 rounded-lg text-slate-600 hover:bg-white transition"
                  >
                    <Plus className="w-3.5 h-3.5" />
                  </button>
                </div>

                <div className="text-right">
                  <div className="font-black text-slate-900 text-base">
                    ₹{Number(item.total_price).toLocaleString('en-IN')}
                  </div>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-[11px] text-red-500 hover:text-red-700 font-medium"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary Card */}
        <div className="lg:col-span-4 bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-5">
          <h3 className="font-bold text-slate-900 text-base border-b border-slate-100 pb-3">Order Summary</h3>

          <div className="space-y-3 text-xs font-medium text-slate-600">
            <div className="flex justify-between">
              <span>Materials Subtotal ({itemCount} items)</span>
              <span className="font-bold text-slate-900">₹{Number(subtotal).toLocaleString('en-IN')}</span>
            </div>

            <div className="flex justify-between">
              <span>GST (18% on Construction Materials)</span>
              <span className="font-bold text-slate-900">₹{Number(taxAmount).toLocaleString('en-IN')}</span>
            </div>

            <div className="flex justify-between items-center">
              <div>
                <span>Site Delivery & Freight</span>
                <div className="text-[10px] text-slate-400">Free on bulk orders &gt; ₹50,000</div>
              </div>
              <span className="font-bold text-slate-900">
                {Number(deliveryFee) === 0 ? <span className="text-emerald-600">FREE</span> : `₹${Number(deliveryFee).toLocaleString('en-IN')}`}
              </span>
            </div>

            <div className="pt-3 border-t border-slate-100 flex justify-between items-baseline text-slate-900">
              <span className="text-sm font-bold">Estimated Total</span>
              <span className="text-2xl font-black text-slate-900">
                ₹{Number(grandTotal).toLocaleString('en-IN')}
              </span>
            </div>
          </div>

          <button
            onClick={() => navigate('/checkout')}
            className="w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl text-slate-950 font-bold text-sm bg-amber-500 hover:bg-amber-400 transition shadow-md active:scale-95"
          >
            <span>Proceed to Checkout</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <div className="space-y-2 pt-3 border-t border-slate-100 text-[11px] text-slate-400">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-500 shrink-0" />
              <span>Certified factory-direct stock verified by BIS</span>
            </div>
            <div className="flex items-center space-x-2">
              <Truck className="w-4 h-4 text-blue-500 shrink-0" />
              <span>Unloading & transit insurance included</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
