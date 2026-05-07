<template>
  <footer class="footer">
    <div class="footer-inner">
      <router-link to="/" class="footer-logo">
        <span class="footer-mark" />
        <span>Vlade</span>
      </router-link>
      <p>视频、图片、音频统一处理，上传后完成体检、参数调整与结果导出。</p>
      <div class="footer-links">
        <router-link to="/video">视频</router-link>
        <router-link to="/image">图片</router-link>
        <router-link to="/audio">音频</router-link>
      </div>
    </div>
  </footer>
</template>

<script>
export default { name: 'AppFooter' }
</script>

<style scoped>
.footer {
  position: relative;
  z-index: 2;
  padding: 3rem clamp(1.25rem, 5vw, 5rem);
  border-top: 1px solid rgba(255, 255, 255, 0.065);
  background:
    radial-gradient(circle at 10% 0%, rgba(212, 135, 94, 0.08), transparent 20rem),
    linear-gradient(135deg, rgba(16, 14, 12, 0.88), rgba(8, 7, 6, 0.96));
}

.footer-inner {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 1rem;
  align-items: center;
}

.footer-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-primary);
  text-decoration: none;
  font-family: var(--font-mono);
  font-weight: 800;
}

.footer-mark {
  width: 0.55rem;
  height: 0.55rem;
  transform: rotate(45deg);
  background: var(--accent);
}

.footer p {
  color: var(--text-tertiary);
  font-size: 0.82rem;
}

.footer-links {
  display: flex;
  gap: 0.8rem;
}

.footer-links a {
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: 0.8rem;
  transition: color 0.22s cubic-bezier(0.2, 0.9, 0.2, 1);
}

.footer-links a:hover {
  color: var(--accent);
}

@media (max-width: 700px) {
  .footer-inner {
    grid-template-columns: 1fr;
  }
}
</style>
