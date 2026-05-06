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
            <img src="https://picsum.photos/seed/vlade-left-lab/760/940" alt="" />
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
              :style="{ '--node-shift': `${index * 8}px`, '--node-lift': `${32 + index * 10}px` }"
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
          <span>{{ copy.noSignup }}</span>
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
import { gsap } from 'gsap'
import AppFooter from '../components/AppFooter.vue'
import MediaVisual from '../components/MediaVisual.vue'
import { suiteList } from '../data/toolSuites.js'

const copy = {
  workbench: '\u5a92\u4f53\u5de5\u4f5c\u53f0',
  heroTitle: '\u5904\u7406\u5a92\u4f53\uff0c\u5c11\u7ed5\u8def\u3002',
  heroText: '\u4e0a\u4f20\u6587\u4ef6\uff0c\u9009\u62e9\u64cd\u4f5c\uff0c\u5b8c\u6210\u540e\u4e0b\u8f7d\u3002\u89c6\u9891\u3001\u56fe\u7247\u3001\u97f3\u9891\u90fd\u5728\u4e00\u4e2a\u754c\u9762\u91cc\u3002',
  start: '\u5f00\u59cb\u4f7f\u7528',
  choose: '\u9009\u62e9\u4f60\u7684\u5a92\u4f53\u5de5\u4f5c\u53f0',
  video: '\u89c6\u9891',
  image: '\u56fe\u7247',
  audio: '\u97f3\u9891',
  cut: '\u88c1\u526a',
  convert: '\u8f6c\u6362',
  ready: '\u5df2\u5c31\u7eea',
  pickWorkbench: '\u9009\u62e9\u4e00\u4e2a\u5de5\u4f5c\u53f0',
  entry: '\u9009\u62e9\u5165\u53e3',
  flowTitle: '\u540c\u4e00\u5957\u5de5\u4f5c\u53f0\uff0c\u4e09\u79cd\u6587\u4ef6\u3002',
  flowText: '\u53f3\u8fb9\u9009\u5165\u53e3\uff0c\u8fdb\u53bb\u4e4b\u540e\u5e03\u5c40\u4e0d\u4f1a\u53d8\u3002\u53ea\u6362\u5de5\u5177\u3001\u53c2\u6570\u548c\u63d0\u793a\u3002',
  quickTitle: '\u5c11\u70b9\u7b49\u5f85\uff0c\u591a\u70b9\u786e\u5b9a\u3002',
  quickText: '\u754c\u9762\u53ea\u663e\u793a\u5f53\u524d\u5de5\u5177\u9700\u8981\u7684\u9009\u9879\uff0c\u5b8c\u6210\u540e\u76f4\u63a5\u4fdd\u5b58\u3002',
  noSignup: '\u65e0\u9700\u6ce8\u518c',
  browserUpload: '\u6d4f\u89c8\u5668\u4e0a\u4f20',
  download: '\u7ed3\u679c\u4e0b\u8f7d',
}

const displayCopy = {
  video: {
    title: '\u89c6\u9891\u5904\u7406',
    eyebrow: 'VIDEO',
    intro: '\u538b\u7f29\u3001\u8f6c\u6362\u3001\u88c1\u526a\u3001\u5408\u5e76\uff0c\u4e0a\u4f20\u540e\u76f4\u63a5\u5904\u7406\u3002',
    featuredTools: [
      { title: '\u88c1\u526a', icon: 'ph:scissors' },
      { title: '\u8f6c\u6362', icon: 'ph:arrows-left-right' },
      { title: '\u538b\u7f29', icon: 'ph:arrows-in-line-vertical' },
    ],
  },
  image: {
    title: '\u56fe\u7247\u5904\u7406',
    eyebrow: 'IMAGE',
    intro: '\u538b\u7f29\u3001\u8f6c\u6362\u3001\u88c1\u526a\u3001\u6539\u5c3a\u5bf8\uff0c\u5e38\u7528\u64cd\u4f5c\u653e\u5728\u4e00\u8d77\u3002',
    featuredTools: [
      { title: '\u88c1\u526a', icon: 'ph:crop' },
      { title: '\u538b\u7f29', icon: 'ph:image-square' },
      { title: '\u6c34\u5370', icon: 'ph:text-t' },
    ],
  },
  audio: {
    title: '\u97f3\u9891\u5904\u7406',
    eyebrow: 'AUDIO',
    intro: '\u538b\u7f29\u3001\u8f6c\u6362\u3001\u526a\u5207\u3001\u5408\u5e76\u3001\u8c03\u97f3\u91cf\u3002',
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
      revealObserver: null,
      scrollRaf: 0,
      steps: [
        { index: '01', title: '\u9009\u6587\u4ef6', text: '\u62d6\u8fdb\u4e0a\u4f20\u533a\uff0c\u6216\u4ece\u672c\u5730\u9009\u62e9\u3002' },
        { index: '02', title: '\u8c03\u53c2\u6570', text: '\u53ea\u770b\u5f53\u524d\u5de5\u5177\u4f1a\u7528\u5230\u7684\u8bbe\u7f6e\u3002' },
        { index: '03', title: '\u62ff\u7ed3\u679c', text: '\u5904\u7406\u5b8c\u6210\u540e\u4fdd\u5b58\u5230\u672c\u5730\u3002' },
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
        '--flow-window-shift': `${progress * -12}px`,
        '--flow-window-tilt': `${(progress - 0.5) * -1.6}deg`,
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
    initLaunchMotion() {
      if (this.launchMotion || !this.$refs.launchButton || !window.matchMedia('(pointer: fine)').matches) return
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
  font-size: clamp(3.5rem, 9vw, 8.6rem);
  line-height: 0.9;
  max-width: 9ch;
}

.stage-copy p {
  max-width: 30rem;
  margin-top: 1.25rem;
  color: var(--text-secondary);
  font-size: clamp(1rem, 1.6vw, 1.18rem);
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
  min-height: 108vh;
  padding-top: clamp(3rem, 7vw, 7rem);
  padding-bottom: clamp(3rem, 7vw, 7rem);
  scroll-margin-top: 5.2rem;
  transition: filter 0.42s cubic-bezier(0.16, 1, 0.3, 1);
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
  position: relative;
  display: grid;
  grid-template-columns: minmax(300px, 0.52fr) minmax(0, 1fr);
  gap: clamp(1.4rem, 3.2vw, 3.25rem);
  align-items: start;
  max-width: 1500px;
  margin: 0 auto;
}

.flow-layout::before {
  content: '';
  position: absolute;
  inset: -2.5rem -1.5rem -2rem;
  z-index: -1;
  pointer-events: none;
  opacity: 0.62;
  background:
    radial-gradient(circle at 33% 22%, rgba(212,135,94,0.13), transparent 21rem),
    linear-gradient(115deg, rgba(255,255,255,0.025), transparent 42%);
}

.flow-visual {
  position: sticky;
  top: 5.2rem;
  min-height: 540px;
  padding-top: clamp(2.4rem, 4vw, 4.3rem);
}

.visual-window {
  position: relative;
  min-height: clamp(430px, 54vw, 560px);
  overflow: hidden;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.075);
  background:
    radial-gradient(circle at 22% 14%, rgba(212, 135, 94, 0.13), transparent 18rem),
    linear-gradient(145deg, rgba(42, 36, 30, 0.72), rgba(13, 12, 10, 0.82));
  box-shadow: 0 32px 120px rgba(0, 0, 0, 0.42);
  transform:
    translateY(var(--flow-window-shift))
    rotate(var(--flow-window-tilt));
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
  height: clamp(470px, 58vw, 620px);
  display: block;
  object-fit: cover;
  object-position: 52% center;
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
  top: 0.9rem;
  left: 0.9rem;
  right: 0.9rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 2.7rem;
  padding: 0 0.9rem;
  border: 1px solid rgba(255, 255, 255, 0.075);
  border-radius: 13px;
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
  inset: 0.9rem;
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
  min-width: 9.8rem;
  padding: 0.66rem 0.74rem;
  border: 1px solid rgba(255, 255, 255, 0.075);
  border-radius: 13px;
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
  left: 1.05rem;
  top: 4.7rem;
}

.lab-chip--queue {
  right: 1.05rem;
  bottom: 6.55rem;
  min-width: 8.7rem;
}

.visual-console {
  position: absolute;
  z-index: 5;
  left: 0.9rem;
  right: 0.9rem;
  bottom: 0.9rem;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 0.35rem 0.65rem;
  align-items: center;
  padding: 1rem;
  border-radius: 15px;
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
  padding-top: clamp(0.6rem, 2.2vw, 1.9rem);
}

.flow-head {
  max-width: 46rem;
  margin: 0 0 1.25rem clamp(0.45rem, 2.2vw, 2rem);
}

.flow-head h2,
.quick-panel h2 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 4vw, 3.3rem);
  line-height: 1.05;
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
  padding-left: clamp(0rem, 1vw, 0.7rem);
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
  min-height: 192px;
  display: grid;
  grid-template-columns: clamp(190px, 24vw, 248px) minmax(0, 1fr) 2rem;
  align-items: end;
  gap: clamp(0.9rem, 1.8vw, 1.15rem);
  width: min(100%, 820px);
  padding: 0.86rem;
  border-radius: 17px;
  border: 1px solid rgba(255, 255, 255, 0.075);
  overflow: hidden;
  text-decoration: none;
  background:
    radial-gradient(circle at var(--node-x) var(--node-y), rgba(255, 226, 202, 0.16), transparent 12rem),
    radial-gradient(circle at 18% 10%, rgba(212, 135, 94, 0.12), transparent 16rem),
    linear-gradient(145deg, rgba(42, 36, 30, 0.74), rgba(13, 12, 10, 0.78));
  box-shadow: 0 18px 64px rgba(0, 0, 0, 0.28);
  transition:
    transform 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    border-color 0.32s cubic-bezier(0.16, 1, 0.3, 1),
    box-shadow 0.32s cubic-bezier(0.16, 1, 0.3, 1);
}

.flow-node--0 {
  margin-left: clamp(0rem, 1.6vw, 1.2rem);
}

.flow-node--1 {
  width: min(100%, 850px);
}

.flow-node--2 {
  width: min(100%, 790px);
  margin-left: clamp(0rem, 2.8vw, 2.1rem);
}

.flow-action-stack {
  position: absolute;
  z-index: 4;
  top: 0.72rem;
  left: clamp(9.8rem, 20vw, 12.1rem);
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
  transform: translate(0.15rem, -1.1rem) rotate(-3deg) scale(1);
}

.flow-node:hover .flow-action-card:nth-child(2),
.flow-section--focus .flow-action-card:nth-child(2) {
  transform: translate(1.45rem, 0.12rem) rotate(2deg) scale(1);
}

.flow-node:hover .flow-action-card:nth-child(3),
.flow-section--focus .flow-action-card:nth-child(3) {
  transform: translate(0.62rem, 1.42rem) rotate(-1deg) scale(1);
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
  height: 166px;
  border-radius: 12px;
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
  font-size: clamp(1.12rem, 1.7vw, 1.34rem);
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
    padding-top: 2rem;
    padding-bottom: 2.5rem;
  }

  .flow-visual {
    position: relative;
    top: auto;
    min-height: auto;
    padding-top: 0;
  }

  .visual-window {
    min-height: 420px;
    transform: none;
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
    padding-top: 0;
  }

  .flow-head {
    margin-left: 0;
  }

  .flow-action-stack {
    display: none;
  }
}

@media (max-width: 680px) {
  .entry-stage,
  .flow-section,
  .details-band {
    padding: 1.25rem;
  }

  .entry-stage {
    min-height: auto;
  }

  .stage-copy h1 {
    font-size: clamp(3rem, 18vw, 5rem);
  }

  .launch-control {
    width: 100%;
    min-width: 0;
    min-height: 5.8rem;
    padding: 0.72rem 5.25rem 0.72rem 0.72rem;
    border-radius: 22px;
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
    min-height: 360px;
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

  .flow-node {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .flow-node-visual {
    height: 170px;
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
}
</style>
