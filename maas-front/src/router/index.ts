import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      component: () => import('@/components/layout/AppLayout.vue'),
      children: [
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/pages/DashboardPage.vue'),
        },
        { path: 'models', name: 'models', component: () => import('@/pages/ModelMarketPage.vue') },
        {
          path: 'models/:id',
          name: 'model-detail',
          component: () => import('@/pages/ModelDetailPage.vue'),
        },
        {
          path: 'fine-tuning',
          name: 'fine-tuning',
          component: () => import('@/pages/FineTuningPage.vue'),
        },
        { path: 'data', name: 'data', component: () => import('@/pages/DataManagementPage.vue') },
        { path: 'api-keys', name: 'api-keys', component: () => import('@/pages/ApiKeyPage.vue') },
        {
          path: 'inference',
          name: 'inference',
          component: () => import('@/pages/InferencePage.vue'),
        },
        {
          path: 'analytics',
          name: 'analytics',
          component: () => import('@/pages/AnalyticsPage.vue'),
        },
      ],
    },
    { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login' }
  }
  if (to.name === 'login' && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
})

export default router
