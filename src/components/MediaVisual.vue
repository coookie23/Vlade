<template>
  <div class="media-visual" :class="[`media-visual--${suite.key}`, `media-visual--${variant}`]">
    <img :src="suite.visual" alt="" loading="lazy" />
    <div class="visual-shade" />

    <div v-if="suite.key === 'video'" class="video-ui">
      <div class="video-screen">
        <Icon icon="ph:play-fill" width="28" />
      </div>
      <div class="video-timeline">
        <span v-for="i in 5" :key="i" :style="{ width: `${18 + i * 8}%` }" />
      </div>
      <div class="mini-tools">
        <span><Icon icon="ph:scissors" width="14" /> {{ labels.cut }}</span>
        <span><Icon icon="ph:arrows-left-right" width="14" /> {{ labels.convert }}</span>
      </div>
    </div>

    <div v-else-if="suite.key === 'image'" class="image-ui">
      <div class="crop-box">
        <i class="handle handle-a" />
        <i class="handle handle-b" />
        <i class="handle handle-c" />
        <i class="handle handle-d" />
      </div>
      <div class="image-controls">
        <span v-for="i in 4" :key="i"><b :style="{ width: `${36 + i * 12}%` }" /></span>
      </div>
      <div class="mini-tools">
        <span><Icon icon="ph:crop" width="14" /> {{ labels.cut }}</span>
        <span><Icon icon="ph:image-square" width="14" /> {{ labels.compress }}</span>
      </div>
    </div>

    <div v-else class="audio-ui">
      <div class="waveform">
        <span v-for="i in 28" :key="i" :style="{ height: `${18 + ((i * 7) % 46)}px` }" />
      </div>
      <div class="mixer">
        <span v-for="i in 3" :key="i"><b :style="{ height: `${32 + i * 18}%` }" /></span>
      </div>
      <div class="mini-tools">
        <span><Icon icon="ph:waveform" width="14" /> {{ labels.trim }}</span>
        <span><Icon icon="ph:speaker-high" width="14" /> {{ labels.volume }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { Icon } from '@iconify/vue'

export default {
  name: 'MediaVisual',
  components: { Icon },
  props: {
    suite: { type: Object, required: true },
    variant: { type: String, default: 'panel' },
  },
  data() {
    return {
      labels: {
        cut: '\u88c1\u526a',
        convert: '\u8f6c\u6362',
        compress: '\u538b\u7f29',
        trim: '\u526a\u5207',
        volume: '\u97f3\u91cf',
      },
    }
  },
}
</script>

<style scoped>
.media-visual {
  position: relative;
  width: 100%;
  min-height: 100%;
  overflow: hidden;
  border-radius: inherit;
  background:
    radial-gradient(circle at 24% 12%, rgba(212, 135, 94, 0.14), transparent 16rem),
    linear-gradient(145deg, rgba(42, 36, 30, 0.7), rgba(13, 12, 10, 0.88));
}

.media-visual img {
  width: 100%;
  height: 100%;
  min-height: inherit;
  display: block;
  object-fit: cover;
  filter: saturate(0.58) brightness(0.58);
  transform: scale(1.04);
  transition:
    transform 0.82s cubic-bezier(0.16, 1, 0.3, 1),
    filter 0.82s cubic-bezier(0.16, 1, 0.3, 1);
}

.media-visual:hover img {
  filter: saturate(0.72) brightness(0.66);
  transform: scale(1.09);
}

.visual-shade {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(180deg, rgba(0, 0, 0, 0.04), rgba(0, 0, 0, 0.72)),
    radial-gradient(circle at 70% 22%, rgba(212, 135, 94, 0.18), transparent 12rem);
}

.video-ui,
.image-ui,
.audio-ui {
  position: absolute;
  inset: 0;
  z-index: 2;
  padding: clamp(0.9rem, 2vw, 1.25rem);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  gap: 0.8rem;
}

.video-screen {
  position: absolute;
  inset: 13% 12% auto;
  aspect-ratio: 16 / 9;
  display: grid;
  place-items: center;
  border-radius: 14px;
  color: var(--accent);
  border: 1px solid rgba(255, 255, 255, 0.12);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(0, 0, 0, 0.24)),
    rgba(0, 0, 0, 0.22);
  box-shadow: inset 0 0 0 1px rgba(212, 135, 94, 0.08), 0 20px 60px rgba(0, 0, 0, 0.34);
}

.video-timeline {
  display: grid;
  gap: 0.35rem;
  padding: 0.75rem;
  border-radius: 13px;
  background: rgba(8, 7, 6, 0.62);
  backdrop-filter: blur(14px);
}

.video-timeline span {
  height: 0.46rem;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(212, 135, 94, 0.92), rgba(212, 135, 94, 0.14));
}

.crop-box {
  position: absolute;
  inset: 16% 18% 30%;
  border: 2px solid rgba(240, 235, 228, 0.76);
  background:
    linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
    rgba(0, 0, 0, 0.12);
  background-size: 33.333% 33.333%;
  box-shadow: 0 20px 70px rgba(0, 0, 0, 0.35);
}

.handle {
  position: absolute;
  width: 0.72rem;
  height: 0.72rem;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 18px rgba(212, 135, 94, 0.5);
}

.handle-a { left: -0.36rem; top: -0.36rem; }
.handle-b { right: -0.36rem; top: -0.36rem; }
.handle-c { left: -0.36rem; bottom: -0.36rem; }
.handle-d { right: -0.36rem; bottom: -0.36rem; }

.image-controls {
  display: grid;
  gap: 0.5rem;
  padding: 0.8rem;
  border-radius: 13px;
  background: rgba(8, 7, 6, 0.62);
  backdrop-filter: blur(14px);
}

.image-controls span {
  height: 0.42rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
}

.image-controls b {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: rgba(212, 135, 94, 0.82);
}

.waveform {
  min-height: 120px;
  display: flex;
  align-items: center;
  gap: 0.22rem;
  padding: 0.9rem;
  border-radius: 15px;
  background: rgba(8, 7, 6, 0.58);
  backdrop-filter: blur(14px);
}

.waveform span {
  flex: 1;
  border-radius: 999px;
  background: linear-gradient(180deg, rgba(240, 235, 228, 0.76), rgba(212, 135, 94, 0.72));
  animation: visualWave 1.6s cubic-bezier(0.65, 0, 0.35, 1) infinite alternate;
}

.waveform span:nth-child(3n) { animation-delay: 0.14s; }
.waveform span:nth-child(4n) { animation-delay: 0.28s; }

.mixer {
  position: absolute;
  top: 12%;
  right: 1rem;
  display: flex;
  gap: 0.45rem;
  height: 150px;
  padding: 0.65rem;
  border-radius: 14px;
  background: rgba(8, 7, 6, 0.58);
  backdrop-filter: blur(14px);
}

.mixer span {
  position: relative;
  width: 0.45rem;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.1);
}

.mixer b {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: inherit;
  background: var(--accent);
}

.mini-tools {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.mini-tools span {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  min-height: 2rem;
  padding: 0 0.65rem;
  border-radius: 999px;
  color: var(--text-primary);
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(8, 7, 6, 0.58);
  backdrop-filter: blur(14px);
  font-size: 0.72rem;
}

.media-visual--card .video-screen {
  inset: 10% 10% auto;
}

.media-visual--card .crop-box {
  inset: 13% 16% 28%;
}

.media-visual--card .waveform {
  min-height: 86px;
}

@keyframes visualWave {
  from {
    transform: scaleY(0.72);
    opacity: 0.72;
  }
  to {
    transform: scaleY(1.08);
    opacity: 1;
  }
}
</style>
