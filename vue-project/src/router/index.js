import { createRouter, createWebHistory } from 'vue-router'
import UVsearch from '../components/UVsearch.vue'
import Home from '../components/Home.vue'
import Skinsearch from '@/components/Skinsearch2.vue'

const routes = [
  {
    path: '/Home',
    name: 'Home',
    component: Home
  },
  {
    path: '/UVsearch',
    name: 'UVsearch',
    component: UVsearch
  },
  {
    path: '/Skinsearch',
    name: 'Skinsearch',
    component: Skinsearch
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router