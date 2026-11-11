import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Layers, Calculator, ShoppingCart, User } from 'lucide-react';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';

export default function MobileNav() {
  const { itemCount } = useCart();
  const { isAuthenticated, role } = useAuth();

  const getAccountLink = () => {
    if (!isAuthenticated) return '/login';
    switch (role) {
      case 'supplier': return '/supplier/dashboard';
      case 'admin': return '/admin/dashboard';
      case 'delivery_partner': return '/delivery/dashboard';
      default: return '/customer/dashboard';
    }
  };

  return (
    <div className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white border-t border-slate-200 shadow-2xl py-2 px-4 flex items-center justify-around">
      <NavLink
        to="/home"
        className={({ isActive }) => `flex flex-col items-center text-[10px] font-bold ${isActive ? 'text-amber-600' : 'text-slate-500'}`}
      >
        <Home className="w-5 h-5 mb-0.5" />
        <span>Home</span>
      </NavLink>

      <NavLink
        to="/materials"
        className={({ isActive }) => `flex flex-col items-center text-[10px] font-bold ${isActive ? 'text-amber-600' : 'text-slate-500'}`}
      >
        <Layers className="w-5 h-5 mb-0.5" />
        <span>Materials</span>
      </NavLink>

      <NavLink
        to="/estimator"
        className={({ isActive }) => `flex flex-col items-center text-[10px] font-bold ${isActive ? 'text-amber-600' : 'text-slate-500'}`}
      >
        <div className="bg-amber-500 text-slate-950 p-1.5 rounded-full -mt-4 shadow-md border-2 border-white">
          <Calculator className="w-5 h-5" />
        </div>
        <span className="mt-0.5">Estimator</span>
      </NavLink>

      <NavLink
        to="/cart"
        className={({ isActive }) => `relative flex flex-col items-center text-[10px] font-bold ${isActive ? 'text-amber-600' : 'text-slate-500'}`}
      >
        <ShoppingCart className="w-5 h-5 mb-0.5" />
        {itemCount > 0 && (
          <span className="absolute -top-1 right-1 bg-amber-500 text-slate-950 text-[10px] font-black w-4 h-4 rounded-full flex items-center justify-center">
            {itemCount}
          </span>
        )}
        <span>Cart</span>
      </NavLink>

      <NavLink
        to={getAccountLink()}
        className={({ isActive }) => `flex flex-col items-center text-[10px] font-bold ${isActive ? 'text-amber-600' : 'text-slate-500'}`}
      >
        <User className="w-5 h-5 mb-0.5" />
        <span>{isAuthenticated ? 'Account' : 'Login'}</span>
      </NavLink>
    </div>
  );
}
