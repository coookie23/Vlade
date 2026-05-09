<template>
  <main class="home">
    <section class="entry-stage">
      <div class="stage-copy">
        <span class="kicker">VLADE / {{ copy.workbench }}</span>
        <h1>{{ copy.heroTitle }}</h1>
        <p>{{ copy.heroText }}</p>

        <div class="stage-actions">
          <button
            ref="launchButton"
            class="launch-control"
            type="button"
            @click="jumpToFlow"
            @mouseenter="initLaunchMotion"
            @mousemove="moveLaunch"
            @mouseleave="resetLaunch"
          >
            <span class="launch-glow" />
            <span class="launch-core">
              <Icon icon="ph:cursor-click" width="25" />
            </span>
            <span class="launch-copy">
              <strong>{{ copy.start }}</strong>
              <small>{{ copy.choose }}</small>
            </span>
            <span class="launch-ports" aria-hidden="true">
              <span class="launch-port" :title="copy.video"><Icon icon="ph:video-camera" width="15" /></span>
              <span class="launch-port" :title="copy.image"><Icon icon="ph:image" width="15" /></span>
              <span class="launch-port" :title="copy.audio"><Icon icon="ph:music-notes" width="15" /></span>
            </span>
          </button>
          <router-link class="login-control" :to="{ path: '/auth', query: { redirect: '/video' } }">
            <Icon icon="ph:sign-in" width="18" />
            <span>
              <strong>{{ copy.login }}</strong>
              <small>{{ copy.loginHint }}</small>
            </span>
          </router-link>
        </div>
      </div>

      <div class="media-stack" aria-hidden="true">
        <div class="preview-frame preview-frame--main">
          <MediaVisual class="hero-visual" :suite="homeSuites[0]" variant="panel" />
          <div class="frame-ui"><span /><span /><span /></div>
          <div class="frame-caption">
            <strong>compress.mp4</strong>
            <small>72% smaller</small>
          </div>
        </div>
        <div class="preview-frame preview-frame--float">
          <MediaVisual class="hero-visual hero-visual--audio" :suite="homeSuites[2]" variant="card" />
          <div class="wave-lines">
            <span v-for="i in 18" :key="i" :style="{ height: `${18 + (i % 5) * 12}px` }" />
          </div>
        </div>
        <div class="process-chip chip-a">
          <Icon icon="ph:scissors" width="16" />
          {{ copy.cut }}
        </div>
        <div class="process-chip chip-b">
          <Icon icon="ph:arrows-left-right" width="16" />
          {{ copy.convert }}
        </div>
      </div>
    </section>

    <section ref="flowSection" class="flow-section" :class="{ 'flow-section--focus': flowFocus }" :style="flowStyle">
      <div class="flow-layout">
        <aside class="flow-visual" data-reveal>
          <div class="visual-window">
            <div class="lab-topbar">
              <span>MEDIA CHECK</span>
              <b>{{ progressLabel }}</b>
            </div>
            <img
              src="https://picsum.photos/seed/vlade-left-lab/640/800"
              alt=""
              width="640"
              height="800"
              loading="lazy"
            />
            <div class="visual-scan" />
            <div class="visual-grid">
              <span v-for="i in 18" :key="i" />
            </div>
            <div class="lab-chip lab-chip--format">
              <Icon icon="ph:file-magnifying-glass" width="16" />
              <span>ACTIVE</span>
              <strong>{{ activeSuiteLabel }}</strong>
            </div>
            <div class="lab-chip lab-chip--queue">
              <Icon icon="ph:stack" width="16" />
              <span>QUEUE</span>
              <strong>{{ copy.ready }}</strong>
            </div>
            <div class="visual-console">
              <span class="console-dot" />
              <strong>{{ activeSuiteLabel }}</strong>
              <small>{{ copy.pickWorkbench }}</small>
            </div>
          </div>

          <div class="scroll-meter">
            <span>FLOW</span>
            <div><i /></div>
            <small>{{ progressLabel }}</small>
          </div>
        </aside>

        <div class="flow-content">
          <div class="flow-head" data-reveal>
            <span>/ {{ copy.entry }}</span>
            <h2>{{ copy.flowTitle }}</h2>
            <p>{{ copy.flowText }}</p>
          </div>

          <div class="flow-track">
            <router-link
              v-for="(suite, index) in homeSuites"
              :key="suite.key"
              :to="suite.path"
              class="flow-node"
              :class="`flow-node--${index}`"
              :style="{ '--node-shift': `${index * 18}px`, '--node-lift': `${36 + index * 12}px` }"
              @mousemove="trackNodeLight"
              data-reveal
            >
              <div class="flow-action-stack" aria-hidden="true">
                <span
                  v-for="(tool, toolIndex) in suite.featuredTools"
                  :key="tool.title"
                  class="flow-action-card"
                  :style="{ '--action-index': toolIndex }"
                >
                  <Icon :icon="tool.icon" width="14" />
                  <b>{{ tool.title }}</b>
                  <i />
                </span>
              </div>
              <MediaVisual class="flow-node-visual" :suite="suite" variant="card" />
              <div class="flow-node-copy">
                <span>{{ suite.eyebrow }}</span>
                <h3>{{ suite.title }}</h3>
                <p>{{ suite.intro }}</p>
              </div>
              <Icon class="flow-arrow" icon="ph:arrow-up-right" width="18" />
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="details-band">
      <div class="work-steps" data-reveal>
        <div v-for="step in steps" :key="step.title" class="step-line">
          <span class="step-index">{{ step.index }}</span>
          <div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </div>
        </div>
      </div>

      <div class="quick-panel" data-reveal>
        <span class="panel-dot" />
        <h2>{{ copy.quickTitle }}</h2>
        <p>{{ copy.quickText }}</p>
        <div class="panel-tags">
          <span>{{ copy.needLogin }}</span>
          <span>{{ copy.browserUpload }}</span>
          <span>{{ copy.download }}</span>
        </div>
      </div>
    </section>

    <AppFooter />
  </main>
</template>

<script>
import { Icon } from '@iconify/vue'
import AppFooter from '../components/AppFooter.vue'
import MediaVisual from '../components/MediaVisual.vue'
import { suiteList } from '../data/toolSuites.js'

const copy = {
  workbench: '\u5a92\u4f53\u5de5\u4f5c\u53f0',
  heroTitle: '媒体处理更有章法',
  heroText: '从上传体检到压缩转码和下载，所有步骤都收在同一个工作台里，流程更短，结果更稳。',
  start: '\u5f00\u59cb\u4f7f\u7528',
  choose: '\u9009\u62e9\u4f60\u7684\u5a92\u4f53\u5de5\u4f5c\u53f0',
  login: '\u767b\u5f55',
  loginHint: '\u4e0a\u4f20\u524d\u9700\u8981\u8d26\u6237',
  video: '\u89c6\u9891',
  image: '\u56fe\u7247',
  audio: '\u97f3\u9891',
  cut: '\u88c1\u526a',
  convert: '\u8f6c\u6362',
  ready: '\u5df2\u5c31\u7eea',
  pickWorkbench: '\u9009\u62e9\u4e00\u4e2a\u5de5\u4f5c\u53f0',
  entry: '\u9009\u62e9\u5165\u53e3',
  flowTitle: '三类素材一套流程',
  flowText: '视频、图片、音频共用同一套上传、参数和结果视图，只在需要时切换工具细节。',
  quickTitle: '把等待变成确定性',
  quickText: '界面只呈现当前工具真正需要的选项，完成后给出清楚的结果摘要和下载入口。',
  needLogin: '\u767b\u5f55\u540e\u5904\u7406',
  browserUpload: '\u6d4f\u89c8\u5668\u4e0a\u4f20',
  download: '\u7ed3\u679c\u4e0b\u8f7d',
}

const displayCopy = {
  video: {
    title: '视频工作台',
    eyebrow: 'VIDEO',
    intro: '面向短片、录屏和素材包，完成压缩、转码、裁剪与合并。',
    featuredTools: [
      { title: '\u88c1\u526a', icon: 'ph:scissors' },
      { title: '\u8f6c\u6362', icon: 'ph:arrows-left-right' },
      { title: '\u538b\u7f29', icon: 'ph:arrows-in-line-vertical' },
    ],
  },
  image: {
    title: '图片工作台',
    eyebrow: 'IMAGE',
    intro: '把网页图、封面和头像的尺寸、格式与体积收在一处处理。',
    featuredTools: [
      { title: '\u88c1\u526a', icon: 'ph:crop' },
      { title: '\u538b\u7f29', icon: 'ph:image-square' },
      { title: '\u6c34\u5370', icon: 'ph:text-t' },
    ],
  },
  audio: {
    title: '音频工作台',
    eyebrow: 'AUDIO',
    intro: '整理旁白、配乐和录音片段，快速完成剪切、转码和音量校准。',
    featuredTools: [
      { title: '\u526a\u5207', icon: 'ph:waveform' },
      { title: '\u97f3\u91cf', icon: 'ph:speaker-high' },
      { title: '\u964d\u566a', icon: 'ph:waves' },
    ],
  },
}

export default {
  name: 'Home',
  components: { Icon, AppFooter, MediaVisual },
  data() {
    return {
      copy,
      suites: suiteList,
      flowProgress: 0,
      flowFocus: false,
      flowFocusTimer: 0,
      launchMotion: null,
      gsapApi: null,
      revealObserver: null,
      scrollRaf: 0,
      steps: [
        { index: '01', title: '导入素材', text: '拖入文件或从本地选择，先让系统读取基础信息。' },
        { index: '02', title: '校准参数', text: '只展示当前工具相关设置，减少不必要的判断。' },
        { index: '03', title: '导出结果', text: '处理完成后查看摘要，再把新文件保存到本地。' },
      ],
    }
  },
  computed: {
    homeSuites() {
      return this.suites.map((suite) => ({
        ...suite,
        ...(displayCopy[suite.key] || {}),
      }))
    },
    flowStyle() {
      const progress = this.flowProgress
      return {
        '--flow-progress': progress.toFixed(3),
        '--flow-meter-width': `${progress * 100}%`,
        '--flow-track-shift': `${progress * 14}px`,
        '--flow-window-shift': `${progress * -18}px`,
        '--flow-window-tilt': `${(progress - 0.5) * -3}deg`,
        '--flow-image-scale': (1.02 + progress * 0.08).toFixed(3),
        '--flow-grid-opacity': (0.24 + progress * 0.36).toFixed(3),
        '--flow-grid-shift': `${progress * 18}px`,
      }
    },
    activeSuiteLabel() {
      const index = Math.min(this.homeSuites.length - 1, Math.floor(this.flowProgress * this.homeSuites.length))
      return this.homeSuites[index]?.title || copy.workbench
    },
    progressLabel() {
      return `${Math.round(this.flowProgress * 100)}%`
    },
  },
  mounted() {
    this.initReveal()
    this.updateFlowProgress()
    window.addEventListener('scroll', this.queueFlowProgress, { passive: true })
    window.addEventListener('resize', this.queueFlowProgress)
  },
  beforeUnmount() {
    if (this.revealObserver) this.revealObserver.disconnect()
    if (this.scrollRaf) cancelAnimationFrame(this.scrollRaf)
    if (this.flowFocusTimer) window.clearTimeout(this.flowFocusTimer)
    this.resetLaunch()
    window.removeEventListener('scroll', this.queueFlowProgress)
    window.removeEventListener('resize', this.queueFlowProgress)
  },
  methods: {
    jumpToFlow() {
      const section = this.$refs.flowSection
      if (!section) return
      this.flowFocus = true
      if (this.flowFocusTimer) window.clearTimeout(this.flowFocusTimer)
      section.scrollIntoView({ behavior: 'smooth', block: 'start' })
      this.flowFocusTimer = window.setTimeout(() => { this.flowFocus = false }, 1700)
    },
    async initLaunchMotion() {
      if (this.launchMotion || !this.$refs.launchButton || !window.matchMedia('(pointer: fine)').matches) return
      // GSAP 只在按钮交互时加载，避免首屏 JS 直接变重。
      if (!this.gsapApi) {
        const module = await import('gsap')
        this.gsapApi = module.gsap
      }
      const gsap = this.gsapApi
      const root = this.$refs.launchButton
      const core = root.querySelector('.launch-core')
      const copyNode = root.querySelector('.launch-copy')
      const ports = Array.from(root.querySelectorAll('.launch-port'))
      const ease = 'power3.out'
      const quick = (target, prop, duration = 0.38) => gsap.quickTo(target, prop, { duration, ease })
      this.launchMotion = {
        rootX: quick(root, 'x'),
        rootY: quick(root, 'y'),
        rootScale: quick(root, 'scale', 0.28),
        coreX: quick(core, 'x'),
        coreY: quick(core, 'y'),
        coreRotate: quick(core, 'rotation', 0.42),
        copyX: quick(copyNode, 'x'),
        copyY: quick(copyNode, 'y'),
        ports: ports.map((port) => ({ x: quick(port, 'x'), y: quick(port, 'y') })),
      }
    },
    moveLaunch(event) {
      const root = event.currentTarget
      const rect = root.getBoundingClientRect()
      const localX = event.clientX - rect.left
      const localY = event.clientY - rect.top
      const dx = (localX - rect.width / 2) / (rect.width / 2)
      const dy = (localY - rect.height / 2) / (rect.height / 2)
      root.style.setProperty('--pointer-x', `${localX}px`)
      root.style.setProperty('--pointer-y', `${localY}px`)
      this.initLaunchMotion()
      if (!this.launchMotion) return
      this.launchMotion.rootX(dx * 10)
      this.launchMotion.rootY(dy * 8)
      this.launchMotion.rootScale(1.015)
      this.launchMotion.coreX(dx * 16)
      this.launchMotion.coreY(dy * 12)
      this.launchMotion.coreRotate(dx * -9)
      this.launchMotion.copyX(dx * 5)
      this.launchMotion.copyY(dy * 4)
      this.launchMotion.ports.forEach((port, index) => {
        port.x(dx * (7 + index * 2))
        port.y(dy * (5 + index * 1.5) - 3)
      })
    },
    resetLaunch() {
      if (!this.launchMotion) return
      this.launchMotion.rootX(0)
      this.launchMotion.rootY(0)
      this.launchMotion.rootScale(1)
      this.launchMotion.coreX(0)
      this.launchMotion.coreY(0)
      this.launchMotion.coreRotate(0)
      this.launchMotion.copyX(0)
      this.launchMotion.copyY(0)
      this.launchMotion.ports.forEach((port) => { port.x(0); port.y(0) })
    },
    trackNodeLight(event) {
      const rect = event.currentTarget.getBoundingClientRect()
      event.currentTarget.style.setProperty('--node-x', `${event.clientX - rect.left}px`)
      event.currentTarget.style.setProperty('--node-y', `${event.clientY - rect.top}px`)
    },
    initReveal() {
      this.revealObserver = new IntersectionObserver(
        entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) entry.target.classList.add('is-visible')
          })
        },
        { threshold: 0.18, rootMargin: '0px 0px -8% 0px' },
      )
      this.$el.querySelectorAll('[data-reveal]').forEach(el => this.revealObserver.observe(el))
    },
    queueFlowProgress() {
      if (this.scrollRaf) return
      this.scrollRaf = requestAnimationFrame(() => {
        this.scrollRaf = 0
        this.updateFlowProgress()
      })
    },
    updateFlowProgress() {
      const section = this.$refs.flowSection
      if (!section) return
      const rect = section.getBoundingClientRect()
      const travel = window.innerHeight + rect.height
      const raw = (window.innerHeight - rect.top) / travel
      this.flowProgress = Math.min(1, Math.max(0, raw))
    },
  },
}
</script>

<style scoped>
.home {
  position: relative;
  z-index: 2;
  overflow: hidden;
  background:
    radial-gradient(circle at 18% 8%, rgba(212, 135, 94, 0.12), transparent 30rem),
    radial-gradient(circle at 85% 42%, rgba(138, 94, 55, 0.14), transparent 28rem),
    linear-gradient(145deg, rgba(25, 21, 18, 0.88), rgba(10, 9, 8, 0.98));
}

.home::before {
  content: '';
  position: fixed;
  inset: 3.5rem 0 0;
  z-index: -1;
  opacity: 0.075;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 220 220' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.82' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.75'/%3E%3C/svg%3E");
}

[data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition:
    opacity 0.72s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.72s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-reveal].is-visible {
  opacity: 1;
  transform: translateY(0);
}

.entry-stage {
  min-height: calc(100vh - 3.5rem);
  display: grid;
  grid-template-columns: minmax(0, 0.85fr) minmax(420px, 1.15fr);
  gap: clamp(2rem, 5vw, 5rem);
  align-items: center;
  padding: clamp(2rem, 5vw, 5rem);
}

.stage-copy {
  max-width: 42rem;
  transform: translateY(-2vh);
  opacity: 0;
  animation: homeCopyIn 0.92s cubic-bezier(0.16, 1, 0.3, 1) 0.08s forwards;
}

.kicker,
.flow-head span {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.1em;
}

.stage-copy h1 {
  margin-top: 0.8rem;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: 6.4rem;
  font-weight: 850;
  line-height: 0.92;
  letter-spacing: 0;
  max-width: 9ch;
  text-wrap: balance;
}

.stage-copy p {
  max-width: 30rem;
  margin-top: 1.25rem;
  color: var(--text-secondary);
  font-size: 1.08rem;
  line-height: 1.75;
}

.stage-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 2.35rem;
}

.launch-control {
  --pointer-x: 50%;
  --pointer-y: 50%;
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 1rem;
  min-height: 6.4rem;
  min-width: min(100%, 30rem);
  padding: 0.8rem 7.2rem 0.8rem 0.8rem;
  border: 1px solid rgba(212, 135, 94, 0.34);
  border-radius: 28px;
  color: var(--text-primary);
  cursor: pointer;
  overflow: hidden;
  background:
    radial-gradient(circle at var(--pointer-x) var(--pointer-y), rgba(212, 135, 94, 0.2), transparent 9rem),
    radial-gradient(circle at 14% 50%, rgba(212, 135, 94, 0.2), transparent 8rem),
    linear-gradient(135deg, rgba(48, 38, 30, 0.88), rgba(13, 11, 9, 0.86));
  box-shadow:
    0 28px 90px rgba(0, 0, 0, 0.4),
    0 16px 46px rgba(212, 135, 94, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.07),
    inset 0 -24px 40px rgba(0, 0, 0, 0.22);
  transition:
    border-color 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    background 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.login-control {
  position: relative;
  min-height: 3.25rem;
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0 1rem;
  border: 1px solid rgba(212, 135, 94, 0.26);
  border-radius: 16px;
  color: var(--text-primary);
  text-decoration: none;
  background:
    radial-gradient(circle at 20% 20%, rgba(212,135,94,0.14), transparent 6rem),
    rgba(10, 9, 8, 0.34);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.05);
  transition:
    transform 0.3s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.3s cubic-bezier(0.16, 1, 0.3, 1),
    background 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.login-control svg {
  color: var(--accent);
}

.login-control span {
  display: grid;
  line-height: 1.1;
}

.login-control strong {
  font-size: 0.86rem;
}

.login-control small {
  color: var(--text-tertiary);
  font-size: 0.68rem;
}

.login-control:hover {
  transform: translateY(-2px);
  border-color: rgba(212,135,94,0.48);
  background:
    radial-gradient(circle at 30% 30%, rgba(212,135,94,0.2), transparent 7rem),
    rgba(20, 17, 14, 0.5);
}

.launch-control::before {
  content: '';
  position: absolute;
  inset: 0.52rem;
  padding: 1px;
  border-radius: 22px;
  pointer-events: none;
  background:
    linear-gradient(135deg, rgba(212,135,94,0.22), rgba(212,135,94,0.025), rgba(212,135,94,0.3), rgba(212,135,94,0.035));
  background-size: 180% 180%;
  opacity: 0.58;
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  animation: launchBorder 5.4s cubic-bezier(0.65, 0, 0.35, 1) infinite alternate;
}

.launch-control::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0.42;
  background:
    linear-gradient(90deg, transparent 0 22%, rgba(212,135,94,0.08) 22% 22.4%, transparent 22.4% 100%),
    linear-gradient(0deg, transparent 0 62%, rgba(255,255,255,0.035) 62% 62.5%, transparent 62.5% 100%);
}

.launch-glow {
  position: absolute;
  inset: 0.5rem;
  border: 1px solid rgba(212,135,94,0.12);
  border-radius: 22px;
  pointer-events: none;
  box-shadow: inset 0 0 34px rgba(212,135,94,0.055), 0 0 30px rgba(212,135,94,0.075);
  animation: launchBreath 4.2s cubic-bezier(0.65, 0, 0.35, 1) infinite alternate;
}

.launch-core {
  position: relative;
  z-index: 2;
  width: 4.75rem;
  height: 4.75rem;
  display: grid;
  place-items: center;
  flex: 0 0 auto;
  border-radius: 50%;
  color: var(--bg);
  background:
    radial-gradient(circle at 35% 30%, rgba(255, 230, 210, 0.9), transparent 1.4rem),
    linear-gradient(135deg, #e1a17b, var(--accent));
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.4),
    inset 0 -12px 22px rgba(98,45,20,0.2),
    0 16px 36px rgba(0,0,0,0.32),
    0 0 36px rgba(212,135,94,0.24);
}

.launch-copy {
  position: relative;
  z-index: 2;
  display: grid;
  text-align: left;
  line-height: 1.08;
}

.launch-copy strong {
  font-size: clamp(1.15rem, 2vw, 1.55rem);
  letter-spacing: 0;
}

.launch-copy small {
  margin-top: 0.42rem;
  color: var(--text-secondary);
  font-size: 0.8rem;
}

.launch-ports {
  position: absolute;
  z-index: 3;
  right: 1rem;
  bottom: 0.9rem;
  display: flex;
  align-items: center;
}

.launch-port {
  width: 2.08rem;
  height: 2.08rem;
  display: grid;
  place-items: center;
  margin-left: -0.42rem;
  border: 1px solid rgba(255,255,255,0.075);
  border-radius: 50%;
  color: var(--accent);
  background: rgba(12,10,8,0.8);
  box-shadow: 0 10px 24px rgba(0,0,0,0.26), inset 0 1px 0 rgba(255,255,255,0.045);
  transition:
    margin-left 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    color 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.launch-port:first-child {
  margin-left: 0;
}

.launch-control:hover {
  border-color: rgba(212,135,94,0.56);
  box-shadow:
    0 34px 104px rgba(0, 0, 0, 0.48),
    0 22px 58px rgba(212, 135, 94, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.08),
    inset 0 -24px 42px rgba(0, 0, 0, 0.2);
}

.launch-control:hover .launch-port {
  margin-left: 0.28rem;
  color: #e1a17b;
  border-color: rgba(212,135,94,0.24);
  transform: translateY(-0.18rem);
}

.launch-control:active {
  transform: translateY(2px) scale(0.985);
}

.media-stack {
  position: relative;
  min-height: 620px;
  opacity: 0;
  animation: homeVisualIn 1.05s cubic-bezier(0.16, 1, 0.3, 1) 0.18s forwards;
}

.preview-frame {
  position: absolute;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  background:
    linear-gradient(145deg, rgba(42, 36, 30, 0.68), rgba(13, 12, 10, 0.82)),
    rgba(0, 0, 0, 0.24);
  box-shadow: 0 32px 120px rgba(0, 0, 0, 0.45);
}

.hero-visual {
  height: 100%;
  min-height: 100%;
  border-radius: inherit;
  transition:
    transform 0.9s cubic-bezier(0.16, 1, 0.3, 1),
    filter 0.9s cubic-bezier(0.16, 1, 0.3, 1);
}

.media-stack:hover .hero-visual {
  transform: scale(1.035);
  filter: brightness(1.08);
}

.preview-frame--main {
  inset: 2rem 0 4rem 4rem;
  z-index: 1;
}

.preview-frame--float {
  width: 42%;
  height: 32%;
  left: 0;
  bottom: 0.6rem;
  z-index: 2;
  transform: rotate(-4deg);
}

.frame-ui {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  gap: 0.35rem;
}

.frame-ui span {
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  background: rgba(240, 235, 228, 0.32);
}

.frame-caption {
  position: absolute;
  left: 1rem;
  right: 1rem;
  bottom: 1rem;
  display: flex;
  align-items: end;
  justify-content: space-between;
  padding-top: 6rem;
  background: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.72));
}

.frame-caption strong {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: 0.86rem;
}

.frame-caption small {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.72rem;
}

.wave-lines {
  position: absolute;
  inset: auto 1rem 1rem;
  height: 74px;
  display: flex;
  align-items: end;
  gap: 0.25rem;
}

.wave-lines span {
  flex: 1;
  border-radius: 999px;
  background: rgba(212, 135, 94, 0.68);
  animation: waveLift 1.8s cubic-bezier(0.65, 0, 0.35, 1) infinite alternate;
}

.wave-lines span:nth-child(3n) {
  animation-delay: 0.18s;
}

.wave-lines span:nth-child(4n) {
  animation-delay: 0.36s;
}

.process-chip {
  position: absolute;
  z-index: 3;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  min-height: 2.5rem;
  padding: 0 0.85rem;
  border-radius: 12px;
  color: var(--text-primary);
  border: 1px solid rgba(212, 135, 94, 0.22);
  background:
    linear-gradient(135deg, rgba(212, 135, 94, 0.2), rgba(212, 135, 94, 0.04)),
    rgba(12, 10, 8, 0.74);
  backdrop-filter: blur(18px);
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.34);
}

.chip-a {
  top: 6%;
  right: 12%;
}

.chip-b {
  right: 2%;
  bottom: 22%;
}

.flow-section,
.details-band {
  padding: clamp(2rem, 5vw, 5rem);
}

.flow-section {
  position: relative;
  isolation: isolate;
  min-height: 120vh;
  scroll-margin-top: 5.2rem;
  transition: filter 0.42s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-section::before {
  content: '';
  position: absolute;
  inset: -5rem 0 auto;
  z-index: -1;
  height: 32rem;
  pointer-events: none;
  opacity: 0.48;
  background:
    linear-gradient(102deg, transparent 0 18%, rgba(212,135,94,0.075) 18% 42%, transparent 42% 100%),
    radial-gradient(circle at 9% 34%, rgba(212,135,94,0.11), transparent 19rem);
}

.flow-section--focus .flow-head,
.flow-section--focus .flow-node {
  animation: focusLift 0.95s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-section--focus .flow-node {
  border-color: rgba(212, 135, 94, 0.42);
  box-shadow: 0 28px 96px rgba(0, 0, 0, 0.42), 0 0 0 1px rgba(212,135,94,0.1);
}

.flow-layout {
  display: grid;
  grid-template-columns: minmax(360px, 44vw) minmax(520px, 1fr);
  gap: clamp(1.1rem, 3.2vw, 3.6rem);
  align-items: start;
}

.flow-visual {
  position: sticky;
  top: 5rem;
  min-height: 620px;
  padding-top: clamp(0rem, 2vw, 1.4rem);
}

.visual-window {
  position: relative;
  min-height: 560px;
  overflow: hidden;
  border-radius: 22px;
  border: 1px solid rgba(255, 255, 255, 0.075);
  background:
    radial-gradient(circle at 22% 14%, rgba(212, 135, 94, 0.13), transparent 18rem),
    linear-gradient(145deg, rgba(42, 36, 30, 0.72), rgba(13, 12, 10, 0.82));
  box-shadow: 0 32px 120px rgba(0, 0, 0, 0.42);
  transform:
    translateY(var(--flow-window-shift))
    rotate(var(--flow-window-tilt));
  transform-origin: 42% 30%;
}

.visual-window::before {
  content: '';
  position: absolute;
  inset: 0.7rem;
  z-index: 3;
  pointer-events: none;
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 17px;
  box-shadow:
    inset 0 0 0 1px rgba(212,135,94,0.045),
    inset 0 -38px 80px rgba(0,0,0,0.2);
}

.visual-window img {
  width: 100%;
  height: 620px;
  display: block;
  object-fit: cover;
  object-position: 56% center;
  filter: saturate(0.72) brightness(0.72);
  transform: scale(var(--flow-image-scale));
}

.visual-window::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(0, 0, 0, 0.08), rgba(0, 0, 0, 0.72)),
    radial-gradient(circle at 72% 24%, rgba(212, 135, 94, 0.15), transparent 14rem);
}

.lab-topbar {
  position: absolute;
  z-index: 5;
  top: 1rem;
  left: 1rem;
  right: 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 2.7rem;
  padding: 0 0.9rem;
  border: 1px solid rgba(255, 255, 255, 0.075);
  border-radius: 14px;
  color: var(--text-tertiary);
  background: rgba(9, 8, 7, 0.58);
  backdrop-filter: blur(16px);
  font-family: var(--font-mono);
  font-size: 0.68rem;
}

.lab-topbar b {
  color: var(--accent);
  font-weight: 600;
}

.visual-scan {
  position: absolute;
  z-index: 4;
  left: 1.4rem;
  right: 1.4rem;
  top: 24%;
  height: 1px;
  pointer-events: none;
  opacity: 0.5;
  background: linear-gradient(90deg, transparent, rgba(212,135,94,0.78), transparent);
  box-shadow: 0 0 22px rgba(212,135,94,0.32);
  animation: scanLine 4.8s cubic-bezier(0.65, 0, 0.35, 1) infinite alternate;
}

.visual-grid {
  position: absolute;
  inset: 1rem;
  z-index: 2;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.45rem;
  opacity: var(--flow-grid-opacity);
  transform: translateY(var(--flow-grid-shift));
}

.visual-grid span {
  min-height: 42px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.06);
  background: rgba(255, 255, 255, 0.028);
}

.lab-chip {
  position: absolute;
  z-index: 5;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.18rem 0.5rem;
  align-items: center;
  min-width: 11.4rem;
  padding: 0.72rem 0.82rem;
  border: 1px solid rgba(255, 255, 255, 0.075);
  border-radius: 14px;
  color: var(--text-primary);
  background:
    radial-gradient(circle at 14% 18%, rgba(212,135,94,0.14), transparent 5.5rem),
    rgba(9, 8, 7, 0.6);
  backdrop-filter: blur(16px);
  box-shadow: 0 18px 48px rgba(0,0,0,0.28);
}

.lab-chip svg {
  grid-row: span 2;
  color: var(--accent);
}

.lab-chip span {
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
  line-height: 1;
}

.lab-chip strong {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.88rem;
  line-height: 1.1;
}

.lab-chip--format {
  left: 1.25rem;
  top: 5rem;
}

.lab-chip--queue {
  right: 1.25rem;
  bottom: 7.1rem;
  min-width: 9.6rem;
}

.visual-console {
  position: absolute;
  z-index: 3;
  left: 1rem;
  right: 1rem;
  bottom: 1rem;
  z-index: 5;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.35rem 0.65rem;
  align-items: center;
  padding: 1rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(10, 9, 8, 0.68);
  backdrop-filter: blur(18px);
}

.console-dot,
.panel-dot {
  width: 0.64rem;
  height: 0.64rem;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 20px rgba(212, 135, 94, 0.55);
}

.visual-console strong {
  color: var(--text-primary);
  font-size: 1rem;
}

.visual-console small {
  grid-column: 2;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.7rem;
}

.scroll-meter {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 0.75rem;
  align-items: center;
  margin-top: 1rem;
  color: var(--text-tertiary);
  font-family: var(--font-mono);
  font-size: 0.68rem;
}

.scroll-meter div {
  height: 2px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
}

.scroll-meter i {
  display: block;
  width: var(--flow-meter-width);
  height: 100%;
  border-radius: inherit;
  background: var(--accent);
}

.flow-content {
  padding-top: clamp(1.2rem, 5.4vw, 4.2rem);
  margin-left: clamp(-2.4rem, -2.4vw, -0.9rem);
}

.flow-head {
  max-width: 40rem;
  margin-bottom: 1.15rem;
  padding-left: clamp(0rem, 1.6vw, 1.1rem);
}

.flow-head h2,
.quick-panel h2 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: 3rem;
  font-weight: 820;
  line-height: 1.08;
  letter-spacing: 0;
  text-wrap: balance;
}

.flow-head p {
  margin-top: 0.8rem;
  color: var(--text-tertiary);
  font-size: 0.9rem;
  line-height: 1.7;
}

.flow-track {
  position: relative;
  display: grid;
  gap: 0.9rem;
}

.flow-track::before {
  content: '';
  position: absolute;
  top: 0.9rem;
  bottom: 0.9rem;
  left: 1.15rem;
  width: 1px;
  pointer-events: none;
  opacity: 0.38;
  background:
    linear-gradient(180deg, transparent, rgba(212,135,94,0.52), transparent),
    linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  transform: translateX(var(--flow-track-shift));
}

.flow-node {
  --node-x: 50%;
  --node-y: 50%;
  position: relative;
  isolation: isolate;
  min-height: 210px;
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr) 2rem;
  align-items: end;
  gap: 1.2rem;
  width: min(100%, 850px);
  padding: 1rem;
  border-radius: 18px;
  border: 1px solid rgba(255, 255, 255, 0.075);
  overflow: hidden;
  text-decoration: none;
  background:
    radial-gradient(circle at var(--node-x) var(--node-y), rgba(255, 226, 202, 0.16), transparent 12rem),
    radial-gradient(circle at 18% 10%, rgba(212, 135, 94, 0.12), transparent 16rem),
    linear-gradient(145deg, rgba(42, 36, 30, 0.74), rgba(13, 12, 10, 0.78));
  box-shadow: 0 20px 70px rgba(0, 0, 0, 0.28);
  transition:
    transform 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node--0 {
  margin-left: clamp(0rem, 1.5vw, 1rem);
}

.flow-node--1 {
  width: min(100%, 880px);
}

.flow-node--2 {
  margin-left: clamp(0rem, 3vw, 2rem);
}

.flow-action-stack {
  position: absolute;
  z-index: 4;
  top: 0.9rem;
  left: 12.6rem;
  width: 14rem;
  height: 7rem;
  pointer-events: none;
}

.flow-action-card {
  --bar-size: 60%;
  position: absolute;
  left: 0;
  top: 2.1rem;
  min-width: 11.2rem;
  min-height: 2.35rem;
  display: grid;
  grid-template-columns: 1rem minmax(0, 1fr) 2.5rem;
  align-items: center;
  gap: 0.5rem;
  padding: 0.48rem 0.62rem;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 999px;
  color: var(--text-secondary);
  opacity: 0;
  background:
    radial-gradient(circle at 18% 20%, rgba(212,135,94,0.16), transparent 5rem),
    linear-gradient(135deg, rgba(34,28,23,0.94), rgba(9,8,7,0.86));
  box-shadow:
    0 18px 44px rgba(0,0,0,0.34),
    inset 0 1px 0 rgba(255,255,255,0.045);
  transform: translateX(-0.3rem) translateY(0.2rem) scale(0.92);
  transition:
    opacity 0.36s cubic-bezier(0.16, 1, 0.3, 1),
    color 0.36s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.36s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.54s cubic-bezier(0.16, 1, 0.3, 1);
  transition-delay: calc(var(--action-index) * 0.045s);
}

.flow-action-card:nth-child(1) { --bar-size: 72%; }
.flow-action-card:nth-child(2) { --bar-size: 54%; }
.flow-action-card:nth-child(3) { --bar-size: 82%; }

.flow-action-card svg {
  color: var(--accent);
}

.flow-action-card b {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.72rem;
}

.flow-action-card i {
  display: block;
  height: 0.24rem;
  border-radius: 999px;
  background: rgba(255,255,255,0.07);
  overflow: hidden;
}

.flow-action-card i::before {
  content: '';
  display: block;
  width: var(--bar-size);
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, rgba(212,135,94,0.18), rgba(212,135,94,0.86));
  transform-origin: left center;
  transform: scaleX(0.42);
  transition: transform 0.54s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node:hover .flow-action-card,
.flow-section--focus .flow-action-card {
  opacity: 0.94;
  color: var(--text-primary);
  border-color: rgba(212,135,94,0.24);
}

.flow-node:hover .flow-action-card i::before,
.flow-section--focus .flow-action-card i::before {
  transform: scaleX(1);
}

.flow-node:hover .flow-action-card:nth-child(1),
.flow-section--focus .flow-action-card:nth-child(1) {
  transform: translate(0.2rem, -1.25rem) rotate(-3deg) scale(1);
}

.flow-node:hover .flow-action-card:nth-child(2),
.flow-section--focus .flow-action-card:nth-child(2) {
  transform: translate(1.75rem, 0.15rem) rotate(2deg) scale(1);
}

.flow-node:hover .flow-action-card:nth-child(3),
.flow-section--focus .flow-action-card:nth-child(3) {
  transform: translate(0.72rem, 1.58rem) rotate(-1deg) scale(1);
}

.flow-node::before {
  content: '';
  position: absolute;
  left: 1rem;
  right: 1rem;
  bottom: 0.8rem;
  height: 2px;
  pointer-events: none;
  opacity: 0.24;
  border-radius: 999px;
  background:
    linear-gradient(90deg, rgba(212,135,94,0), rgba(212,135,94,0.65), rgba(212,135,94,0.08)),
    rgba(255,255,255,0.04);
  transform: scaleX(0.18);
  transform-origin: left center;
  transition:
    opacity 0.36s cubic-bezier(0.16, 1, 0.3, 1),
    transform 0.54s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node::after {
  content: '';
  position: absolute;
  inset: 0.58rem;
  pointer-events: none;
  opacity: 0;
  border: 1px solid rgba(212,135,94,0.18);
  border-radius: 14px;
  box-shadow: inset 0 0 26px rgba(212,135,94,0.055);
  transition: opacity 0.32s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node[data-reveal] {
  transform: translateY(var(--node-lift)) translateX(var(--node-shift));
}

.flow-node[data-reveal].is-visible {
  transform: translateY(0) translateX(var(--node-shift));
}

.flow-node:hover {
  transform: translateY(-5px) translateX(calc(var(--node-shift) + 8px));
  border-color: rgba(212, 135, 94, 0.32);
  box-shadow: 0 30px 90px rgba(0, 0, 0, 0.38);
}

.flow-node:hover::before,
.flow-section--focus .flow-node::before {
  opacity: 0.82;
  transform: scaleX(0.86);
  animation: mediaTrackPulse 1.4s cubic-bezier(0.65, 0, 0.35, 1) infinite alternate;
}

.flow-node:hover::after {
  opacity: 1;
  border-color: rgba(212,135,94,0.3);
}

.flow-node-visual {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 180px;
  border-radius: 13px;
  transition: transform 0.72s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node:hover .flow-node-visual {
  transform: scale(1.05);
}

.flow-node-copy span {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
}

.flow-node-copy,
.flow-arrow {
  position: relative;
  z-index: 3;
}

.flow-node-copy h3 {
  margin-top: 0.35rem;
  color: var(--text-primary);
  font-size: 1.35rem;
}

.flow-node-copy p {
  margin-top: 0.35rem;
  color: var(--text-tertiary);
  font-size: 0.86rem;
  line-height: 1.6;
}

.flow-arrow {
  align-self: start;
  color: var(--accent);
  transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), color 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node:hover .flow-arrow {
  color: #e1a17b;
  transform: translate(4px, -4px);
}

.details-band {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(320px, 0.7fr);
  gap: 1rem;
  align-items: stretch;
}

.work-steps,
.quick-panel {
  border: 1px solid rgba(255, 255, 255, 0.065);
  border-radius: 18px;
  background:
    linear-gradient(145deg, rgba(42, 36, 30, 0.66), rgba(13, 12, 10, 0.72)),
    radial-gradient(circle at 12% 12%, rgba(212, 135, 94, 0.08), transparent 15rem);
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.24);
}

.work-steps {
  padding: 1rem;
}

.step-line {
  display: grid;
  grid-template-columns: 4rem 1fr;
  gap: 1rem;
  padding: 1.1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.055);
}

.step-line:last-child {
  border-bottom: 0;
}

.step-index {
  color: var(--accent);
  font-family: var(--font-mono);
  font-size: 0.82rem;
}

.step-line h3 {
  color: var(--text-primary);
  font-size: 1rem;
}

.step-line p,
.quick-panel p {
  margin-top: 0.25rem;
  color: var(--text-tertiary);
  font-size: 0.84rem;
  line-height: 1.65;
}

.quick-panel {
  position: relative;
  padding: 1.5rem;
  min-height: 310px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.panel-dot {
  position: absolute;
  top: 1.2rem;
  left: 1.2rem;
}

.panel-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 1rem;
}

.panel-tags span {
  padding: 0.42rem 0.62rem;
  border-radius: 999px;
  color: var(--text-secondary);
  border: 1px solid rgba(255, 255, 255, 0.07);
  background: rgba(255, 255, 255, 0.035);
  font-size: 0.74rem;
}

@keyframes waveLift {
  from {
    transform: scaleY(0.58);
    opacity: 0.55;
  }
  to {
    transform: scaleY(1);
    opacity: 0.95;
  }
}

@keyframes homeCopyIn {
  from {
    opacity: 0;
    transform: translateY(calc(-2vh + 26px));
    filter: brightness(0.82) blur(3px);
  }
  to {
    opacity: 1;
    transform: translateY(-2vh);
    filter: brightness(1) blur(0);
  }
}

@keyframes homeVisualIn {
  from {
    opacity: 0;
    transform: translateX(34px) scale(0.98);
    filter: brightness(0.72) blur(4px);
  }
  to {
    opacity: 1;
    transform: translateX(0) scale(1);
    filter: brightness(1) blur(0);
  }
}

@keyframes mediaTrackPulse {
  from {
    filter: brightness(0.82);
  }
  to {
    filter: brightness(1.18);
  }
}

@keyframes scanLine {
  from {
    opacity: 0.22;
    transform: translateY(-18px) scaleX(0.42);
  }
  to {
    opacity: 0.72;
    transform: translateY(180px) scaleX(1);
  }
}

@keyframes launchBorder {
  from {
    background-position: 0% 40%;
    opacity: 0.36;
  }
  to {
    background-position: 100% 60%;
    opacity: 0.72;
  }
}

@keyframes launchBreath {
  from {
    opacity: 0.52;
    box-shadow: inset 0 0 20px rgba(212,135,94,0.04), 0 0 18px rgba(212,135,94,0.05);
  }
  to {
    opacity: 0.92;
    box-shadow: inset 0 0 34px rgba(212,135,94,0.075), 0 0 34px rgba(212,135,94,0.11);
  }
}

@keyframes focusLift {
  0% {
    transform: translateY(18px) scale(0.985);
    filter: brightness(0.85);
  }
  60% {
    transform: translateY(-4px) scale(1.01);
    filter: brightness(1.12);
  }
  100% {
    transform: translateY(0) scale(1);
    filter: brightness(1);
  }
}

@media (max-width: 1180px) {
  .stage-copy h1 {
    font-size: 5.6rem;
  }

  .flow-layout {
    grid-template-columns: minmax(320px, 0.78fr) minmax(0, 1fr);
    gap: 1.5rem;
  }

  .flow-content {
    margin-left: -0.7rem;
  }

  .flow-node {
    grid-template-columns: 220px minmax(0, 1fr) 2rem;
  }

  .flow-node--0,
  .flow-node--2 {
    margin-left: 0;
  }
}

@media (max-width: 980px) {
  .entry-stage,
  .flow-layout,
  .details-band {
    grid-template-columns: 1fr;
  }

  .media-stack {
    min-height: 480px;
  }

  .preview-frame--main {
    inset: 0 0 4rem 2rem;
  }

  .flow-section {
    min-height: auto;
  }

  .flow-visual {
    position: relative;
    top: auto;
    min-height: auto;
    padding-top: 0;
  }

  .visual-window {
    min-height: 420px;
  }

  .visual-window img {
    height: 480px;
  }

  .lab-chip--queue {
    bottom: 6.6rem;
  }

  .flow-node,
  .flow-node[data-reveal],
  .flow-node[data-reveal].is-visible,
  .flow-node:hover {
    width: 100%;
    margin-left: 0;
    transform: translateY(0) translateX(0);
  }

  .flow-content {
    margin-left: 0;
    padding-top: 0;
  }

  .flow-head {
    padding-left: 0;
  }

  .flow-action-stack {
    display: none;
  }
}

@media (max-width: 680px) {
  .home {
    overflow-x: hidden;
  }

  .entry-stage,
  .flow-section,
  .details-band {
    padding: 1.1rem;
  }

  .entry-stage {
    min-height: auto;
    gap: 1.35rem;
    align-items: start;
    padding-top: 1.35rem;
  }

  .stage-copy {
    max-width: 100%;
    transform: none;
    opacity: 1;
    animation: none;
  }

  .stage-copy h1 {
    max-width: 10ch;
    font-size: 4.15rem;
    line-height: 0.94;
  }

  .stage-copy p {
    max-width: 100%;
    font-size: 0.95rem;
    line-height: 1.68;
    overflow-wrap: anywhere;
  }

  .stage-actions {
    margin-top: 1.45rem;
  }

  .launch-control {
    width: 100%;
    min-width: 0;
    min-height: 5.8rem;
    padding: 0.72rem 5.25rem 0.72rem 0.72rem;
    border-radius: 22px;
  }

  .login-control {
    width: 100%;
    justify-content: center;
    min-height: 3.1rem;
  }

  .launch-control::before,
  .launch-glow {
    inset: 0.42rem;
    border-radius: 18px;
  }

  .launch-core {
    width: 4rem;
    height: 4rem;
  }

  .launch-copy strong {
    font-size: 1.08rem;
  }

  .launch-copy small {
    font-size: 0.72rem;
  }

  .launch-ports {
    right: 0.75rem;
    bottom: 0.75rem;
  }

  .launch-port {
    width: 1.82rem;
    height: 1.82rem;
    margin-left: -0.58rem;
  }

  .media-stack {
    min-height: 330px;
    width: 100%;
    overflow: hidden;
  }

  .preview-frame--main {
    inset: 0 0 3rem 0;
  }

  .preview-frame--float {
    width: 58%;
  }

  .chip-b {
    right: 0;
    bottom: 12%;
  }

  .process-chip {
    min-height: 2.35rem;
    padding: 0 0.72rem;
    font-size: 0.72rem;
  }

  .flow-section {
    scroll-margin-top: 4.1rem;
  }

  .visual-window {
    min-height: 340px;
    border-radius: 18px;
  }

  .visual-window img {
    height: 390px;
  }

  .flow-node {
    grid-template-columns: 1fr;
    min-height: auto;
    padding: 0.85rem;
    border-radius: 16px;
  }

  .flow-node-visual {
    height: 170px;
  }

  .flow-node-copy {
    min-width: 0;
  }

  .flow-node-copy h3,
  .flow-node-copy p {
    overflow-wrap: anywhere;
  }

  .lab-topbar {
    min-height: 2.35rem;
    font-size: 0.62rem;
  }

  .lab-chip {
    min-width: 9.2rem;
    padding: 0.62rem 0.68rem;
  }

  .lab-chip--format {
    left: 0.9rem;
    top: 4.35rem;
  }

  .lab-chip--queue {
    right: 0.9rem;
    bottom: 6rem;
  }

  .flow-arrow {
    position: absolute;
    top: 1rem;
    right: 1rem;
  }

  .details-band {
    gap: 0.85rem;
  }

  .step-line {
    grid-template-columns: 2.6rem minmax(0, 1fr);
    gap: 0.75rem;
    padding: 0.9rem;
  }

  .quick-panel {
    min-height: 240px;
    padding: 1.15rem;
  }

  .panel-tags span {
    min-height: 2.35rem;
    display: inline-flex;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .entry-stage,
  .flow-section,
  .details-band {
    padding-inline: 0.82rem;
  }

  .kicker,
  .flow-head span {
    font-size: 0.64rem;
  }

  .stage-copy h1 {
    font-size: 3.45rem;
  }

  .launch-control {
    min-height: 5.25rem;
    gap: 0.72rem;
    padding-right: 4.7rem;
  }

  .launch-core {
    width: 3.55rem;
    height: 3.55rem;
  }

  .launch-copy {
    min-width: 0;
  }

  .launch-copy strong,
  .launch-copy small {
    overflow-wrap: anywhere;
  }

  .media-stack {
    min-height: 292px;
  }

  .preview-frame--float,
  .process-chip {
    display: none;
  }

  .visual-window {
    min-height: 300px;
  }

  .visual-window img {
    height: 340px;
  }

  .lab-chip {
    max-width: calc(100% - 1.8rem);
  }

  .lab-chip--queue {
    left: 0.9rem;
    right: auto;
  }

  .flow-head h2,
  .quick-panel h2 {
    font-size: 2.15rem;
  }

  .flow-node-visual {
    height: 150px;
  }

  .step-line {
    grid-template-columns: 1fr;
  }
}
</style>
