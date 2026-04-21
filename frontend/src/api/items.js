import request from './index'

export const getItemList = (params) => request.get('/items/', { params })
export const getItemDetail = (id) => request.get(`/items/${id}`)
export const createItem = (formData) => request.post('/items/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const updateItem = (id, formData) => request.put(`/items/${id}`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
export const deleteItem = (id) => request.delete(`/items/${id}`)
export const getMyItems = (params) => request.get('/items/my', { params })
