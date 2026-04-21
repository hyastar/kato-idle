import request from './index'

export const getProfile = () => request.get('/user/profile')
export const updateProfile = (data) => request.put('/user/profile', data)
export const uploadAvatar = (formData) => request.post('/user/avatar', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
})
