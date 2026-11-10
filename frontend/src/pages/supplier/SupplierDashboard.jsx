import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import { 
  Building2, 
  Package, 
  AlertTriangle, 
  DollarSign, 
  Plus, 
  Check, 
  RotateCw, 
  Layers, 
  Loader2, 
  TrendingUp,
  X,
  Truck
} from 'lucide-react';

export default function SupplierDashboard() {
  const { user } = useAuth();
  const [metrics, setMetrics] = useState(null);
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);

  // Add Product Modal
  const [modalOpen, setModalOpen] = useState(false);
  const [newProdName, setNewProdName] = useState('');
  const [newProdBrand, setNewProdBrand] = useState('');
  const [newProdCategory, setNewProdCategory] = useState('');
  const [newProdPrice, setNewProdPrice] = useState('');
  const [newProdUnit, setNewProdUnit] = useState('bag');
  const [newProdStock, setNewProdStock] = useState('100');
  const [newProdDesc, setNewProdDesc] = useState('');
  const [newProdImg, setNewProdImg] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Quick inline stock edit state
  const [editingStockId, setEditingStockId] = useState(null);
  const [tempStockValue, setTempStockValue] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const [m, p, o, c] = await Promise.all([
        api.get('/supplier/dashboard'),
        api.get('/products?limit=50'),
        api.get('/orders'),
        api.get('/categories')
      ]);
      setMetrics(m);
      setProducts(p.items || []);
      setOrders(o || []);
      setCategories(c || []);
      if (c && c.length > 0) setNewProdCategory(c[0].id);
    } catch (err) {
      console.error('Failed to load supplier dashboard:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateProduct = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post('/products', {
        name: newProdName,
        brand: newProdBrand,
        category_id: Number(newProdCategory),
        price: Number(newProdPrice),
        unit: newProdUnit,
        initial_stock: Number(newProdStock),
        description: newProdDesc,
        image_url: newProdImg || 'https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500&auto=format&fit=crop&q=60'
      });
      setModalOpen(false);
      setNewProdName('');
      setNewProdPrice('');
      await loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create product.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUpdateStock = async (productId) => {
    try {
      await api.put(`/products/${productId}/stock`, {
        stock: Number(tempStockValue)
      });
      setEditingStockId(null);
      await loadData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to update stock.');
    }
  };

  const handleOrderStatusUpdate = async (orderId, newStatus) => {
    try {
      await api.put(`/orders/${orderId}/status`, {
        status: newStatus
      });
      await loadData();
    } catch (err) {
      alert('Failed to update order status');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Supplier Profile Header */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-xs font-bold text-emerald-600 uppercase tracking-wider">
            <span>Verified Supplier Yard</span>
            <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px]">
              {metrics?.approval_status || 'Approved'}
            </span>
          </div>
          <h1 className="text-2xl font-black text-slate-900 mt-1">
            {metrics?.company_name || user?.name}
          </h1>
          <p className="text-xs text-slate-500">
            Supplier ID: SUP-{user?.id} • Rating: {metrics?.rating || '4.9'} ★
          </p>
        </div>

        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center space-x-2 px-4 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs rounded-xl shadow-md transition"
        >
          <Plus className="w-4 h-4" />
          <span>Add New Material</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Total Revenue</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            ₹{Number(metrics?.total_revenue || 0).toLocaleString('en-IN')}
          </div>
          <div className="text-[11px] text-emerald-600 font-semibold">Verified Dispatches</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Incoming Orders</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {metrics?.total_orders || orders.length}
          </div>
          <div className="text-[11px] text-slate-500">Purchases to fulfill</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Active Materials</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {metrics?.active_products || products.length}
          </div>
          <div className="text-[11px] text-slate-500">Listed in catalog</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-red-500 uppercase">Low Stock Alerts</div>
          <div className="text-2xl sm:text-3xl font-black text-red-500">
            {metrics?.low_stock_products || 0}
          </div>
          <div className="text-[11px] text-slate-500">&lt; Threshold</div>
        </div>
      </div>

      {/* Material Inventory Management Table */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <Layers className="w-5 h-5 text-amber-500" />
            <h2 className="font-bold text-slate-900 text-base">Material Inventory & Pricing</h2>
          </div>
          <span className="text-xs text-slate-400">{products.length} products total</span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase tracking-wider">
                <th className="py-2.5 px-3">Material Product</th>
                <th className="py-2.5 px-3">Category</th>
                <th className="py-2.5 px-3">Unit Price (₹)</th>
                <th className="py-2.5 px-3">Live Stock</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {products.map((p) => (
                <tr key={p.id} className="hover:bg-slate-50">
                  <td className="py-3 px-3">
                    <div className="font-bold text-slate-900">{p.name}</div>
                    <div className="text-[11px] text-slate-400">Brand: {p.brand || 'Standard'}</div>
                  </td>
                  <td className="py-3 px-3 text-slate-600">{p.category?.name || 'Material'}</td>
                  <td className="py-3 px-3 font-bold text-slate-900">
                    ₹{Number(p.price).toLocaleString('en-IN')} / {p.unit}
                  </td>
                  <td className="py-3 px-3">
                    {editingStockId === p.id ? (
                      <div className="flex items-center space-x-1.5">
                        <input
                          type="number"
                          value={tempStockValue}
                          onChange={(e) => setTempStockValue(e.target.value)}
                          className="w-16 px-2 py-1 border border-amber-500 rounded text-xs font-bold"
                        />
                        <button
                          onClick={() => handleUpdateStock(p.id)}
                          className="p-1 bg-emerald-600 text-white rounded hover:bg-emerald-700"
                        >
                          <Check className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => setEditingStockId(null)}
                          className="p-1 bg-slate-200 text-slate-600 rounded"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <span className={`font-bold ${p.inventory?.stock < 20 ? 'text-red-600' : 'text-slate-900'}`}>
                          {p.inventory?.stock || 0} {p.unit}
                        </span>
                        <button
                          onClick={() => { setEditingStockId(p.id); setTempStockValue(String(p.inventory?.stock || 0)); }}
                          className="text-[10px] text-blue-600 hover:underline"
                        >
                          Edit
                        </button>
                      </div>
                    )}
                  </td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 text-[10px] font-bold rounded-md bg-emerald-100 text-emerald-800 uppercase">
                      Approved
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <span className="text-slate-400 text-[11px]">Active</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Incoming Orders to Fulfill */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <Truck className="w-5 h-5 text-amber-500" />
            <h2 className="font-bold text-slate-900 text-base">Incoming Material Purchase Orders</h2>
          </div>
          <span className="text-xs text-slate-400">{orders.length} orders total</span>
        </div>

        <div className="divide-y divide-slate-100">
          {orders.map((o) => (
            <div key={o.id} className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-mono font-bold text-slate-900 text-sm">{o.order_number}</span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded uppercase bg-amber-50 text-amber-800">
                    {o.status}
                  </span>
                </div>
                <div className="text-slate-500 mt-1">
                  Buyer: {o.customer_name} • Total: ₹{Number(o.net_amount).toLocaleString('en-IN')}
                </div>
              </div>

              {/* Order Status Update Controls */}
              <div className="flex items-center space-x-2">
                <span className="text-slate-400">Update Status:</span>
                <select
                  value={o.status}
                  onChange={(e) => handleOrderStatusUpdate(o.id, e.target.value)}
                  className="px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white font-bold text-slate-800 text-xs focus:ring-2 focus:ring-amber-500"
                >
                  <option value="confirmed">Confirmed</option>
                  <option value="processing">Processing (Packing)</option>
                  <option value="ready_for_dispatch">Ready for Dispatch</option>
                  <option value="shipped">Dispatched (Shipped)</option>
                  <option value="delivered">Delivered</option>
                </select>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Add Product Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 shadow-2xl space-y-4 border border-slate-200">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-slate-900 text-base">Add New Material Product</h3>
              <button onClick={() => setModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleCreateProduct} className="space-y-3 text-xs">
              <div>
                <label className="block font-bold text-slate-700 mb-1">Product Name</label>
                <input
                  type="text"
                  required
                  value={newProdName}
                  onChange={(e) => setNewProdName(e.target.value)}
                  placeholder="e.g. UltraTech Super 53 Grade OPC"
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Brand Name</label>
                  <input
                    type="text"
                    value={newProdBrand}
                    onChange={(e) => setNewProdBrand(e.target.value)}
                    placeholder="e.g. UltraTech"
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-amber-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Category</label>
                  <select
                    value={newProdCategory}
                    onChange={(e) => setNewProdCategory(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white focus:ring-2 focus:ring-amber-500"
                  >
                    {categories.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block font-bold text-slate-700 mb-1">Unit Price (₹)</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={newProdPrice}
                    onChange={(e) => setNewProdPrice(e.target.value)}
                    placeholder="390"
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-amber-500"
                  />
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Unit</label>
                  <select
                    value={newProdUnit}
                    onChange={(e) => setNewProdUnit(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs bg-white focus:ring-2 focus:ring-amber-500"
                  >
                    <option value="bag">bag</option>
                    <option value="kg">kg</option>
                    <option value="ton">ton</option>
                    <option value="piece">piece</option>
                    <option value="sqft">sqft</option>
                    <option value="liter">liter</option>
                  </select>
                </div>

                <div>
                  <label className="block font-bold text-slate-700 mb-1">Initial Stock</label>
                  <input
                    type="number"
                    required
                    value={newProdStock}
                    onChange={(e) => setNewProdStock(e.target.value)}
                    className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-amber-500"
                  />
                </div>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Description / Civil Specs</label>
                <textarea
                  rows={2}
                  value={newProdDesc}
                  onChange={(e) => setNewProdDesc(e.target.value)}
                  placeholder="Specification details, BIS standard conformity..."
                  className="w-full px-3 py-2 rounded-xl border border-slate-300 text-xs focus:ring-2 focus:ring-amber-500"
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full py-2.5 px-4 rounded-xl text-slate-950 font-bold bg-amber-500 hover:bg-amber-400 shadow-md transition disabled:opacity-50"
              >
                {submitting ? 'Submitting...' : 'Save & Publish Product'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
