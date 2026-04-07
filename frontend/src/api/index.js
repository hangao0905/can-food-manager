import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 请求拦截器：附加 JWT token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截器：token 过期跳转登录
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // 清除登录状态
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      // 标记已处理，防止组件弹出错误提示
      error.config._handled = true
      // 用 setTimeout(0) 确保在 Promise 链之外执行 redirect
      setTimeout(() => {
        window.location.href = window.location.origin + '/login'
      }, 0)
    }
    return Promise.reject(error)
  }
)

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
  recalcAll: () => api.post('/can-foods/recalc-all'),
}

export const standardApi = {
  list: () => api.get('/standards/'),
  update: (id, data) => api.put(`/standards/${id}`, data),
  init: () => api.post('/standards/init'),
}

export const userApi = {
  list: () => api.get('/users/'),
  create: (username, password, role) => api.post('/users/', null, { params: { username, password, role } }),
  update: (id, data) => api.put(`/users/${id}`, data),
  delete: (id) => api.delete(`/users/${id}`),
}

export default api
