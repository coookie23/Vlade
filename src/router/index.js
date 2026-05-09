import { createRouter, createWebHistory } from 'vue-router'

// 路由懒加载：用户进入哪个页面，才下载哪个页面的代码，减轻首屏压力。
const Home = () => import('../views/Home.vue')
const VideoView = () => import('../views/VideoView.vue')
const AudioView = () => import('../views/AudioView.vue')
const ImageView = () => import('../views/ImageView.vue')
const AuthView = () => import('../views/AuthView.vue')

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/video', name: 'Video', component: VideoView },
  { path: '/audio', name: 'Audio', component: AudioView },
  { path: '/image', name: 'Image', component: ImageView },
  { path: '/auth', name: 'Auth', component: AuthView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
