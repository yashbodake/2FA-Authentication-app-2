import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/register', component: () => import('./components/Register.vue') },
  { path: '/login', component: () => import('./components/Login.vue') },
  { path: '/', component: () => import('./components/Dashboard.vue'), meta: { requiresAuth: true } },
  { path: '/enable-2fa', component: () => import('./components/Enable2FA.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('token')

  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
