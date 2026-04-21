import request from './index'

export const getFavorites = () => request.get('/favorite/')
export const addFavorite = (itemId) => request.post(`/favorite/${itemId}`)
export const removeFavorite = (itemId) => request.delete(`/favorite/${itemId}`)
export const checkFavorite = (itemId) => request.get(`/favorite/check/${itemId}`)
