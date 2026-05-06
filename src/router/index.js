import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import VideoView from '../views/VideoView.vue'
import AudioView from '../views/AudioView.vue'
import ImageView from '../views/ImageView.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/video', name: 'Video', component: VideoView },
  { path: '/audio', name: 'Audio', component: AudioView },
  { path: '/image', name: 'Image', component: ImageView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
