import { createRouter, createWebHistory } from 'vue-router'
import UVsearch from '../components/UVsearch.vue'//change here (UVchart  or  UVsearch)
import Home from '../components/Home.vue'
import Skinsearch from '@/components/Skinsearch.vue'
import UVinformation from '@/components/UVinformation.vue'

const routes = [
  {
    path: '/',
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
  },
  {
    path: '/UVinformation',
    name: 'UVinformation',
    component: UVinformation
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router