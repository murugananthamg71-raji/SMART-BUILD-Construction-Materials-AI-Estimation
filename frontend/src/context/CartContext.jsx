import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from './AuthContext';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [cart, setCart] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchCart = async () => {
    if (!isAuthenticated) {
      setCart(null);
      return;
    }
    try {
      setLoading(true);
      const data = await api.get('/cart');
      setCart(data);
    } catch (err) {
      console.error('Failed to fetch cart:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, [isAuthenticated]);

  const addToCart = async (productId, quantity = 1) => {
    if (!isAuthenticated) {
      throw new Error('Please login to add materials to your cart.');
    }
    const updated = await api.post('/cart/items', { product_id: productId, quantity });
    setCart(updated);
    return updated;
  };

  const updateQuantity = async (itemId, quantity) => {
    const updated = await api.put(`/cart/items/${itemId}`, { quantity });
    setCart(updated);
    return updated;
  };

  const removeItem = async (itemId) => {
    const updated = await api.delete(`/cart/items/${itemId}`);
    setCart(updated);
    return updated;
  };

  const clearCart = async () => {
    const updated = await api.delete('/cart');
    setCart(updated);
    return updated;
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        itemCount: cart?.item_count || 0,
        subtotal: cart?.subtotal || '0.00',
        taxAmount: cart?.tax_amount || '0.00',
        deliveryFee: cart?.delivery_fee || '0.00',
        grandTotal: cart?.grand_total || '0.00',
        loading,
        addToCart,
        updateQuantity,
        removeItem,
        clearCart,
        refreshCart: fetchCart
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
