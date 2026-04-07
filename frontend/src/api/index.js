import axios from 'axios'

const api = axios.create({
  baseURL: '/',
  timeout: 10000,
})

export const brandApi = {
  list: () => api.get('/brands/'),
  get: (id) => api.get(`/brands/${id}`),
  create: (data) => api.post('/brands/', data),
  update: (id, data) => api.put(`/brands/${id}`, data),
  delete: (id) => api.delete(`/brands/${id}`),
}

export const flavorApi = {
  list: (params) => api.get('/flavors/', { params }),
  get: (id) => api.get(`/flavors/${id}`),
  create: (data) => api.post('/flavors/', data),
  update: (id, data) => api.put(`/flavors/${id}`, data),
  delete: (id) => api.delete(`/flavors/${id}`),
}

export const canFoodApi = {
  list: (params) => api.get('/can-foods/', { params }),
  get: (id) => api.get(`/can-foods/${id}`),
  create: (data) => api.post('/can-foods/', data),
  update: (id, data) => api.put(`/can-foods/${id}`, data),
  delete: (id) => api.delete(`/can-foods/${id}`),
}

export default api
