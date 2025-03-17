import { createRouter, createWebHistory } from 'vue-router'
import UVsearch from '../components/UVchart.vue'//change here (UVchart  or  UVsearch)
import Home from '../components/Home.vue'
import Skinsearch from '@/components/Skinsearch.vue'
import UVinformation from '@/components/UVinformation.vue'
import UV_Final from '@/components/UV_Final.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/UV_Final',
    name: 'UV_Final',
    component: UV_Final
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