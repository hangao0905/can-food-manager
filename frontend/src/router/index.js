import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/brands' },
  { path: '/brands', component: () => import('../views/Brands.vue') },
  { path: '/flavors', component: () => import('../views/Flavors.vue') },
  { path: '/can-foods', component: () => import('../views/CanFoods.vue') },
  { path: '/query', component: () => import('../views/Query.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
