<template>
  <main class="auth-page">
    <section class="auth-shell">
      <div class="auth-copy">
        <span class="kicker">ACCOUNT / VLADE</span>
        <h1>{{ user ? '账户已就绪。' : mode === 'login' ? '继续处理你的媒体。' : '创建你的工作台账户。' }}</h1>
        <p>{{ user ? '回到工作台后就可以上传、体检、处理并保存结果。' : '登录后才能上传处理文件，注册成功会自动进入工作台。' }}</p>

        <div class="db-card">
          <Icon icon="ph:database" width="22" />
          <div>
            <strong>后端写入</strong>
            <span>FastAPI 使用 session pool 连接 PostgreSQL</span>
          </div>
        </div>
      </div>

      <form v-if="!user" class="auth-panel" @submit.prevent="submit">
        <div class="mode-tabs" role="tablist" aria-label="账号模式">
          <button type="button" :class="{ active: mode === 'login' }" @click="setMode('login')">
            <Icon icon="ph:sign-in" width="17" />
            登录
          </button>
          <button type="button" :class="{ active: mode === 'register' }" @click="setMode('register')">
            <Icon icon="ph:user-plus" width="17" />
            注册
          </button>
        </div>

        <label v-if="mode === 'register'" class="field">
          <span>昵称</span>
          <input v-model.trim="form.display_name" type="text" autocomplete="name" placeholder="例如 Vlade" />
        </label>

        <label class="field">
          <span>邮箱</span>
          <input v-model.trim="form.email" type="email" autocomplete="email" placeholder="you@example.com" required />
        </label>

        <label class="field">
          <span>密码</span>
          <input v-model="form.password" type="password" :autocomplete="mode === 'login' ? 'current-password' : 'new-password'" placeholder="至少 8 位" required minlength="8" />
        </label>

        <p v-if="message" class="message" :class="{ error: hasError }">{{ message }}</p>

        <button class="submit-btn" type="submit" :disabled="loading">
          <Icon :icon="loading ? 'ph:spinner-gap' : submitIcon" width="18" :class="{ spin: loading }" />
          {{ loading ? '处理中' : submitLabel }}
        </button>

      </form>

      <section v-else class="auth-panel account-panel">
        <div class="account-avatar">
          <Icon icon="ph:user-circle" width="30" />
        </div>
        <div class="account-copy">
          <span>当前账户</span>
          <strong>{{ user.display_name || user.email }}</strong>
          <small>{{ user.email }}</small>
        </div>
        <button class="submit-btn" type="button" @click="continueWork">
          <Icon icon="ph:arrow-up-right" width="18" />
          继续使用
        </button>
        <button class="ghost-btn" type="button" @click="logout" :disabled="loading">
          <Icon icon="ph:sign-out" width="17" />
          退出当前账户
        </button>
        <p v-if="message" class="message" :class="{ error: hasError }">{{ message }}</p>
      </section>
    </section>
  </main>
</template>

<script>
import { Icon } from '@iconify/vue'
import { getCurrentUser, loginUser, logoutUser, registerUser } from '../api/index.js'
import { clearSession, getStoredUser, getToken, safeRedirectPath, storeSession } from '../utils/session.js'

export default {
  name: 'AuthView',
  components: { Icon },
  data() {
    return {
      mode: 'login',
      loading: false,
      message: '',
      hasError: false,
      user: null,
      form: {
        display_name: '',
        email: '',
        password: '',
      },
    }
  },
  computed: {
    submitLabel() {
      return this.mode === 'login' ? '登录' : '创建账户'
    },
    submitIcon() {
      return this.mode === 'login' ? 'ph:sign-in' : 'ph:user-plus'
    },
    redirectPath() {
      return safeRedirectPath(this.$route.query.redirect)
    },
  },
  watch: {
    '$route.query.mode'() {
      this.syncModeFromRoute()
    },
  },
  created() {
    this.syncModeFromRoute()
  },
  async mounted() {
    this.user = getStoredUser()
    if (getToken()) {
      try {
        const data = await getCurrentUser()
        this.storeSession(getToken(), data.user)
      } catch {
        this.clearSession()
      }
    }
  },
  methods: {
    setMode(mode) {
      const nextMode = this.normalizeMode(mode)
      this.mode = nextMode
      this.message = ''
      this.hasError = false
      if (this.$route.query.mode !== nextMode) {
        this.$router.replace({
          path: this.$route.path,
          query: {
            ...this.$route.query,
            mode: nextMode,
          },
        })
      }
    },
    normalizeMode(mode) {
      return mode === 'register' ? 'register' : 'login'
    },
    syncModeFromRoute() {
      const nextMode = this.normalizeMode(this.$route.query.mode)
      if (this.mode !== nextMode) {
        this.mode = nextMode
        this.message = ''
        this.hasError = false
      }
    },
    storeSession(token, user) {
      storeSession(token, user)
      this.user = user
    },
    clearSession() {
      clearSession()
      this.user = null
    },
    continueWork() {
      this.$router.replace(this.redirectPath)
    },
    async submit() {
      this.loading = true
      this.message = ''
      this.hasError = false
      try {
        const payload = {
          email: this.form.email,
          password: this.form.password,
          display_name: this.form.display_name,
        }
        const data = this.mode === 'login'
          ? await loginUser(payload)
          : await registerUser(payload)
        this.storeSession(data.token, data.user)
        this.form.password = ''
        await this.$router.replace(this.redirectPath)
      } catch (err) {
        this.hasError = true
        this.message = err.message || '操作失败'
      } finally {
        this.loading = false
      }
    },
    async logout() {
      this.loading = true
      try {
        await logoutUser()
      } catch {
        // Local session still needs to be cleared if the server is unreachable.
      } finally {
        this.clearSession()
        this.message = '已退出登录'
        this.hasError = false
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 4.25rem);
  position: relative;
  z-index: 2;
  display: grid;
  place-items: center;
  padding: 4rem 1.25rem;
}

.auth-shell {
  width: min(1040px, 100%);
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 430px);
  gap: 2rem;
  align-items: center;
}

.auth-copy {
  min-width: 0;
}

.kicker {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0;
}

.auth-copy h1 {
  max-width: 11ch;
  margin-top: 1rem;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2.6rem, 5vw, 5.2rem);
  line-height: 0.96;
  letter-spacing: 0;
}

.auth-copy p {
  max-width: 34rem;
  margin-top: 1.2rem;
  color: var(--text-secondary);
  font-size: 1rem;
}

.db-card {
  width: min(28rem, 100%);
  margin-top: 2rem;
  display: flex;
  gap: 0.85rem;
  align-items: center;
  padding: 1rem;
  border: 1px solid rgba(255,255,255,0.075);
  border-radius: 8px;
  background:
    linear-gradient(135deg, rgba(212,135,94,0.16), rgba(255,255,255,0.035)),
    rgba(16,14,12,0.62);
}

.db-card svg {
  color: var(--accent);
  flex: 0 0 auto;
}

.db-card div {
  display: grid;
  gap: 0.12rem;
}

.db-card strong {
  color: var(--text-primary);
  font-size: 0.92rem;
}

.db-card span {
  color: var(--text-tertiary);
  font-size: 0.82rem;
}

.auth-panel {
  display: grid;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid rgba(255,255,255,0.085);
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(37,31,26,0.92), rgba(16,14,12,0.86)),
    rgba(20,18,15,0.82);
  box-shadow: 0 28px 80px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,255,255,0.045);
  backdrop-filter: blur(18px);
}

.mode-tabs {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.45rem;
  padding: 0.3rem;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 8px;
  background: rgba(0,0,0,0.18);
}

.mode-tabs button,
.submit-btn,
.ghost-btn {
  min-height: 2.8rem;
  border: 0;
  border-radius: 7px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.42rem;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
  transition:
    transform 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    background 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    color 0.24s cubic-bezier(0.2, 0.9, 0.2, 1),
    opacity 0.24s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.mode-tabs button {
  color: var(--text-tertiary);
  background: transparent;
}

.mode-tabs button.active {
  color: var(--bg);
  background: var(--accent);
}

.field {
  display: grid;
  gap: 0.45rem;
}

.field span {
  color: var(--text-secondary);
  font-size: 0.78rem;
  font-weight: 800;
}

.field input {
  width: 100%;
  min-height: 3rem;
  padding: 0 0.9rem;
  border: 1px solid rgba(255,255,255,0.09);
  border-radius: 7px;
  outline: none;
  color: var(--text-primary);
  background: rgba(0,0,0,0.22);
  font: inherit;
  transition:
    border-color 0.22s cubic-bezier(0.2, 0.9, 0.2, 1),
    box-shadow 0.22s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.field input:focus {
  border-color: rgba(212,135,94,0.62);
  box-shadow: 0 0 0 3px rgba(212,135,94,0.12);
}

.message {
  min-height: 1.4rem;
  color: #9bd6ad;
  font-size: 0.86rem;
  font-weight: 800;
}

.message.error {
  color: #ff9c8c;
}

.submit-btn {
  color: var(--bg);
  background: var(--accent);
}

.ghost-btn {
  color: var(--text-primary);
  background: rgba(255,255,255,0.055);
  border: 1px solid rgba(255,255,255,0.08);
}

.account-panel {
  align-content: start;
  text-align: left;
}

.account-avatar {
  width: 3.75rem;
  height: 3.75rem;
  display: grid;
  place-items: center;
  border-radius: 16px;
  color: var(--accent);
  background:
    radial-gradient(circle at 30% 20%, rgba(212,135,94,0.22), transparent 4rem),
    rgba(0,0,0,0.2);
  box-shadow: inset 0 0 0 1px rgba(212,135,94,0.16);
}

.account-copy {
  display: grid;
  gap: 0.14rem;
  min-width: 0;
}

.account-copy span {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.68rem;
}

.account-copy strong {
  color: var(--text-primary);
  font-size: 1.05rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.account-copy small {
  color: var(--text-tertiary);
  overflow-wrap: anywhere;
}

.submit-btn:disabled,
.ghost-btn:disabled {
  cursor: wait;
  opacity: 0.7;
}

.submit-btn:not(:disabled):hover,
.ghost-btn:not(:disabled):hover,
.mode-tabs button:not(.active):hover {
  transform: translateY(-1px);
}

.user-strip {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  min-width: 0;
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 800;
}

.user-strip svg {
  color: #9bd6ad;
  flex: 0 0 auto;
}

.user-strip span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spin {
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 820px) {
  .auth-page {
    min-height: calc(100vh - 3.65rem);
    padding: 2.2rem 0.85rem 6.4rem;
    place-items: start stretch;
  }

  .auth-shell {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .auth-copy h1 {
    max-width: 9ch;
    font-size: 3rem;
  }
}
</style>
