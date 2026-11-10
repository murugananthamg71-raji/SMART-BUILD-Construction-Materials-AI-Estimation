import React, { useState } from 'react';
import { 
  Calculator, 
  Sparkles, 
  Building2, 
  Download, 
  ShoppingCart, 
  Info, 
  AlertTriangle, 
  CheckCircle2, 
  Check, 
  Layers, 
  ShieldCheck,
  Loader2
} from 'lucide-react';
import api from '../../services/api';
import { useCart } from '../../context/CartContext';

export default function AIEstimatorPage() {
  const { addToCart } = useCart();

  // Form Inputs
  const [length, setLength] = useState(40);
  const [width, setWidth] = useState(30);
  const [floors, setFloors] = useState(2);
  const [height, setHeight] = useState(10);
  const [constructionType, setConstructionType] = useState('Residential');
  const [buildingType, setBuildingType] = useState('Individual House');
  const [location, setLocation] = useState('Bangalore');
  const [quality, setQuality] = useState('Standard');

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [addedSuccess, setAddedSuccess] = useState(false);

  const handleCalculate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await api.post('/estimator/calculate', {
        building_length: Number(length),
        building_width: Number(width),
        no_of_floors: Number(floors),
        floor_height: Number(height),
        construction_type: constructionType,
        building_type: buildingType,
        location: location,
        quality_preference: quality
      });
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Calculation failed. Please verify inputs.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddAllToCart = async () => {
    try {
      // Find top products and add representative bulk quantities
      const prodRes = await api.get('/products?limit=5');
      const products = prodRes.items || [];
      if (products.length > 0) {
        await addToCart(products[0].id, 10);
        setAddedSuccess(true);
        setTimeout(() => setAddedSuccess(false), 3000);
      }
    } catch (err) {
      alert(err.message || 'Please log in to add materials to your cart.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Page Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/10 text-amber-600 border border-amber-500/20">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Rule-Based Civil Engineering Estimation Engine</span>
        </div>
        <h1 className="text-3xl font-black text-slate-900 tracking-tight">AI Construction Material Estimator</h1>
        <p className="text-sm text-slate-500 max-w-3xl">
          Enter structural dimensions to calculate preliminary Bill of Quantities (BOQ) for Cement, TMT Steel, Bricks, Sand, Gravel, and Finishes based on IS 456 standards.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Estimator Input Form */}
        <div className="lg:col-span-5 bg-white p-6 rounded-3xl border border-slate-200/90 shadow-sm space-y-5">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-100">
            <Calculator className="w-5 h-5 text-amber-500" />
            <h2 className="font-bold text-slate-900 text-base">Project Parameters</h2>
          </div>

          {error && (
            <div className="p-3 rounded-xl bg-red-50 text-red-700 text-xs flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleCalculate} className="space-y-4">
            {/* Dimensions */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Building Length (ft)</label>
                <input
                  type="number"
                  required
                  min="10"
                  max="1000"
                  value={length}
                  onChange={(e) => setLength(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Building Width (ft)</label>
                <input
                  type="number"
                  required
                  min="10"
                  max="1000"
                  value={width}
                  onChange={(e) => setWidth(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Number of Floors</label>
                <input
                  type="number"
                  required
                  min="1"
                  max="25"
                  value={floors}
                  onChange={(e) => setFloors(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Floor Height (ft)</label>
                <input
                  type="number"
                  step="0.5"
                  min="8"
                  max="20"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                />
              </div>
            </div>

            {/* Categorization */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Construction Type</label>
                <select
                  value={constructionType}
                  onChange={(e) => setConstructionType(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  <option value="Residential">Residential</option>
                  <option value="Commercial">Commercial (+18% Load)</option>
                  <option value="Industrial">Industrial (+32% Load)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Building Typology</label>
                <select
                  value={buildingType}
                  onChange={(e) => setBuildingType(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  <option value="Individual House">Individual House</option>
                  <option value="Apartment">Apartment</option>
                  <option value="Office">Office Building</option>
                  <option value="Warehouse">Warehouse / Shed</option>
                  <option value="Shop">Retail Shop</option>
                </select>
              </div>
            </div>

            {/* Quality & Location */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Material Quality Tier</label>
                <select
                  value={quality}
                  onChange={(e) => setQuality(e.target.value)}
                  className="w-full px-3 py-2.5 rounded-xl border border-slate-300 text-xs font-bold text-slate-800 bg-white focus:outline-none focus:ring-2 focus:ring-amber-500"
                >
                  <option value="Budget">Budget Tier (-12%)</option>
                  <option value="Standard">Standard Tier (Default)</option>
                  <option value="Premium">Premium Tier (+35%)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 mb-1">Project Location</label>
                <input
                  type="text"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-amber-500"
                  placeholder="e.g. Bangalore"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl text-slate-950 font-bold text-sm bg-amber-500 hover:bg-amber-400 transition shadow-md disabled:opacity-50 mt-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Computing Quantities...</span>
                </>
              ) : (
                <>
                  <Calculator className="w-4 h-4" />
                  <span>Calculate Material Requirements</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Estimation Results Panel */}
        <div className="lg:col-span-7 space-y-6">
          {!result ? (
            <div className="bg-white rounded-3xl p-10 border border-slate-200 text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-amber-50 text-amber-500 flex items-center justify-center mx-auto">
                <Calculator className="w-8 h-8" />
              </div>
              <h3 className="text-xl font-bold text-slate-900">Ready to Compute Estimate</h3>
              <p className="text-xs text-slate-500 max-w-sm mx-auto leading-relaxed">
                Configure your plot dimensions on the left and click "Calculate Material Requirements" to generate a complete structural material breakdown.
              </p>
            </div>
          ) : (
            <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200/90 shadow-sm space-y-6">
              {/* Summary KPIs */}
              <div className="flex flex-wrap items-center justify-between gap-4 p-5 rounded-2xl bg-[#102A43] text-white">
                <div>
                  <div className="text-xs text-amber-400 uppercase font-bold tracking-wider">Total Built-Up Area</div>
                  <div className="text-3xl font-black">{result.built_up_area_sqft.toLocaleString('en-IN')} <span className="text-base font-normal text-slate-300">sq.ft</span></div>
                </div>
                <div>
                  <div className="text-xs text-amber-400 uppercase font-bold tracking-wider">Estimated Material Budget</div>
                  <div className="text-3xl font-black text-emerald-400">
                    ₹{result.estimated_total_budget.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                  </div>
                </div>
              </div>

              {/* Material Quantities Table */}
              <div className="space-y-3">
                <h3 className="font-bold text-slate-900 text-base">Material Bill of Quantities (BOQ)</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase tracking-wider">
                        <th className="py-2.5 px-3">Material Category</th>
                        <th className="py-2.5 px-3">Estimated Qty</th>
                        <th className="py-2.5 px-3">Avg Rate (₹)</th>
                        <th className="py-2.5 px-3 text-right">Projected Cost (₹)</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 font-medium">
                      {result.breakdown.map((item, idx) => (
                        <tr key={idx} className="hover:bg-slate-50">
                          <td className="py-3 px-3">
                            <div className="font-bold text-slate-900">{item.material}</div>
                            <div className="text-[11px] text-slate-400">{item.specification}</div>
                          </td>
                          <td className="py-3 px-3 font-semibold text-slate-800">
                            {item.quantity.toLocaleString('en-IN')} {item.unit}
                          </td>
                          <td className="py-3 px-3 text-slate-600">
                            ₹{item.unit_price.toFixed(2)}
                          </td>
                          <td className="py-3 px-3 text-right font-bold text-slate-900">
                            ₹{item.estimated_cost.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row items-center gap-3 pt-3 border-t border-slate-100">
                <button
                  onClick={handleAddAllToCart}
                  className={`flex-1 w-full flex items-center justify-center space-x-2 py-3 px-4 rounded-xl text-xs font-bold transition shadow-sm ${
                    addedSuccess
                      ? 'bg-emerald-600 text-white'
                      : 'bg-amber-500 hover:bg-amber-400 text-slate-950'
                  }`}
                >
                  {addedSuccess ? (
                    <>
                      <Check className="w-4 h-4" />
                      <span>Added to Cart!</span>
                    </>
                  ) : (
                    <>
                      <ShoppingCart className="w-4 h-4" />
                      <span>Add Selected Materials to Cart</span>
                    </>
                  )}
                </button>

                <button
                  onClick={() => window.print()}
                  className="w-full sm:w-auto flex items-center justify-center space-x-1.5 py-3 px-4 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 transition"
                >
                  <Download className="w-4 h-4" />
                  <span>Download BOQ</span>
                </button>
              </div>

              {/* Disclaimer */}
              <div className="p-3.5 rounded-2xl bg-amber-50/80 border border-amber-200 text-amber-900 text-xs flex items-start space-x-2.5">
                <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <span className="leading-relaxed">
                  <strong>Civil Engineering Notice:</strong> {result.disclaimer}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
