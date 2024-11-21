import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ClusterView from '../views/ClusterView.vue'
import DataUpload from '@/components/dataset-selection/DataUpload.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/data',
      name: 'data',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/DataView.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    },
    {
      path: '/label',
      name: 'label',
      component: ClusterView
    }, 
    {
      path: '/upload', 
      name: 'upload', 
      component: DataUpload
    }
  ]
})

export default router
