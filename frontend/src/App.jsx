import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { CartProvider } from './context/CartContext';

// Layout
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import MobileNav from './components/layout/MobileNav';

// Public & Customer Pages
import LandingPage from './pages/customer/LandingPage';
import ProductListingPage from './pages/customer/ProductListingPage';
import ProductDetailsPage from './pages/customer/ProductDetailsPage';
import AIEstimatorPage from './pages/customer/AIEstimatorPage';
import CartPage from './pages/customer/CartPage';
import CheckoutPage from './pages/customer/CheckoutPage';
import OrderConfirmationPage from './pages/customer/OrderConfirmationPage';
import OrderHistoryPage from './pages/customer/OrderHistoryPage';
import AboutPage from './pages/customer/AboutPage';
import ContactPage from './pages/customer/ContactPage';

// Auth Pages
import LoginPage from './pages/auth/LoginPage';
import RegisterPage from './pages/auth/RegisterPage';

// Role Dashboards
import CustomerDashboard from './pages/customer/CustomerDashboard';
import SupplierDashboard from './pages/supplier/SupplierDashboard';
import AdminDashboard from './pages/admin/AdminDashboard';
import DeliveryDashboard from './pages/delivery/DeliveryDashboard';

// Route Guard
import ProtectedRoute from './routes/ProtectedRoute';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <CartProvider>
          <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800 antialiased pb-16 md:pb-0">
            {/* Top Navigation */}
            <Navbar />

            {/* Main Content Area */}
            <main className="flex-1">
              <Routes>
                {/* Public Marketplace */}
                <Route path="/" element={<LandingPage />} />
                <Route path="/materials" element={<ProductListingPage />} />
                <Route path="/materials/:id" element={<ProductDetailsPage />} />
                <Route path="/estimator" element={<AIEstimatorPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/contact" element={<ContactPage />} />

                {/* Authentication */}
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {/* Customer Protected */}
                <Route
                  path="/checkout"
                  element={
                    <ProtectedRoute allowedRoles={['customer', 'admin']}>
                      <CheckoutPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/orders/:id"
                  element={
                    <ProtectedRoute>
                      <OrderConfirmationPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/orders"
                  element={
                    <ProtectedRoute allowedRoles={['customer', 'admin']}>
                      <OrderHistoryPage />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/customer/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['customer', 'admin']}>
                      <CustomerDashboard />
                    </ProtectedRoute>
                  }
                />

                {/* Supplier Portal */}
                <Route
                  path="/supplier/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['supplier', 'admin']}>
                      <SupplierDashboard />
                    </ProtectedRoute>
                  }
                />

                {/* Admin Portal */}
                <Route
                  path="/admin/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['admin']}>
                      <AdminDashboard />
                    </ProtectedRoute>
                  }
                />

                {/* Delivery Logistics */}
                <Route
                  path="/delivery/dashboard"
                  element={
                    <ProtectedRoute allowedRoles={['delivery_partner', 'admin']}>
                      <DeliveryDashboard />
                    </ProtectedRoute>
                  }
                />

                {/* Catch-all redirect */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>

            {/* Desktop & Mobile Footers */}
            <Footer />
            <MobileNav />
          </div>
        </CartProvider>
      </AuthProvider>
    </BrowserRouter>
  );
}
