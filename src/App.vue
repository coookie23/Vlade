<template>
  <div class="app-shell" :class="{ 'app-shell--ready': ready }">
    <canvas ref="particles" class="particle-canvas" />
    <div class="noise-overlay" />
    <div class="boot-layer" aria-hidden="true">
      <span />
      <span />
      <span />
    </div>
    <div class="bg-photo-layer">
      <img
        src="https://picsum.photos/seed/vlade-global-workspace/1920/1080"
        alt=""
        class="bg-photo"
      />
      <div class="bg-gradient-mesh" />
    </div>
    <NavBar />
    <router-view v-slot="{ Component }">
      <transition name="page-fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'

export default {
  components: { NavBar },
  data() {
    return { ready: false }
  },
  mounted() {
    this.initParticles()
    window.setTimeout(() => { this.ready = true }, 760)
  },
  methods: {
    initParticles() {
      const canvas = this.$refs.particles
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      let W, H, particles
      const COUNT = 60

      const resize = () => {
        W = canvas.width = window.innerWidth
        H = canvas.height = window.innerHeight
      }

      class Particle {
        constructor() {
          this.reset()
        }
        reset() {
          this.x = Math.random() * W
          this.y = Math.random() * H
          this.r = Math.random() * 1.5 + 0.5
          this.vx = (Math.random() - 0.5) * 0.3
          this.vy = (Math.random() - 0.5) * 0.3
          this.opacity = Math.random() * 0.5 + 0.15
          this.opacityDir = Math.random() > 0.5 ? 0.003 : -0.003
        }
        update() {
          this.x += this.vx
          this.y += this.vy
          this.opacity += this.opacityDir
          if (this.opacity > 0.5 || this.opacity < 0.08) this.opacityDir *= -1
          if (this.x < -20 || this.x > W + 20 || this.y < -20 || this.y > H + 20) this.reset()
        }
        draw() {
          ctx.beginPath()
          ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
          ctx.fillStyle = `rgba(212,135,94,${this.opacity})`
          ctx.fill()
        }
      }

      const drawLines = () => {
        for (let i = 0; i < particles.length; i++) {
          for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x
            const dy = particles[i].y - particles[j].y
            const dist = Math.sqrt(dx * dx + dy * dy)
            if (dist < 120) {
              ctx.beginPath()
              ctx.moveTo(particles[i].x, particles[i].y)
              ctx.lineTo(particles[j].x, particles[j].y)
              ctx.strokeStyle = `rgba(212,135,94,${0.06 * (1 - dist / 120)})`
              ctx.lineWidth = 0.5
              ctx.stroke()
            }
          }
        }
      }

      const animate = () => {
        ctx.clearRect(0, 0, W, H)
        for (const p of particles) { p.update(); p.draw() }
        drawLines()
        requestAnimationFrame(animate)
      }

      resize()
      particles = Array.from({ length: COUNT }, () => new Particle())
      animate()
      window.addEventListener('resize', () => { resize(); particles.forEach(p => p.reset()) })
    },
  },
}
</script>

<style>
:root {
  --bg: #1a1714;
  --bg-surface: rgba(36, 33, 29, 0.85);
  --bg-elevated: rgba(45, 42, 37, 0.9);
  --text-primary: #f0ebe4;
  --text-secondary: #a0988e;
  --text-tertiary: #6b6560;
  --accent: #d4875e;
  --accent-glow: rgba(212, 135, 94, 0.15);
  --border: rgba(54, 49, 43, 0.6);
  --border-light: rgba(54, 49, 43, 0.8);
  --glass-bg: rgba(36, 33, 29, 0.65);
  --glass-border: rgba(255, 255, 255, 0.06);
  --glass-highlight: rgba(255, 255, 255, 0.04);
  --radius-sm: 0.375rem;
  --radius-md: 0.625rem;
  --radius-lg: 1rem;
  --font-display: 'HarmonyOS Sans SC', 'MiSans', 'Alibaba PuHuiTi', 'PingFang SC', 'Microsoft YaHei UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'SFMono-Regular', Consolas, monospace;
  --font-body: 'Inter', 'HarmonyOS Sans SC', 'MiSans', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei UI', sans-serif;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html { background: var(--bg); }

body {
  font-family: var(--font-body);
  line-height: 1.6;
  color: var(--text-primary);
  background: var(--bg);
  font-feature-settings: 'kern';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-shell {
  min-height: 100vh;
  position: relative;
  padding-top: 4.25rem;
  overflow-x: hidden;
}

@media (max-width: 820px) {
  .app-shell {
    padding-top: 3.65rem;
    padding-bottom: calc(4.35rem + env(safe-area-inset-bottom));
  }
}

/* Boot layer */
.boot-layer {
  position: fixed;
  inset: 0;
  z-index: 9998;
  display: grid;
  place-items: center;
  pointer-events: none;
  opacity: 1;
  background:
    radial-gradient(circle at 32% 28%, rgba(212,135,94,0.16), transparent 24rem),
    radial-gradient(circle at 78% 64%, rgba(138,94,55,0.12), transparent 22rem),
    linear-gradient(145deg, rgba(18,15,12,0.96), rgba(7,7,6,0.98));
  transition:
    opacity 0.62s cubic-bezier(0.16, 1, 0.3, 1),
    visibility 0.62s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.62s cubic-bezier(0.16, 1, 0.3, 1);
}

.boot-layer::before {
  content: '';
  position: absolute;
  inset: 0;
  opacity: 0.28;
  background:
    linear-gradient(90deg, transparent 0 18%, rgba(212,135,94,0.12) 18.2%, transparent 18.7% 100%),
    repeating-linear-gradient(0deg, rgba(255,255,255,0.028) 0 1px, transparent 1px 34px);
  transform: translateX(-18%);
  animation: bootGrid 1.1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.boot-layer span {
  position: absolute;
  width: min(46vw, 36rem);
  height: 1px;
  border-radius: 999px;
  background: linear-gradient(90deg, transparent, rgba(212,135,94,0.58), transparent);
  transform-origin: center;
  animation: bootLine 1.05s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.boot-layer span:nth-child(1) {
  --boot-y: -2.4rem;
  transform: translateY(var(--boot-y)) scaleX(0);
}

.boot-layer span:nth-child(2) {
  --boot-y: 0rem;
  transform: translateY(var(--boot-y)) scaleX(0);
  animation-delay: 0.08s;
}

.boot-layer span:nth-child(3) {
  --boot-y: 2.4rem;
  transform: translateY(var(--boot-y)) scaleX(0);
  animation-delay: 0.16s;
}

.app-shell--ready .boot-layer {
  opacity: 0;
  visibility: hidden;
  transform: scale(1.015);
}

.app-shell--ready .particle-canvas {
  opacity: 0.72;
}

/* Page transition */
.page-fade-enter-active,
.page-fade-leave-active {
  transition:
    opacity 0.42s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.42s cubic-bezier(0.16, 1, 0.3, 1),
    filter 0.42s cubic-bezier(0.16, 1, 0.3, 1);
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(18px) scale(0.992);
  filter: brightness(0.82) blur(2px);
}
.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.996);
  filter: brightness(0.86) blur(1px);
}

/* Particle canvas */
.particle-canvas {
  position: fixed; inset: 0; z-index: 1; pointer-events: none;
  opacity: 0.95;
  transition: opacity 1.1s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Noise texture */
.noise-overlay {
  position: fixed; inset: 0; pointer-events: none; z-index: 9999;
  opacity: 0.025;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-repeat: repeat; background-size: 256px 256px;
}

/* Background photo + gradient mesh */
.bg-photo-layer { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.bg-photo-layer::after { content: ''; position: absolute; inset: 0; background: rgba(26, 23, 20, 0.78); }
.bg-photo { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.35) saturate(0.72); }
.bg-gradient-mesh {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at 30% 20%, rgba(212,135,94,0.08) 0%, transparent 60%),
    radial-gradient(ellipse at 70% 60%, rgba(212,135,94,0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(180,120,70,0.04) 0%, transparent 40%);
}

/* Glass base class */
.glass {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
}

/* Breathing glow animation */
@keyframes breathe {
  0%, 100% { box-shadow: 0 0 20px rgba(212,135,94,0.05), 0 0 60px rgba(212,135,94,0.02); }
  50% { box-shadow: 0 0 30px rgba(212,135,94,0.1), 0 0 80px rgba(212,135,94,0.04); }
}

/* Floating animation */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* Scan line */
@keyframes scan {
  0% { top: -100%; }
  100% { top: 200%; }
}

/* Flow light */
@keyframes flowLight {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

@keyframes bootGrid {
  0% {
    opacity: 0;
    transform: translateX(-18%);
  }
  45% {
    opacity: 0.3;
  }
  100% {
    opacity: 0.08;
    transform: translateX(0);
  }
}

@keyframes bootLine {
  0% {
    opacity: 0;
    transform: translateY(var(--boot-y, 0)) scaleX(0);
  }
  42% {
    opacity: 0.82;
  }
  100% {
    opacity: 0;
    transform: translateY(var(--boot-y, 0)) scaleX(1);
  }
}

/* Stagger reveal — triggered by .in class added via JS */
.stagger-reveal > * {
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
}
.stagger-reveal.in > * { opacity: 1; transform: translateY(0); }
.stagger-reveal.in > *:nth-child(1) { transition-delay: 0.05s; }
.stagger-reveal.in > *:nth-child(2) { transition-delay: 0.12s; }
.stagger-reveal.in > *:nth-child(3) { transition-delay: 0.19s; }
.stagger-reveal.in > *:nth-child(4) { transition-delay: 0.26s; }
.stagger-reveal.in > *:nth-child(5) { transition-delay: 0.33s; }
.stagger-reveal.in > *:nth-child(6) { transition-delay: 0.40s; }
</style>
