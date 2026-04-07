import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    component: () => import('../views/Login.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    component: () => import('../views/Dashboard.vue'),
  },
  {
    path: '/brands',
    component: () => import('../views/Brands.vue'),
  },
  {
    path: '/flavors',
    component: () => import('../views/Flavors.vue'),
  },
  {
    path: '/can-foods',
    component: () => import('../views/CanFoods.vue'),
  },
  {
    path: '/query',
    component: () => import('../views/Query.vue'),
  },
  {
    path: '/standards',
    component: () => import('../views/Standards.vue'),
  },
  {
    path: '/compare',
    component: () => import('../views/Compare.vue'),
  },
  {
    path: '/users',
    component: () => import('../views/Users.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const publicPages = ['/login']
  const requiresAdmin = ['/users']
  const token = localStorage.getItem('token')

  if (!publicPages.includes(to.path) && !token) {
    next('/login')
    return
  }
  if (to.path === '/login' && token) {
    next('/brands')
    return
  }

  // admin 页面权限检查
  if (requiresAdmin.includes(to.path)) {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (user.role !== 'admin') {
      alert('需要管理员权限')
      next('/brands')
      return
    }
  }

  next()
})

export default router
