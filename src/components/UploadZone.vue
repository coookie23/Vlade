<template>
  <div class="upload-wrap">
    <div
      class="upload-zone"
      :class="{ 'drag-over': dragging, 'has-file': files.length, processing: status === 'processing', done: status === 'done', error: status === 'error' }"
      @click="openPicker"
      @dragover.prevent="dragging = true"
      @dragleave="dragging = false"
      @drop.prevent="onDrop"
    >
      <input ref="input" class="file-input" type="file" :accept="accept" :multiple="multiple" @change="onSelect" />

      <div class="zone-grid">
        <div class="zone-icon">
          <Icon :icon="statusIcon" width="26" />
        </div>

        <div class="zone-copy">
          <template v-if="status === 'idle' && !files.length">
            <h4>{{ multiple ? '选择多个文件' : '选择文件' }}</h4>
            <p>拖进来，或点击选择。</p>
            <span v-if="hint">{{ hint }}</span>
          </template>
          <template v-else-if="status === 'idle'">
            <h4>{{ files.length > 1 ? `${files.length} 个文件已选择` : files[0].name }}</h4>
            <p>{{ selectedSummary }}</p>
            <button type="button" class="inline-action" @click.stop="pickAgain">重新选择</button>
          </template>
          <template v-else-if="status === 'processing'">
            <h4>{{ progressText }}</h4>
            <p v-if="progressPercent > 0">{{ Math.round(progressPercent) }}%{{ progressSpeed ? ` · ${progressSpeed.toFixed(1)}x` : '' }}</p>
            <p v-else>保持页面打开，完成后会显示下载。</p>
          </template>
          <template v-else-if="status === 'done'">
            <h4>处理完成</h4>
            <p>结果已经准备好。</p>
          </template>
          <template v-else>
            <h4>处理失败</h4>
            <p>{{ errorMsg }}</p>
          </template>
        </div>
      </div>

      <div v-if="status === 'processing'" class="progress-track"><span :style="{ width: (progressPercent || 5) + '%' }" /></div>
    </div>

    <div class="upload-actions">
      <button v-if="files.length && status === 'idle'" class="submit-btn" type="button" @click="submit">
        <Icon icon="ph:play" width="16" />
        开始 {{ submitLabel }}
      </button>
      <button v-if="files.length || status === 'done' || status === 'error'" class="reset-btn" type="button" @click="reset">
        <Icon icon="ph:arrow-counter-clockwise" width="16" />
        重置
      </button>
    </div>
  </div>
</template>

<script>
import { Icon } from '@iconify/vue'

export default {
  name: 'UploadZone',
  components: { Icon },
  props: {
    accept: { type: String, default: '' },
    hint: { type: String, default: '' },
    action: { type: Function, required: true },
    progressText: { type: String, default: '处理中...' },
    submitLabel: { type: String, default: '处理' },
    multiple: { type: Boolean, default: false },
    progressPercent: { type: Number, default: 0 },
    progressSpeed: { type: Number, default: 0 },
  },
  emits: ['file-selected', 'done', 'reset'],
  data() {
    return { dragging: false, files: [], status: 'idle', errorMsg: '' }
  },
  computed: {
    statusIcon() {
      if (this.status === 'processing') return 'ph:spinner-gap'
      if (this.status === 'done') return 'ph:check-circle'
      if (this.status === 'error') return 'ph:warning-circle'
      if (this.files.length) return this.multiple ? 'ph:files' : 'ph:file'
      return 'ph:upload-simple'
    },
    selectedSummary() {
      if (!this.files.length) return ''
      const total = this.files.reduce((sum, file) => sum + file.size, 0)
      return `${this.formatSize(total)} · ${this.multiple ? '按选择顺序处理' : '准备好了'}`
    },
  },
  methods: {
    openPicker() {
      if (this.status === 'processing') return
      if (!this.files.length) this.$refs.input.click()
    },
    onDrop(event) {
      this.dragging = false
      this.setFiles(Array.from(event.dataTransfer.files || []))
    },
    onSelect(event) {
      this.setFiles(Array.from(event.target.files || []))
    },
    setFiles(files) {
      if (!files.length) return
      this.files = this.multiple ? files : files.slice(0, 1)
      this.status = 'idle'
      this.errorMsg = ''
      this.$emit('file-selected', this.multiple ? this.files : this.files[0])
    },
    pickAgain() {
      this.files = []
      this.$nextTick(() => this.$refs.input.click())
    },
    async submit() {
      if (!this.files.length) return
      this.status = 'processing'
      this.errorMsg = ''
      try {
        const payload = this.multiple ? this.files : this.files[0]
        const result = await this.action(payload)
        this.status = 'done'
        this.$emit('done', result)
      } catch (error) {
        this.errorMsg = error?.message || '处理失败'
        this.status = 'error'
      }
    },
    reset() {
      this.files = []
      this.status = 'idle'
      this.errorMsg = ''
      if (this.$refs.input) this.$refs.input.value = ''
      this.$emit('reset')
    },
    formatSize(bytes) {
      if (bytes < 1024) return `${bytes} B`
      if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
      return `${(bytes / 1024 / 1024).toFixed(1)} MB`
    },
  },
}
</script>

<style scoped>
.upload-wrap { display: flex; flex-direction: column; gap: 0.85rem; }
.upload-zone {
  position: relative; min-height: 188px; display: flex; flex-direction: column; justify-content: center;
  border: 1px dashed rgba(255,255,255,0.14); border-radius: 16px; padding: 1.1rem; cursor: pointer; overflow: hidden;
  background: radial-gradient(circle at 20% 10%, rgba(212,135,94,0.13), transparent 14rem), linear-gradient(150deg, rgba(255,255,255,0.045), rgba(0,0,0,0.14)), rgba(10,9,8,0.28);
  transition: border-color 0.26s cubic-bezier(0.2,0.9,0.2,1), transform 0.26s cubic-bezier(0.2,0.9,0.2,1), background 0.26s cubic-bezier(0.2,0.9,0.2,1);
}
.upload-zone::before {
  content: ''; position: absolute; inset: 0; opacity: 0.12; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.72' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
.upload-zone::after {
  content: '';
  position: absolute;
  inset: 0.82rem;
  border-radius: 13px;
  pointer-events: none;
  opacity: 0;
  border: 1px solid rgba(212,135,94,0.18);
  background:
    radial-gradient(circle at 50% 50%, rgba(212,135,94,0.16), transparent 6rem),
    linear-gradient(90deg, transparent, rgba(212,135,94,0.08), transparent);
  transform: scale(0.94);
  transition:
    opacity 0.28s cubic-bezier(0.16,1,0.3,1),
    transform 0.32s cubic-bezier(0.16,1,0.3,1);
}
.upload-zone:hover, .upload-zone.drag-over { border-color: rgba(212,135,94,0.54); transform: translateY(-2px); }
.upload-zone.drag-over {
  background:
    radial-gradient(circle at 50% 45%, rgba(212,135,94,0.18), transparent 11rem),
    radial-gradient(circle at 20% 10%, rgba(212,135,94,0.13), transparent 14rem),
    linear-gradient(150deg, rgba(255,255,255,0.055), rgba(0,0,0,0.12)),
    rgba(10,9,8,0.34);
  box-shadow: 0 20px 60px rgba(0,0,0,0.26), 0 0 0 1px rgba(212,135,94,0.08);
}
.upload-zone.drag-over::after {
  opacity: 1;
  transform: scale(1);
  animation: dropTarget 1.15s cubic-bezier(0.65,0,0.35,1) infinite alternate;
}
.upload-zone.processing::after {
  opacity: 0.62;
  transform: scale(1);
  background:
    linear-gradient(105deg, transparent 0 34%, rgba(212,135,94,0.14) 47%, transparent 60% 100%),
    radial-gradient(circle at 50% 50%, rgba(212,135,94,0.1), transparent 6rem);
  background-size: 220% 100%, 100% 100%;
  animation: uploadScanner 1.45s cubic-bezier(0.65,0,0.35,1) infinite;
}
.upload-zone.has-file { border-style: solid; border-color: rgba(212,135,94,0.36); }
.upload-zone.done { border-color: rgba(102,194,140,0.42); }
.upload-zone.error { border-color: rgba(222,107,95,0.5); }
.file-input { display: none; }
.zone-grid { position: relative; z-index: 1; display: grid; grid-template-columns: 3.35rem minmax(0, 1fr); gap: 0.95rem; align-items: center; }
.zone-icon {
  position: relative;
  overflow: hidden;
  width: 3.35rem; height: 3.35rem; display: grid; place-items: center; border-radius: 15px; color: var(--accent);
  background: linear-gradient(135deg, rgba(212,135,94,0.18), rgba(212,135,94,0.04)), rgba(0,0,0,0.18);
  transition:
    transform 0.28s cubic-bezier(0.16,1,0.3,1),
    box-shadow 0.28s cubic-bezier(0.16,1,0.3,1),
    background 0.28s cubic-bezier(0.16,1,0.3,1);
}
.zone-icon::before {
  content: '';
  position: absolute;
  left: -30%;
  right: -30%;
  height: 1px;
  top: 50%;
  opacity: 0;
  background: linear-gradient(90deg, transparent, rgba(212,135,94,0.78), transparent);
  transform: translateY(-1.2rem);
}
.upload-zone.drag-over .zone-icon {
  transform: translateY(-2px) scale(1.05);
  background: linear-gradient(135deg, rgba(212,135,94,0.26), rgba(212,135,94,0.07)), rgba(0,0,0,0.22);
  box-shadow: 0 16px 34px rgba(0,0,0,0.24), inset 0 0 0 1px rgba(212,135,94,0.18);
}
.upload-zone.drag-over .zone-icon::before,
.upload-zone.processing .zone-icon::before {
  opacity: 1;
  animation: iconScanner 1.05s cubic-bezier(0.65,0,0.35,1) infinite;
}
.processing .zone-icon svg { animation: spin 0.9s cubic-bezier(0.68,0,0.32,1) infinite; }
.done .zone-icon { color: #66c28c; }
.error .zone-icon { color: #de6b5f; }
.zone-copy { min-width: 0; }
.zone-copy h4 { color: var(--text-primary); font-size: 1rem; line-height: 1.35; overflow-wrap: anywhere; }
.zone-copy p, .zone-copy span { display: block; color: var(--text-tertiary); font-size: 0.78rem; margin-top: 0.2rem; }
.inline-action { margin-top: 0.65rem; border: 0; color: var(--accent); background: transparent; cursor: pointer; font-size: 0.76rem; padding: 0; }
.progress-track { position: relative; z-index: 1; height: 3px; margin-top: 1.2rem; overflow: hidden; border-radius: 999px; background: rgba(255,255,255,0.08); }
.progress-track::after {
  content: '';
  position: absolute;
  inset: 0;
  width: 35%;
  border-radius: inherit;
  background: linear-gradient(90deg, transparent, rgba(255,226,202,0.24), transparent);
  transform: translateX(-120%);
  animation: loadSweep 1.1s cubic-bezier(0.65,0,0.35,1) infinite;
}
.progress-track span { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, rgba(212,135,94,0), rgba(212,135,94,0.95), rgba(212,135,94,0.2)); transition: width 0.4s ease-out; }
.upload-actions { display: flex; gap: 0.55rem; flex-wrap: wrap; }
.submit-btn, .reset-btn {
  min-height: 2.65rem; display: inline-flex; align-items: center; justify-content: center; gap: 0.45rem;
  border-radius: 12px; padding: 0 1rem; cursor: pointer; font-family: var(--font-body); font-weight: 800;
  transition: transform 0.24s cubic-bezier(0.2,0.9,0.2,1), box-shadow 0.24s cubic-bezier(0.2,0.9,0.2,1);
}
.submit-btn { flex: 1; border: 0; color: var(--bg); background: var(--accent); box-shadow: 0 14px 36px rgba(212,135,94,0.18); }
.submit-btn:hover, .reset-btn:hover { transform: translateY(-2px); }
.reset-btn { border: 1px solid rgba(255,255,255,0.08); color: var(--text-secondary); background: rgba(255,255,255,0.045); }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes loadSweep { 0% { transform: translateX(-120%); } 100% { transform: translateX(260%); } }
@keyframes dropTarget {
  from {
    box-shadow: inset 0 0 0 1px rgba(212,135,94,0.08), 0 0 0 rgba(212,135,94,0);
  }
  to {
    box-shadow: inset 0 0 24px rgba(212,135,94,0.08), 0 0 28px rgba(212,135,94,0.12);
  }
}
@keyframes uploadScanner {
  0% {
    background-position: -160% 0, 0 0;
  }
  100% {
    background-position: 220% 0, 0 0;
  }
}
@keyframes iconScanner {
  0% {
    transform: translateY(-1.2rem);
  }
  100% {
    transform: translateY(1.2rem);
  }
}
@media (max-width: 560px) {
  .upload-zone { min-height: 170px; padding: 0.95rem; }
  .zone-grid { grid-template-columns: 1fr; }
  .upload-actions { flex-direction: column; }
}
</style>
