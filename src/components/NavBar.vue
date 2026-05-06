<template>
  <header class="navbar">
    <div class="nav-inner">
      <router-link to="/" class="nav-logo" aria-label="回到首页">
        <span class="logo-mark" />
        <span class="logo-text">Vlade</span>
      </router-link>

      <nav class="nav-links" aria-label="媒体类型">
        <router-link v-for="item in navItems" :key="item.path" :to="item.path" class="nav-link" active-class="nav-link--active">
          <span class="nav-link-icon"><Icon :icon="item.icon" width="18" /></span>
          <span class="nav-link-copy">
            <strong>{{ item.label }}</strong>
            <small>{{ item.tag }}</small>
          </span>
        </router-link>
      </nav>

      <router-link to="/video" class="nav-cta">
        <Icon icon="ph:upload-simple" width="15" />
        开始
      </router-link>
    </div>
  </header>
</template>

<script>
import { Icon } from '@iconify/vue'

export default {
  name: 'NavBar',
  components: { Icon },
  data() {
    return {
      navItems: [
        { path: '/video', label: '视频', tag: '补帧剪辑', icon: 'ph:video-camera' },
        { path: '/image', label: '图片', tag: '压缩转换', icon: 'ph:image' },
        { path: '/audio', label: '音频', tag: '提取剪切', icon: 'ph:music-notes' },
      ],
    }
  },
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  height: 4.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.065);
  background:
    linear-gradient(90deg, rgba(18, 15, 13, 0.86), rgba(10, 9, 8, 0.76)),
    rgba(10, 10, 10, 0.62);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.nav-inner {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0 1.25rem;
}

.nav-logo,
.nav-link,
.nav-cta {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
}

.nav-logo {
  gap: 0.5rem;
  min-width: 7rem;
}

.logo-mark {
  width: 0.7rem;
  height: 0.7rem;
  transform: rotate(45deg);
  background: var(--accent);
  box-shadow: 0 0 16px rgba(212, 135, 94, 0.5);
}

.logo-text {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-weight: 800;
}

.nav-links {
  display: flex;
  gap: 0.45rem;
  min-width: 0;
  padding: 0.22rem;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  background: rgba(0,0,0,0.16);
}

.nav-link {
  gap: 0.55rem;
  min-height: 3rem;
  min-width: 8.4rem;
  padding: 0 0.85rem;
  border: 1px solid transparent;
  border-radius: 12px;
  color: var(--text-tertiary);
  font-size: 0.78rem;
  transition:
    color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    border-color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    background 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    transform 0.24s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.nav-link-icon {
  width: 2rem;
  height: 2rem;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
  border-radius: 10px;
  color: var(--accent);
  background: rgba(212,135,94,0.08);
}

.nav-link-copy {
  display: grid;
  min-width: 0;
  line-height: 1.18;
}

.nav-link-copy strong {
  color: var(--text-primary);
  font-size: 0.86rem;
}

.nav-link-copy small {
  margin-top: 0.12rem;
  color: var(--text-tertiary);
  font-size: 0.66rem;
  white-space: nowrap;
}

.nav-link:hover {
  color: var(--text-primary);
  border-color: rgba(212,135,94,0.18);
  background: rgba(255, 255, 255, 0.045);
  transform: translateY(-1px);
}

.nav-link--active {
  color: var(--text-primary);
  border-color: rgba(212,135,94,0.42);
  background: linear-gradient(135deg, rgba(212,135,94,0.24), rgba(212,135,94,0.075)), rgba(22,17,13,0.84);
  box-shadow: inset 0 0 0 1px rgba(212,135,94,0.12), 0 12px 30px rgba(0,0,0,0.2);
}

.nav-link--active .nav-link-icon {
  color: var(--bg);
  background: var(--accent);
}

.nav-cta {
  gap: 0.35rem;
  min-height: 2.45rem;
  padding: 0 0.95rem;
  border-radius: 999px;
  color: var(--bg);
  background: var(--accent);
  font-size: 0.76rem;
  font-weight: 800;
  box-shadow: 0 12px 30px rgba(212, 135, 94, 0.2);
  transition:
    transform 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    box-shadow 0.24s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.nav-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 36px rgba(212, 135, 94, 0.28);
}

@media (max-width: 820px) {
  .navbar {
    height: 3.85rem;
  }

  .nav-inner {
    gap: 0.55rem;
    padding: 0 0.65rem;
  }

  .nav-logo {
    min-width: auto;
  }

  .logo-text {
    display: none;
  }

  .nav-links {
    flex: 1;
    overflow-x: auto;
    gap: 0.25rem;
    scrollbar-width: none;
  }

  .nav-links::-webkit-scrollbar { display: none; }

  .nav-link {
    min-width: 5.25rem;
    min-height: 2.75rem;
    gap: 0.32rem;
    padding: 0 0.45rem;
  }

  .nav-link-icon {
    width: 1.75rem;
    height: 1.75rem;
  }

  .nav-link-copy small {
    display: none;
  }

  .nav-link-copy strong {
    font-size: 0.78rem;
  }

  .nav-cta {
    display: none;
  }
}
</style>
