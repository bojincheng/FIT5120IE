import { createRouter, createWebHistory } from 'vue-router'
import UVSearch from '../components/UVSearch.vue'
import Weather from '../components/Weather.vue'

const routes = [
  {
    path: '/UVSearch',
    name: 'UVSearch',
    component: UVSearch
  },
  {
    path: '/Weather',
    name: 'Weather',
    component: Weather
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router