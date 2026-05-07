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

      <router-link v-if="user" :to="authTarget" class="nav-cta nav-cta--user">
        <Icon :icon="user ? 'ph:user-circle' : 'ph:sign-in'" width="15" />
        <span>
          <strong>账户</strong>
          <small>{{ accountLabel }}</small>
        </span>
      </router-link>

      <div v-else class="auth-actions" aria-label="账号操作">
        <router-link :to="loginTarget" class="auth-link auth-link--login">
          登录
        </router-link>
        <router-link :to="registerTarget" class="auth-link auth-link--register">
          注册
        </router-link>
      </div>
    </div>
  </header>

  <nav class="mobile-tabbar" aria-label="移动导航">
    <router-link v-for="item in navItems" :key="`mobile-${item.path}`" :to="item.path" class="mobile-tab" active-class="mobile-tab--active">
      <Icon :icon="item.icon" width="20" />
      <span>{{ item.label }}</span>
    </router-link>
    <router-link :to="authTarget" class="mobile-tab" active-class="mobile-tab--active">
      <Icon :icon="user ? 'ph:user-circle' : 'ph:sign-in'" width="20" />
      <span>{{ user ? '账户' : '登录' }}</span>
    </router-link>
  </nav>
</template>

<script>
import { Icon } from '@iconify/vue'
import { AUTH_CHANGE_EVENT, authRouteFor, getStoredUser } from '../utils/session.js'

export default {
  name: 'NavBar',
  components: { Icon },
  data() {
    return {
      user: null,
      navItems: [
        { path: '/video', label: '视频', tag: '补帧剪辑', icon: 'ph:video-camera' },
        { path: '/image', label: '图片', tag: '压缩转换', icon: 'ph:image' },
        { path: '/audio', label: '音频', tag: '提取剪切', icon: 'ph:music-notes' },
      ],
    }
  },
  mounted() {
    this.syncUser()
    window.addEventListener(AUTH_CHANGE_EVENT, this.syncUser)
    window.addEventListener('storage', this.syncUser)
  },
  beforeUnmount() {
    window.removeEventListener(AUTH_CHANGE_EVENT, this.syncUser)
    window.removeEventListener('storage', this.syncUser)
  },
  computed: {
    authTarget() {
      return this.user ? '/auth' : this.loginTarget
    },
    loginTarget() {
      return this.authTargetFor('login')
    },
    registerTarget() {
      return this.authTargetFor('register')
    },
    accountLabel() {
      return this.user?.display_name || this.user?.email || '已登录'
    },
  },
  methods: {
    syncUser() {
      this.user = getStoredUser()
    },
    authTargetFor(mode) {
      const target = authRouteFor(this.$route.fullPath)
      return {
        ...target,
        query: {
          ...target.query,
          mode,
        },
      }
    },
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
.nav-cta,
.auth-link {
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

.auth-actions {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  flex: 0 0 auto;
  padding: 0.18rem;
  border: 1px solid rgba(255,255,255,0.055);
  border-radius: 999px;
  background: rgba(0,0,0,0.14);
}

.auth-link {
  min-width: 4.35rem;
  min-height: 2.55rem;
  justify-content: center;
  padding: 0 0.95rem;
  border: 1px solid transparent;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0;
  transition:
    color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    border-color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    background 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    box-shadow 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    transform 0.24s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.auth-link--login {
  color: var(--text-secondary);
  border-color: rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.025);
}

.auth-link--register {
  color: var(--bg);
  border-color: rgba(212,135,94,0.42);
  background: linear-gradient(180deg, rgba(222,153,105,0.96), rgba(199,119,77,0.94));
  box-shadow: 0 10px 22px rgba(212,135,94,0.14);
}

.auth-link:hover {
  transform: translateY(-1px);
}

.auth-link:active {
  transform: translateY(0);
}

.auth-link--login:hover {
  color: var(--text-primary);
  border-color: rgba(212,135,94,0.24);
  background: rgba(255,255,255,0.045);
}

.auth-link--register:hover {
  border-color: rgba(232,164,116,0.5);
  background: linear-gradient(180deg, rgba(226,158,111,1), rgba(204,124,82,0.96));
  box-shadow: 0 12px 26px rgba(212,135,94,0.18);
}

.nav-cta {
  gap: 0.48rem;
  min-height: 2.7rem;
  max-width: 12rem;
  padding: 0 0.9rem;
  border-radius: 999px;
  color: var(--bg);
  background: var(--accent);
  box-shadow: 0 12px 30px rgba(212, 135, 94, 0.2);
  transition:
    transform 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    box-shadow 0.24s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.nav-cta span {
  display: grid;
  min-width: 0;
  line-height: 1.05;
}

.nav-cta strong {
  font-size: 0.76rem;
  font-weight: 900;
}

.nav-cta small {
  max-width: 7.2rem;
  overflow: hidden;
  color: rgba(26,23,20,0.72);
  font-size: 0.62rem;
  font-weight: 800;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.nav-cta--user {
  color: var(--text-primary);
  border: 1px solid rgba(212,135,94,0.3);
  background:
    linear-gradient(135deg, rgba(212,135,94,0.16), rgba(255,255,255,0.035)),
    rgba(14,12,10,0.72);
}

.nav-cta--user small {
  color: var(--text-tertiary);
}

.nav-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 36px rgba(212, 135, 94, 0.28);
}

.mobile-tabbar {
  display: none;
}

@media (max-width: 820px) {
  .navbar {
    height: 3.65rem;
  }

  .nav-inner {
    gap: 0.55rem;
    padding: 0 0.85rem;
  }

  .nav-logo {
    min-width: auto;
  }

  .nav-links {
    display: none;
  }

  .nav-cta {
    display: none;
  }

  .auth-actions {
    display: none;
  }

  .mobile-tabbar {
    position: fixed;
    left: 0.65rem;
    right: 0.65rem;
    bottom: 0;
    z-index: 70;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.35rem;
    padding: 0.42rem 0.42rem calc(0.42rem + env(safe-area-inset-bottom));
    border: 1px solid rgba(255,255,255,0.075);
    border-bottom: 0;
    border-radius: 18px 18px 0 0;
    background:
      linear-gradient(180deg, rgba(31, 26, 22, 0.92), rgba(10, 9, 8, 0.96)),
      rgba(10, 9, 8, 0.86);
    box-shadow: 0 -18px 50px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,255,255,0.055);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
  }

  .mobile-tab {
    min-width: 0;
    min-height: 3.15rem;
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.18rem;
    border: 1px solid transparent;
    border-radius: 13px;
    color: var(--text-tertiary);
    text-decoration: none;
    font-size: 0.72rem;
    font-weight: 800;
    transition:
      color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
      border-color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
      background 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
      transform 0.24s cubic-bezier(0.2, 0.9, 0.2, 1);
  }

  .mobile-tab svg {
    color: var(--accent);
  }

  .mobile-tab--active {
    color: var(--text-primary);
    border-color: rgba(212,135,94,0.38);
    background: linear-gradient(135deg, rgba(212,135,94,0.2), rgba(212,135,94,0.055)), rgba(255,255,255,0.035);
    box-shadow: inset 0 0 0 1px rgba(212,135,94,0.08);
  }
}
</style>
