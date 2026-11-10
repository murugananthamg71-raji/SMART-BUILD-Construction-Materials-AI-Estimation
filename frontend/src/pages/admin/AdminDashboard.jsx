import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { 
  ShieldCheck, 
  Users, 
  Building2, 
  DollarSign, 
  Package, 
  AlertCircle, 
  CheckCircle2, 
  XCircle, 
  Layers, 
  Loader2, 
  Search,
  Truck
} from 'lucide-react';

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [suppliers, setSuppliers] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('suppliers');

  const loadData = async () => {
    setLoading(true);
    try {
      const [m, s, u] = await Promise.all([
        api.get('/admin/dashboard'),
        api.get('/admin/suppliers'),
        api.get('/admin/users')
      ]);
      setMetrics(m);
      setSuppliers(s || []);
      setUsers(u || []);
    } catch (err) {
      console.error('Failed to load admin data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleApproveSupplier = async (supplierId, newStatus) => {
    try {
      await api.put(`/admin/suppliers/${supplierId}/approve?status_choice=${newStatus}`);
      await loadData();
    } catch (err) {
      alert('Failed to update supplier approval.');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Admin Header */}
      <div className="bg-[#102A43] text-white p-6 rounded-3xl shadow-lg border border-slate-700 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="p-3 bg-amber-500 rounded-2xl text-slate-950 font-bold shadow-md">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <div>
            <div className="text-xs font-bold text-amber-400 uppercase tracking-wider">Super Administrator</div>
            <h1 className="text-2xl font-black">Platform Administration & Analytics</h1>
            <p className="text-xs text-slate-300">Overseeing marketplace operations, seller vetting, and transactions.</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="px-3 py-1 bg-emerald-500/20 text-emerald-300 font-bold text-xs rounded-full border border-emerald-500/30">
            System Healthy
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Gross Platform Revenue</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            ₹{Number(metrics?.total_revenue || 0).toLocaleString('en-IN')}
          </div>
          <div className="text-[11px] text-emerald-600 font-semibold">{metrics?.total_orders || 0} total transactions</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Registered Users</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {metrics?.total_users || 0}
          </div>
          <div className="text-[11px] text-slate-500">{metrics?.total_customers || 0} builders & contractors</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-slate-400 uppercase">Active Catalog Products</div>
          <div className="text-2xl sm:text-3xl font-black text-slate-900">
            {metrics?.total_products || 0}
          </div>
          <div className="text-[11px] text-slate-500">Across 9 material categories</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs space-y-1">
          <div className="text-xs font-bold text-amber-600 uppercase">Pending Vetting</div>
          <div className="text-2xl sm:text-3xl font-black text-amber-600">
            {metrics?.pending_suppliers || 0}
          </div>
          <div className="text-[11px] text-slate-500">Supplier applications</div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-slate-200 flex space-x-6">
        <button
          onClick={() => setActiveTab('suppliers')}
          className={`py-3 text-sm font-bold border-b-2 transition ${
            activeTab === 'suppliers' ? 'border-amber-500 text-slate-900' : 'border-transparent text-slate-400'
          }`}
        >
          Suppliers Vetting & Verification ({suppliers.length})
        </button>
        <button
          onClick={() => setActiveTab('users')}
          className={`py-3 text-sm font-bold border-b-2 transition ${
            activeTab === 'users' ? 'border-amber-500 text-slate-900' : 'border-transparent text-slate-400'
          }`}
        >
          Platform Users ({users.length})
        </button>
      </div>

      {/* Supplier Vetting Management */}
      {activeTab === 'suppliers' && (
        <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-4">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase tracking-wider">
                  <th className="py-2.5 px-3">Company Name</th>
                  <th className="py-2.5 px-3">Contact Person</th>
                  <th className="py-2.5 px-3">Location</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3 text-right">Approval Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {suppliers.map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50">
                    <td className="py-3 px-3">
                      <div className="font-bold text-slate-900">{s.company_name}</div>
                      <div className="text-[11px] text-slate-400">ID: SUP-{s.id}</div>
                    </td>
                    <td className="py-3 px-3">
                      <div className="text-slate-800">{s.contact_person}</div>
                      <div className="text-[11px] text-slate-400">{s.email}</div>
                    </td>
                    <td className="py-3 px-3 text-slate-600">
                      {s.city}, {s.state}
                    </td>
                    <td className="py-3 px-3">
                      <span className={`px-2.5 py-0.5 text-[10px] font-bold rounded-full uppercase ${
                        s.approval_status === 'approved'
                          ? 'bg-emerald-100 text-emerald-800'
                          : s.approval_status === 'rejected'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {s.approval_status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right space-x-2">
                      {s.approval_status !== 'approved' && (
                        <button
                          onClick={() => handleApproveSupplier(s.id, 'approved')}
                          className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg text-[11px] transition"
                        >
                          Approve
                        </button>
                      )}
                      {s.approval_status !== 'rejected' && (
                        <button
                          onClick={() => handleApproveSupplier(s.id, 'rejected')}
                          className="px-3 py-1 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg text-[11px] transition"
                        >
                          Reject
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Users Tab */}
      {activeTab === 'users' && (
        <div className="bg-white rounded-3xl border border-slate-200/90 shadow-sm p-6 space-y-4">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase tracking-wider">
                  <th className="py-2.5 px-3">Name</th>
                  <th className="py-2.5 px-3">Email</th>
                  <th className="py-2.5 px-3">Phone</th>
                  <th className="py-2.5 px-3">Role</th>
                  <th className="py-2.5 px-3">Active</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 font-medium">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-50">
                    <td className="py-3 px-3 font-bold text-slate-900">{u.name}</td>
                    <td className="py-3 px-3 text-slate-600">{u.email}</td>
                    <td className="py-3 px-3 text-slate-600">{u.phone || 'N/A'}</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-slate-100 text-slate-700">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 px-3">
                      <span className="text-emerald-600 font-bold">Active</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
