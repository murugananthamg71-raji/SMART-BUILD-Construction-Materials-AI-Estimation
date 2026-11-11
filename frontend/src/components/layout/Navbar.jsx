import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import { 
  Building2, 
  ShoppingCart, 
  User as UserIcon, 
  LogOut, 
  Menu, 
  X, 
  Package, 
  LayoutDashboard,
  ShieldCheck,
  ChevronDown
} from 'lucide-react';

export default function Navbar() {
  const { user, isAuthenticated, logout, role } = useAuth();
  const { itemCount } = useCart();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
    setUserDropdownOpen(false);
  };

  const getDashboardLink = () => {
    switch (role) {
      case 'supplier': return '/supplier/dashboard';
      case 'admin': return '/admin/dashboard';
      case 'delivery_partner': return '/delivery/dashboard';
      default: return '/customer/dashboard';
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-[#102A43] text-white shadow-md border-b border-slate-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to={isAuthenticated ? getDashboardLink() : "/login"} className="flex items-center space-x-2.5">
          <div className="bg-amber-500 p-2 rounded-xl text-slate-950 font-bold shadow-md">
            <Building2 className="w-5 h-5 sm:w-6 sm:h-6" />
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-black tracking-tight text-white leading-tight">SMART BUILD</span>
            <span className="text-[10px] tracking-wider text-amber-400 font-bold uppercase hidden sm:inline">
              Materials & AI Estimation
            </span>
          </div>
        </Link>

        {/* Desktop Navigation Links */}
        <nav className="hidden md:flex items-center space-x-6 text-sm font-semibold text-slate-200">
          <Link to={isAuthenticated ? getDashboardLink() : "/login"} className="hover:text-amber-400 transition">
            {isAuthenticated ? "Dashboard" : "Home"}
          </Link>
          <Link to="/materials" className="hover:text-amber-400 transition">Materials</Link>
          <Link to="/about" className="hover:text-amber-400 transition">About</Link>
          <Link to="/contact" className="hover:text-amber-400 transition">Contact</Link>
        </nav>

        {/* Right Section: Cart & Auth */}
        <div className="flex items-center space-x-4">
          {/* Cart Icon */}
          <Link 
            to="/cart" 
            className="relative p-2 text-slate-200 hover:text-amber-400 transition rounded-lg hover:bg-slate-800"
            title="Shopping Cart"
          >
            <ShoppingCart className="w-5 h-5" />
            {itemCount > 0 && (
              <span className="absolute -top-1 -right-1 bg-amber-500 text-slate-950 text-[11px] font-black w-5 h-5 rounded-full flex items-center justify-center shadow-md animate-pulse">
                {itemCount}
              </span>
            )}
          </Link>

          {/* User Account / Auth Buttons */}
          {isAuthenticated ? (
            <div className="relative">
              <button
                onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                className="flex items-center space-x-2 p-1.5 rounded-xl hover:bg-slate-800 transition text-sm font-semibold text-white focus:outline-none"
              >
                <div className="w-8 h-8 rounded-lg bg-amber-500 text-slate-950 flex items-center justify-center font-bold uppercase shadow-xs">
                  {user.name.charAt(0)}
                </div>
                <div className="hidden lg:block text-left">
                  <div className="text-xs font-bold leading-tight truncate max-w-[120px]">{user.name}</div>
                  <div className="text-[10px] text-amber-400 uppercase tracking-wider">{user.role}</div>
                </div>
                <ChevronDown className="w-4 h-4 text-slate-400 hidden sm:block" />
              </button>

              {/* Dropdown Menu */}
              {userDropdownOpen && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-2xl py-2 border border-slate-200 text-slate-800 text-sm z-50 animate-in fade-in-50">
                  <div className="px-4 py-2.5 border-b border-slate-100">
                    <p className="font-bold text-slate-900 truncate">{user.name}</p>
                    <p className="text-xs text-slate-500 truncate">{user.email}</p>
                    <span className="inline-block mt-1 px-2 py-0.5 text-[10px] font-bold rounded-md uppercase tracking-wider bg-amber-100 text-amber-900">
                      {user.role}
                    </span>
                  </div>

                  <Link
                    to={getDashboardLink()}
                    onClick={() => setUserDropdownOpen(false)}
                    className="flex items-center space-x-2.5 px-4 py-2 hover:bg-slate-50 text-slate-700 font-medium"
                  >
                    <LayoutDashboard className="w-4 h-4 text-amber-600" />
                    <span>Dashboard</span>
                  </Link>

                  {role === 'customer' && (
                    <Link
                      to="/orders"
                      onClick={() => setUserDropdownOpen(false)}
                      className="flex items-center space-x-2.5 px-4 py-2 hover:bg-slate-50 text-slate-700 font-medium"
                    >
                      <Package className="w-4 h-4 text-blue-600" />
                      <span>Order History</span>
                    </Link>
                  )}

                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center space-x-2.5 px-4 py-2 hover:bg-red-50 text-red-600 font-medium border-t border-slate-100 mt-1"
                  >
                    <LogOut className="w-4 h-4" />
                    <span>Sign Out</span>
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="hidden sm:flex items-center space-x-2">
              <Link
                to="/login"
                className="px-3.5 py-1.5 text-xs font-bold text-slate-200 hover:text-white rounded-lg hover:bg-slate-800 transition"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="px-4 py-1.5 text-xs font-bold text-slate-950 bg-amber-500 hover:bg-amber-400 rounded-lg shadow-md transition"
              >
                Register
              </Link>
            </div>
          )}

          {/* Mobile Menu Toggle Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-slate-300 hover:text-white rounded-lg hover:bg-slate-800"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-slate-900 border-b border-slate-800 px-4 pt-2 pb-6 space-y-3">
          <Link 
            to={isAuthenticated ? getDashboardLink() : "/login"} 
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-semibold text-slate-200 hover:text-amber-400"
          >
            {isAuthenticated ? "My Dashboard" : "Home"}
          </Link>
          <Link 
            to="/materials" 
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-semibold text-slate-200 hover:text-amber-400"
          >
            Materials Catalog
          </Link>
          <Link 
            to="/about" 
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-semibold text-slate-200"
          >
            About Us
          </Link>
          <Link 
            to="/contact" 
            onClick={() => setMobileMenuOpen(false)}
            className="block py-2 text-sm font-semibold text-slate-200"
          >
            Support & Contact
          </Link>

          {!isAuthenticated && (
            <div className="pt-4 border-t border-slate-800 flex flex-col space-y-2">
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full text-center py-2 text-sm font-bold text-white bg-slate-800 rounded-xl"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full text-center py-2 text-sm font-bold text-slate-950 bg-amber-500 rounded-xl"
              >
                Register
              </Link>
            </div>
          )}
        </div>
      )}
    </header>
  );
}
