import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import { 
  Building2, 
  MapPin, 
  CreditCard, 
  Truck, 
  ShieldCheck, 
  Loader2, 
  AlertCircle, 
  CheckCircle2,
  DollarSign
} from 'lucide-react';

export default function CheckoutPage() {
  const { cart, itemCount, subtotal, taxAmount, deliveryFee, grandTotal, refreshCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  // Address fields
  const [recipientName, setRecipientName] = useState(user?.name || '');
  const [phone, setPhone] = useState(user?.phone || '+91 98888 11111');
  const [streetAddress, setStreetAddress] = useState('Plot 104, Outer Ring Road, Bellandur');
  const [landmark, setLandmark] = useState('Near Gate 2, Tech Park');
  const [city, setCity] = useState('Bangalore');
  const [state, setState] = useState('Karnataka');
  const [postalCode, setPostalCode] = useState('560103');

  // Payment Method
  const [paymentMethod, setPaymentMethod] = useState('cod'); // 'cod' or 'razorpay'
  const [notes, setNotes] = useState('Unload near Tower B foundation');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!cart || cart.items.length === 0) {
    navigate('/cart');
    return null;
  }

  const handlePlaceOrder = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const orderPayload = {
        payment_method: paymentMethod,
        notes: notes,
        new_address: {
          title: 'Project Site',
          recipient_name: recipientName,
          recipient_phone: phone,
          street_address: streetAddress,
          landmark: landmark,
          city: city,
          state: state,
          postal_code: postalCode,
          is_default: true
        }
      };

      const orderData = await api.post('/orders', orderPayload);
      await refreshCart();
      navigate(`/orders/${orderData.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || 'Order placement failed. Please verify site address and available stock.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="space-y-1">
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">Checkout & Site Delivery</h1>
        <p className="text-sm text-slate-500">Provide construction site coordinates and select your preferred payment mode.</p>
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-start space-x-2.5">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handlePlaceOrder} className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Side: Address & Payment Details */}
        <div className="lg:col-span-7 space-y-6">
          {/* Site Delivery Address Card */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center space-x-2 pb-3 border-b border-slate-100">
              <MapPin className="w-5 h-5 text-amber-500" />
              <h2 className="font-bold text-slate-900 text-base">Site Delivery Address</h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Site Contact Person</label>
                <input
                  type="text"
                  required
                  value={recipientName}
                  onChange={(e) => setRecipientName(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Contact Phone</label>
                <input
                  type="tel"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Plot / Street Address / Landmark</label>
              <input
                type="text"
                required
                value={streetAddress}
                onChange={(e) => setStreetAddress(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                placeholder="Plot Number, Road Name, Site Gate"
              />
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">City</label>
                <input
                  type="text"
                  required
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">State</label>
                <input
                  type="text"
                  required
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Postal Code</label>
                <input
                  type="text"
                  required
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Site Unloading Instructions</label>
              <textarea
                rows={2}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                placeholder="Crane access points, ground clearing instructions..."
              />
            </div>
          </div>

          {/* Payment Method Selector */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-4">
            <div className="flex items-center space-x-2 pb-3 border-b border-slate-100">
              <CreditCard className="w-5 h-5 text-amber-500" />
              <h2 className="font-bold text-slate-900 text-base">Payment Method</h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div
                onClick={() => setPaymentMethod('cod')}
                className={`p-4 rounded-2xl border-2 cursor-pointer transition flex items-start space-x-3 ${
                  paymentMethod === 'cod'
                    ? 'border-amber-500 bg-amber-50/50'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className={`w-5 h-5 rounded-full border-2 mt-0.5 flex items-center justify-center ${
                  paymentMethod === 'cod' ? 'border-amber-500 bg-amber-500' : 'border-slate-300'
                }`}>
                  {paymentMethod === 'cod' && <div className="w-2 h-2 rounded-full bg-white" />}
                </div>
                <div>
                  <div className="font-bold text-slate-900 text-sm">Cash on Delivery (COD)</div>
                  <div className="text-xs text-slate-500 mt-0.5">Pay after materials arrive & are inspected on site.</div>
                </div>
              </div>

              <div
                onClick={() => setPaymentMethod('razorpay')}
                className={`p-4 rounded-2xl border-2 cursor-pointer transition flex items-start space-x-3 ${
                  paymentMethod === 'razorpay'
                    ? 'border-amber-500 bg-amber-50/50'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <div className={`w-5 h-5 rounded-full border-2 mt-0.5 flex items-center justify-center ${
                  paymentMethod === 'razorpay' ? 'border-amber-500 bg-amber-500' : 'border-slate-300'
                }`}>
                  {paymentMethod === 'razorpay' && <div className="w-2 h-2 rounded-full bg-white" />}
                </div>
                <div>
                  <div className="font-bold text-slate-900 text-sm">Razorpay (Test Sandbox)</div>
                  <div className="text-xs text-slate-500 mt-0.5">Instant sandbox UPI, Card, NetBanking simulation.</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Side: Order Review Summary */}
        <div className="lg:col-span-5 bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-5">
          <h3 className="font-bold text-slate-900 text-base border-b border-slate-100 pb-3">Final Order Review</h3>

          <div className="space-y-3 max-h-64 overflow-y-auto pr-1 divide-y divide-slate-100">
            {cart.items.map((item) => (
              <div key={item.id} className="pt-2.5 first:pt-0 flex justify-between text-xs">
                <div>
                  <div className="font-bold text-slate-900">{item.product_name}</div>
                  <div className="text-slate-400">Qty: {item.quantity} {item.unit}</div>
                </div>
                <div className="font-bold text-slate-900">
                  ₹{Number(item.total_price).toLocaleString('en-IN')}
                </div>
              </div>
            ))}
          </div>

          <div className="space-y-2.5 pt-3 border-t border-slate-100 text-xs text-slate-600 font-medium">
            <div className="flex justify-between">
              <span>Subtotal</span>
              <span className="font-bold text-slate-900">₹{Number(subtotal).toLocaleString('en-IN')}</span>
            </div>
            <div className="flex justify-between">
              <span>GST (18%)</span>
              <span className="font-bold text-slate-900">₹{Number(taxAmount).toLocaleString('en-IN')}</span>
            </div>
            <div className="flex justify-between">
              <span>Site Freight</span>
              <span className="font-bold text-slate-900">
                {Number(deliveryFee) === 0 ? <span className="text-emerald-600">FREE</span> : `₹${Number(deliveryFee).toLocaleString('en-IN')}`}
              </span>
            </div>
            <div className="pt-3 border-t border-slate-100 flex justify-between items-baseline text-slate-900">
              <span className="text-sm font-bold">Payable Net Amount</span>
              <span className="text-2xl font-black text-slate-900">
                ₹{Number(grandTotal).toLocaleString('en-IN')}
              </span>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl text-slate-950 font-bold text-sm bg-amber-500 hover:bg-amber-400 transition shadow-lg disabled:opacity-50 active:scale-95"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Processing Order...</span>
              </>
            ) : (
              <span>Confirm & Place Order</span>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
