import request from './index'

export const getCategoryList = () => request.get('/categories/')
