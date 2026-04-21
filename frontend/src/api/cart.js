import request from './index'

export const getCart = () => request.get('/cart/')
export const addToCart = (itemId) => request.post(`/cart/${itemId}`)
export const removeFromCart = (itemId) => request.delete(`/cart/${itemId}`)
export const clearCart = () => request.delete('/cart/')
