import { createRouter, createWebHistory } from 'vue-router'
import YearView from './views/YearView.vue'
import HomeView from './views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/:year',
      name: 'year',
      component: YearView,
      props: true
    }
  ]
})

export default router
