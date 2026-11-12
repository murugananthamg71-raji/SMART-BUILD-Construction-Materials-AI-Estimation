import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Building2, Lock, Mail, Eye, EyeOff, Loader2, AlertCircle, Store, UserCheck } from 'lucide-react';

export default function LoginPage() {
  const [role, setRole] = useState('customer');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [loading, setLoading] = useState(false);

  const { user, isAuthenticated, login, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/';

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const r = searchParams.get('role');
    if (r === 'supplier' || r === 'customer') {
      setRole(r);
    }
    if (searchParams.get('registered') === '1') {
      if (r === 'supplier') {
        setSuccessMsg('✅ Supplier registration successful! Please sign in with your credentials below.');
      } else {
        setSuccessMsg('✅ Registration successful! Please sign in to continue.');
      }
    }
  }, [location.search]);

  useEffect(() => {
    if (isAuthenticated && user) {
      if (user.role === 'supplier') {
        navigate('/supplier/dashboard', { replace: true });
      } else if (user.role === 'admin') {
        navigate('/admin/dashboard', { replace: true });
      } else if (user.role === 'delivery_partner') {
        navigate('/delivery/dashboard', { replace: true });
      } else {
        navigate('/customer/dashboard', { replace: true });
      }
    }
  }, [isAuthenticated, user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const loggedUser = await login(email, password);

      // Strict role check: If user chose Material Supplier tab, prevent going to customer dashboard
      if (role === 'supplier') {
        if (loggedUser.role !== 'supplier') {
          logout();
          setError('This email is registered as a Customer account. To access the Material Supplier portal, please login with a Supplier account or register as a Material Supplier below.');
          return;
        }
        navigate('/supplier/dashboard', { replace: true });
        return;
      }

      // If user chose Customer tab, but account is a Supplier, send directly to supplier dashboard
      if (role === 'customer') {
        if (loggedUser.role === 'supplier') {
          navigate('/supplier/dashboard', { replace: true });
          return;
        }
        navigate('/customer/dashboard', { replace: true });
        return;
      }

      const roleRedirects = {
        customer: '/customer/dashboard',
        supplier: '/supplier/dashboard',
        admin: '/admin/dashboard',
        delivery_partner: '/delivery/dashboard',
      };
      navigate(roleRedirects[loggedUser.role] || '/customer/dashboard', { replace: true });
    } catch (err) {
      let msg = 'Invalid email or password.';
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        msg = detail;
      } else if (Array.isArray(detail)) {
        msg = detail.map((d) => d.msg || `${d.loc?.slice(-1)[0]}: invalid input`).join(', ');
      } else if (err.message) {
        msg = err.message;
      }
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <div className="flex justify-center mb-3">
          <Link to="/home" className="inline-block transition hover:opacity-90">
            <img 
              src="/images/smart-build-logo.png" 
              alt="SMART BUILD - Construction Materials AI" 
              className="h-20 sm:h-24 w-auto object-contain mx-auto drop-shadow-sm"
            />
          </Link>
        </div>
        <h2 className="text-center text-2xl font-extrabold text-slate-900 tracking-tight">
          {role === 'supplier' ? 'Supplier Portal Login' : 'Sign in to your account'}
        </h2>
        <p className="mt-2 text-center text-sm text-slate-600">
          Or{' '}
          <Link 
            to={role === 'supplier' ? '/register?role=supplier' : '/register?role=customer'} 
            className="font-semibold text-amber-600 hover:text-amber-500"
          >
            {role === 'supplier' ? 'register as a new material supplier' : 'register for a new account'}
          </Link>
        </p>

        {/* Role Switcher Tabs */}
        <div className="mt-6 bg-slate-200/80 p-1 rounded-xl flex space-x-1 shadow-inner">
          <button
            type="button"
            onClick={() => { setRole('customer'); setError(''); }}
            className={`flex-1 py-2 text-xs sm:text-sm font-bold rounded-lg transition flex items-center justify-center space-x-1.5 ${
              role === 'customer'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <UserCheck className="w-4 h-4 text-amber-600" />
            <span>Customer / Builder</span>
          </button>
          <button
            type="button"
            onClick={() => { setRole('supplier'); setError(''); }}
            className={`flex-1 py-2 text-xs sm:text-sm font-bold rounded-lg transition flex items-center justify-center space-x-1.5 ${
              role === 'supplier'
                ? 'bg-amber-500 text-slate-950 shadow-sm font-black'
                : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            <Store className="w-4 h-4 text-slate-950" />
            <span>Material Supplier</span>
          </button>
        </div>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 shadow-xl rounded-2xl sm:px-10 border border-slate-200">
          <div className="mb-5 pb-3 border-b border-slate-100 flex items-center justify-between">
            <div>
              <span className="text-[11px] font-bold uppercase tracking-wider text-amber-600">
                {role === 'supplier' ? 'Vendor Access' : 'Buyer Access'}
              </span>
              <h3 className="text-base font-bold text-slate-900">
                {role === 'supplier' ? 'Material Supplier Sign In' : 'Customer Account Sign In'}
              </h3>
            </div>
            <span className={`px-2 py-0.5 text-[10px] font-black rounded-md uppercase tracking-wider ${
              role === 'supplier' ? 'bg-amber-100 text-amber-900 border border-amber-300' : 'bg-slate-100 text-slate-700'
            }`}>
              {role === 'supplier' ? 'Supplier' : 'Customer'}
            </span>
          </div>

          {error && (
            <div className="mb-5 p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-sm flex items-start space-x-2.5">
              <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          {successMsg && !error && (
            <div className="mb-5 p-3.5 rounded-xl bg-green-50 border border-green-200 text-green-800 text-sm flex items-start space-x-2.5">
              <span className="font-semibold">{successMsg}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-slate-700">
                {role === 'supplier' ? 'Supplier Business Email' : 'Email Address'}
              </label>
              <div className="mt-1 relative rounded-xl shadow-xs">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Mail className="w-5 h-5" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-slate-300 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 text-sm"
                  placeholder={role === 'supplier' ? 'supplier@smartbuild.com' : 'name@example.com'}
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700">Password</label>
              <div className="mt-1 relative rounded-xl shadow-xs">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-5 h-5" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-300 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500 text-sm"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-400 hover:text-slate-600"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center py-2.5 px-4 border border-transparent rounded-xl shadow-md text-sm font-bold text-slate-950 bg-amber-500 hover:bg-amber-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500 transition disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                  Signing In...
                </>
              ) : (
                role === 'supplier' ? 'Sign In as Material Supplier' : 'Sign In as Customer'
              )}
            </button>
          </form>

          {role === 'supplier' && (
            <div className="mt-4 pt-3 border-t border-dashed border-slate-200">
              <button
                type="button"
                onClick={() => {
                  setEmail('supplier@smartbuild.com');
                  setPassword('Demo1234!');
                  setError('');
                }}
                className="w-full py-1.5 px-3 bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded-lg text-xs font-semibold text-amber-900 flex items-center justify-center space-x-1.5 transition"
              >
                <Store className="w-3.5 h-3.5 text-amber-600" />
                <span>Fill Demo Supplier Credentials (supplier@smartbuild.com)</span>
              </button>
            </div>
          )}

          <div className="mt-5 pt-4 border-t border-slate-100 text-center text-xs text-slate-500">
            {role === 'supplier' ? (
              <p>
                Want to sell materials on SMART BUILD?{' '}
                <Link to="/register?role=supplier" className="font-bold text-amber-600 hover:underline">
                  Register as Supplier
                </Link>
              </p>
            ) : (
              <p>
                Are you a construction materials supplier?{' '}
                <button 
                  type="button" 
                  onClick={() => setRole('supplier')} 
                  className="font-bold text-amber-600 hover:underline inline-block"
                >
                  Switch to Supplier Login
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
