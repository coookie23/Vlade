<template>
  <!-- Hidden video loader, always mounted when file is set -->
  <video
    v-show="false"
    ref="loader"
    :src="videoUrl"
    @loadedmetadata="onMeta"
    @error="onVideoError"
  />

  <div v-if="videoLoaded" class="trimmer">
    <!-- Preview -->
    <div class="preview-frame">
      <video ref="preview" :src="videoUrl" class="preview-video" />
      <div class="preview-overlay">
        <span class="timecode">{{ formatTime(currentTime) }}</span>
      </div>
    </div>

    <!-- Range info -->
    <div class="range-info">
      <div class="range-value">
        <span class="range-label">起始</span>
        <span class="range-time">{{ formatTime(startTime) }}</span>
      </div>
      <span class="range-duration">选中 {{ formatTime(endTime - startTime) }}</span>
      <div class="range-value right">
        <span class="range-label">结束</span>
        <span class="range-time">{{ formatTime(endTime) }}</span>
      </div>
    </div>

    <!-- Filmstrip track -->
    <div class="track-wrapper">
      <div class="track-bar" ref="track" @mousedown="onTrackClick">
        <canvas ref="filmstrip" class="filmstrip-canvas" />
        <div class="track-mask left" :style="{ width: leftPercent + '%' }" />
        <div class="track-mask right" :style="{ width: (100 - rightPercent) + '%' }" />
        <div class="track-selection" :style="{ left: leftPercent + '%', width: (rightPercent - leftPercent) + '%' }">
          <div class="selection-glow" />
        </div>
        <div class="track-handle left-handle" :style="{ left: leftPercent + '%' }" @mousedown.prevent="onHandleDrag($event, 'start')">
          <div class="handle-grip" />
        </div>
        <div class="track-handle right-handle" :style="{ left: rightPercent + '%' }" @mousedown.prevent="onHandleDrag($event, 'end')">
          <div class="handle-grip" />
        </div>
      </div>
    </div>
  </div>

  <div v-else-if="videoUrl" class="trimmer-loading">
    <div class="spinner" />
    <p>正在加载视频...</p>
  </div>

  <div v-else class="trimmer-empty">
    <p class="trim-hint">上传视频后即可可视化裁剪</p>
  </div>
</template>

<script>
export default {
  name: 'VideoTrimmer',
  props: {
    file: { type: File, required: true },
  },
  emits: ['update:start', 'update:end'],
  data() {
    return {
      videoUrl: '',
      videoLoaded: false,
      duration: 0,
      startTime: 0,
      endTime: 0,
      currentTime: 0,
      dragging: null,
      thumbCount: 20,
    }
  },
  computed: {
    leftPercent() { return (this.startTime / this.duration) * 100 },
    rightPercent() { return (this.endTime / this.duration) * 100 },
  },
  watch: {
    startTime(v) { this.$emit('update:start', v) },
    endTime(v) { this.$emit('update:end', v) },
    file: {
      immediate: true,
      handler(f) {
        if (!f) return
        if (this.videoUrl) URL.revokeObjectURL(this.videoUrl)
        this.videoLoaded = false
        this.videoUrl = URL.createObjectURL(f)
      },
    },
  },
  mounted() {
    window.addEventListener('mousemove', this.onMouseMove)
    window.addEventListener('mouseup', this.onMouseUp)
  },
  beforeUnmount() {
    URL.revokeObjectURL(this.videoUrl)
    window.removeEventListener('mousemove', this.onMouseMove)
    window.removeEventListener('mouseup', this.onMouseUp)
  },
  methods: {
    onVideoError(e) {
      console.error('Video load error:', e)
    },
    async onMeta() {
      const v = this.$refs.loader
      if (!v) return
      this.duration = v.duration
      this.endTime = Math.min(30, v.duration)
      this.currentTime = 0
      this.videoLoaded = true
      await this.$nextTick()
      await this.$nextTick()
      this.generateFilmstrip()
    },
    async generateFilmstrip() {
      const canvas = this.$refs.filmstrip
      if (!canvas) return
      const trackEl = this.$refs.track
      const w = trackEl.offsetWidth
      const h = 56
      const dpr = window.devicePixelRatio || 1
      canvas.width = w * dpr
      canvas.height = h * dpr
      canvas.style.width = w + 'px'
      canvas.style.height = h + 'px'
      const ctx = canvas.getContext('2d')
      ctx.scale(dpr, dpr)

      const v = document.createElement('video')
      v.src = this.videoUrl
      v.muted = true
      v.preload = 'metadata'
      v.crossOrigin = 'anonymous'

      await new Promise((resolve) => { v.onloadedmetadata = () => { v.currentTime = 0; resolve() } })

      const count = this.thumbCount
      const stepW = w / count
      for (let i = 0; i < count; i++) {
        const t = (i / count) * this.duration
        v.currentTime = Math.min(t, this.duration - 0.1)
        await new Promise((resolve) => { v.onseeked = resolve })
        ctx.drawImage(v, i * stepW, 0, stepW, h)
      }
    },
    formatTime(s) {
      const m = Math.floor(s / 60)
      const sec = s % 60
      return `${String(m).padStart(2, '0')}:${sec.toFixed(1).padStart(4, '0')}`
    },
    // Handles
    onHandleDrag(e, which) {
      this.dragging = which
      this.updateFromMouse(e)
    },
    onTrackClick(e) {
      const rect = this.$refs.track.getBoundingClientRect()
      const pct = (e.clientX - rect.left) / rect.width
      const t = pct * this.duration
      this.currentTime = Math.max(0, Math.min(this.duration, t))
      const pv = this.$refs.preview
      if (pv) pv.currentTime = this.currentTime
    },
    onMouseMove(e) {
      if (!this.dragging) return
      this.updateFromMouse(e)
    },
    onMouseUp() {
      this.dragging = null
    },
    updateFromMouse(e) {
      const rect = this.$refs.track.getBoundingClientRect()
      const pct = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width))
      const t = pct * this.duration
      if (this.dragging === 'start') {
        this.startTime = Math.max(0, Math.min(this.endTime - 0.5, t))
        this.currentTime = this.startTime
      } else {
        this.endTime = Math.min(this.duration, Math.max(this.startTime + 0.5, t))
        this.currentTime = this.endTime
      }
      const pv = this.$refs.preview
      if (pv) pv.currentTime = this.currentTime
    },
  },
}
</script>

<style scoped>
.trimmer { display: flex; flex-direction: column; gap: 1rem; }

/* Preview */
.preview-frame {
  position: relative;
  border-radius: 1rem;
  overflow: hidden;
  background: #0f172a;
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 4px 24px rgba(0,0,0,0.2);
  aspect-ratio: 16 / 9;
  max-height: 360px;
}

.preview-video {
  width: 100%; height: 100%; object-fit: contain; display: block;
}

.preview-overlay {
  position: absolute; bottom: 0; left: 0; right: 0;
  padding: 0.75rem 1rem;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  display: flex; justify-content: flex-end;
}

.timecode {
  font-family: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
  font-size: 0.8125rem; color: rgba(255,255,255,0.8);
  background: rgba(0,0,0,0.4); padding: 0.25rem 0.5rem; border-radius: 0.25rem;
}

/* Range info */
.range-info { display: flex; align-items: center; justify-content: space-between; }
.range-value { display: flex; flex-direction: column; }
.range-value.right { text-align: right; }
.range-label { font-size: 0.625rem; text-transform: uppercase; letter-spacing: 0.06em; color: #94a3b8; }
.range-time { font-family: var(--font-mono); font-size: 0.9375rem; font-weight: 600; color: var(--text-primary); }
.range-duration { font-size: 0.75rem; color: var(--accent); font-weight: 500; padding: 0.125rem 0.625rem; background: rgba(212,135,94,0.08); border-radius: 0.375rem; }

/* Track */
.track-wrapper { position: relative; }

.track-bar {
  position: relative; height: 56px;
  background: #0f172a; border-radius: 0.75rem;
  overflow: hidden; cursor: pointer;
  border: 1px solid rgba(255,255,255,0.06);
}

.filmstrip-canvas { display: block; width: 100%; height: 100%; opacity: 0.7; }

/* Masks outside selection */
.track-mask {
  position: absolute; top: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.65);
  pointer-events: none;
}
.track-mask.left { left: 0; }
.track-mask.right { right: 0; }

/* Selection */
.track-selection {
  position: absolute; top: 0; bottom: 0;
  border-top: 2px solid rgba(212,135,94,0.5);
  border-bottom: 2px solid rgba(212,135,94,0.5);
  pointer-events: none;
}

.selection-glow {
  position: absolute; inset: -2px;
  background: rgba(212,135,94,0.06);
}

/* Handles */
.track-handle {
  position: absolute; top: 0; bottom: 0;
  width: 8px; margin-left: -4px;
  cursor: ew-resize; z-index: 5;
  display: flex; align-items: center; justify-content: center;
}

.handle-grip {
  width: 8px; height: 32px; border-radius: 4px;
  background: var(--accent);
  box-shadow: 0 0 12px rgba(99,102,241,0.5);
  transition: box-shadow 0.2s, transform 0.15s;
}

.track-handle:hover .handle-grip {
  box-shadow: 0 0 20px rgba(99,102,241,0.8);
  transform: scaleY(1.15);
}

.trimmer-empty, .trimmer-loading {
  padding: 3rem;
  color: var(--text-tertiary); font-size: 0.875rem;
  border: 2px dashed var(--border); border-radius: var(--radius-lg);
  display: flex; flex-direction: column; gap: 0.75rem;
  background: var(--bg-surface);
}

.spinner {
  width: 2rem; height: 2rem;
  border: 3px solid var(--border-light);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
