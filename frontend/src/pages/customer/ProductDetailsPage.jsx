import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../../services/api';
import { useCart } from '../../context/CartContext';
import { 
  Star, 
  ShieldCheck, 
  Truck, 
  ShoppingCart, 
  Check, 
  ArrowLeft, 
  Building2, 
  Layers, 
  Loader2,
  CheckCircle2
} from 'lucide-react';

export default function ProductDetailsPage() {
  const { id } = useParams();
  const { addToCart } = useCart();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await api.get(`/products/${id}`);
        setProduct(data);
      } catch (err) {
        console.error('Failed to load product details:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="py-24 text-center">
        <Loader2 className="w-8 h-8 animate-spin mx-auto text-amber-500" />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="py-20 text-center space-y-3">
        <h2 className="text-xl font-bold text-slate-800">Product Not Found</h2>
        <Link to="/materials" className="text-amber-600 font-bold text-sm">Return to Materials</Link>
      </div>
    );
  }

  const stock = product.inventory?.stock ?? 0;
  const isOutOfStock = stock <= 0;

  const handleAddToCart = async () => {
    if (isOutOfStock) return;
    try {
      await addToCart(product.id, quantity);
      setAdded(true);
      setTimeout(() => setAdded(false), 2500);
    } catch (err) {
      alert(err.message || 'Please log in to add materials to cart.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Back Button */}
      <Link to="/materials" className="inline-flex items-center space-x-1.5 text-xs font-bold text-slate-500 hover:text-slate-900 transition">
        <ArrowLeft className="w-4 h-4" />
        <span>Back to Materials Catalog</span>
      </Link>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-10 bg-white p-6 sm:p-10 rounded-3xl border border-slate-200/90 shadow-sm">
        {/* Left: Product Image */}
        <div className="md:col-span-6 space-y-4">
          <div className="aspect-4/3 rounded-2xl overflow-hidden bg-slate-100 border border-slate-100">
            <img
              src={product.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800&auto=format&fit=crop&q=80'}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          </div>
          <div className="grid grid-cols-3 gap-3 text-center text-xs text-slate-600 font-medium">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <ShieldCheck className="w-5 h-5 mx-auto text-emerald-500 mb-1" />
              <span>BIS Certified</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <Truck className="w-5 h-5 mx-auto text-blue-500 mb-1" />
              <span>Direct Site Transit</span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <CheckCircle2 className="w-5 h-5 mx-auto text-amber-500 mb-1" />
              <span>Verified Plant</span>
            </div>
          </div>
        </div>

        {/* Right: Specifications & Purchase */}
        <div className="md:col-span-6 space-y-6">
          <div className="space-y-2">
            {product.brand && (
              <span className="inline-block px-3 py-1 rounded-lg bg-amber-50 text-amber-900 text-xs font-bold uppercase tracking-wider">
                {product.brand}
              </span>
            )}
            <h1 className="text-2xl sm:text-3xl font-black text-slate-900 leading-tight">
              {product.name}
            </h1>
            <div className="flex items-center space-x-3 text-xs text-slate-500">
              <span>Category: <strong>{product.category?.name || 'Construction Material'}</strong></span>
              <span>•</span>
              <span className="flex items-center text-amber-500 font-bold">
                <Star className="w-3.5 h-3.5 fill-current mr-1" />
                {product.rating ? product.rating.toFixed(1) : '4.8'} ({product.total_reviews || 12} reviews)
              </span>
            </div>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80 flex items-baseline justify-between">
            <div>
              <div className="text-xs text-slate-400 uppercase font-semibold">Wholesale Price</div>
              <div className="text-3xl font-black text-slate-900">
                ₹{Number(product.price).toLocaleString('en-IN')}{' '}
                <span className="text-sm font-semibold text-slate-500">/ {product.unit}</span>
              </div>
            </div>

            <div className="text-right">
              <div className="text-xs text-slate-400 uppercase font-semibold">Inventory</div>
              <div className={`text-sm font-bold ${isOutOfStock ? 'text-red-600' : 'text-emerald-600'}`}>
                {isOutOfStock ? 'Out of Stock' : `${stock} ${product.unit} available`}
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">Description & Civil Specifications</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {product.description || 'High-grade building material formulated to match or exceed CPWD and IS requirements.'}
            </p>
          </div>

          <div className="space-y-2 text-xs text-slate-600 pt-2 border-t border-slate-100">
            <div><strong>Supplier:</strong> {product.supplier_name || 'Apex Infrastructure & Steel'} ({product.supplier_city || 'Bangalore'})</div>
            <div><strong>Min Order Qty:</strong> {product.min_order_quantity} {product.unit}</div>
          </div>

          {/* Add to Cart Controls */}
          <div className="flex items-center gap-4 pt-4 border-t border-slate-100">
            <div className="w-28">
              <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Quantity</label>
              <input
                type="number"
                min="1"
                max={stock || 1}
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, Math.min(stock, Number(e.target.value))))}
                disabled={isOutOfStock}
                className="w-full px-3 py-2.5 rounded-xl border border-slate-300 font-bold text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
              />
            </div>

            <button
              onClick={handleAddToCart}
              disabled={isOutOfStock}
              className={`flex-1 flex items-center justify-center space-x-2 py-3 px-6 rounded-xl font-bold text-sm transition shadow-md ${
                added
                  ? 'bg-emerald-600 text-white'
                  : isOutOfStock
                  ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
                  : 'bg-amber-500 hover:bg-amber-400 text-slate-950 active:scale-95'
              }`}
            >
              {added ? (
                <>
                  <Check className="w-5 h-5" />
                  <span>Added {quantity} {product.unit} to Cart</span>
                </>
              ) : (
                <>
                  <ShoppingCart className="w-5 h-5" />
                  <span>{isOutOfStock ? 'Sold Out' : 'Add to Cart'}</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
