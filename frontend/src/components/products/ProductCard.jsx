import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Star, ShoppingCart, Check, AlertTriangle, Truck } from 'lucide-react';
import { useCart } from '../../context/CartContext';

export default function ProductCard({ product }) {
  const { addToCart } = useCart();
  const [adding, setAdding] = useState(false);
  const [added, setAdded] = useState(false);

  const stock = product.inventory?.stock ?? 0;
  const isOutOfStock = stock <= 0;
  const imageSrc = product.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500&auto=format&fit=crop&q=60';

  const handleAddToCart = async (e) => {
    e.preventDefault();
    if (isOutOfStock || adding) return;

    try {
      setAdding(true);
      await addToCart(product.id, 1);
      setAdded(true);
      setTimeout(() => setAdded(false), 2000);
    } catch (err) {
      alert(err.message || 'Failed to add to cart. Please sign in.');
    } finally {
      setAdding(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200/90 shadow-xs hover:shadow-xl transition-all duration-300 flex flex-col justify-between overflow-hidden group">
      <div>
        {/* Product Image & Badges */}
        <Link to={`/materials/${product.id}`} className="block relative aspect-4/3 overflow-hidden bg-slate-100">
          <img
            src={imageSrc}
            alt={product.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
          {product.brand && (
            <span className="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-xs text-white text-[11px] font-bold px-2.5 py-1 rounded-lg">
              {product.brand}
            </span>
          )}
          {isOutOfStock ? (
            <span className="absolute top-3 right-3 bg-red-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-md uppercase">
              Out of Stock
            </span>
          ) : (
            <span className="absolute top-3 right-3 bg-emerald-600/90 backdrop-blur-xs text-white text-[10px] font-bold px-2 py-0.5 rounded-md uppercase">
              In Stock ({stock} {product.unit})
            </span>
          )}
        </Link>

        {/* Product Details */}
        <div className="p-4 sm:p-5 space-y-2.5">
          <div className="flex items-center justify-between text-xs text-slate-500">
            <span className="truncate max-w-[140px] font-medium">
              By {product.supplier_name || 'Verified Supplier'}
            </span>
            <div className="flex items-center space-x-1 text-amber-500 font-bold shrink-0">
              <Star className="w-3.5 h-3.5 fill-current" />
              <span>{product.rating ? product.rating.toFixed(1) : '4.8'}</span>
            </div>
          </div>

          <Link to={`/materials/${product.id}`} className="block">
            <h3 className="font-bold text-slate-900 text-base leading-snug hover:text-amber-600 transition line-clamp-2">
              {product.name}
            </h3>
          </Link>

          <p className="text-xs text-slate-500 line-clamp-2 leading-relaxed">
            {product.description || 'High-grade civil construction certified material with delivery available direct to site.'}
          </p>
        </div>
      </div>

      {/* Pricing & Call to Action */}
      <div className="p-4 sm:p-5 pt-0 border-t border-slate-100 mt-2 flex items-center justify-between gap-3">
        <div>
          <div className="text-[11px] text-slate-400 uppercase font-semibold">Price per {product.unit}</div>
          <div className="text-lg font-black text-slate-900">
            ₹{Number(product.price).toLocaleString('en-IN')}
          </div>
        </div>

        <button
          onClick={handleAddToCart}
          disabled={isOutOfStock || adding}
          className={`flex items-center justify-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-bold transition shadow-sm ${
            added
              ? 'bg-emerald-600 text-white'
              : isOutOfStock
              ? 'bg-slate-200 text-slate-400 cursor-not-allowed'
              : 'bg-amber-500 hover:bg-amber-400 text-slate-950 active:scale-95'
          }`}
        >
          {added ? (
            <>
              <Check className="w-4 h-4" />
              <span>Added</span>
            </>
          ) : (
            <>
              <ShoppingCart className="w-4 h-4" />
              <span>{isOutOfStock ? 'Sold Out' : 'Add'}</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
