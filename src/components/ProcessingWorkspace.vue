<template>
  <div class="process-page" :class="[`process-page--${suite.key}`, { 'is-switching': toolSwitching, 'is-ready': pageReady }]">
    <aside class="tool-rail">
      <router-link to="/" class="rail-home"><Icon icon="ph:arrow-left" width="16" />首页</router-link>
      <nav class="media-switch" aria-label="媒体类型切换">
        <router-link v-for="item in mediaSwitchItems" :key="item.path" :to="item.path" class="media-switch-link" :class="{ active: suite.key === item.key }">
          <Icon :icon="item.icon" width="16" />
          <span>{{ item.label }}</span>
        </router-link>
      </nav>
      <div class="rail-heading">
        <span class="rail-eyebrow">{{ suite.eyebrow }}</span>
        <h1>{{ suite.title }}</h1>
        <p>{{ suite.intro }}</p>
      </div>
      <nav class="rail-nav" aria-label="工具列表">
        <button v-for="tool in suite.tools" :key="tool.id" class="tool-pill" :class="{ active: activeTool.id === tool.id }" type="button" @click="selectTool(tool)">
          <span class="tool-pill-icon"><Icon :icon="tool.icon" width="18" /></span>
          <span><strong>{{ tool.title }}</strong><small>{{ tool.desc }}</small></span>
        </button>
      </nav>
    </aside>

    <main class="process-main">
      <section class="top-stage">
        <div class="stage-copy">
          <span class="stage-badge"><Icon :icon="suite.icon" width="15" />{{ suite.badge }}</span>
          <h2>{{ activeTool.title }}</h2>
          <p>{{ activeTool.desc }}</p>
        </div>
        <div class="stage-stats">
          <div v-for="item in suite.stats" :key="item.label" class="stat-tile"><span>{{ item.value }}</span><small>{{ item.label }}</small></div>
        </div>
      </section>

      <section class="work-card">
        <div class="card-head">
          <span class="card-mark" />
          <div><h3>选择文件</h3><p>{{ activeTool.multi ? '一次选择多个文件，按顺序处理。' : '拖进来，或从本地选择。' }}</p></div>
        </div>
        <UploadZone
          :key="uploadKey"
          :action="submitFiles"
          :accept="activeTool.accept || suite.accept"
          :multiple="Boolean(activeTool.multi)"
          :submit-label="activeTool.title"
          :progress-text="`正在${activeTool.action}...`"
          :progress-percent="processingPercent"
          :progress-speed="processingSpeed"
          @file-selected="onFileSelected"
          @done="onDone"
          @reset="onReset"
        />
      </section>

      <section v-if="analysis || analysisError || analyzing" class="work-card analysis-card">
        <div class="card-head">
          <span class="card-mark" />
          <div><h3>文件体检卡</h3><p>{{ analyzing ? '正在读取文件信息...' : analysisError || '上传后自动生成，帮助你选对处理方式。' }}</p></div>
        </div>
        <div v-if="analysis" class="analysis-grid">
          <div v-for="item in analysisItems" :key="item.label" class="analysis-item"><small>{{ item.label }}</small><strong>{{ item.value }}</strong></div>
        </div>
        <ul v-if="analysis?.suggestions?.length" class="suggestions">
          <li v-for="tip in analysis.suggestions" :key="tip">{{ tip }}</li>
        </ul>
      </section>

      <section v-if="activeControls.length" class="work-card">
        <div class="card-head">
          <span class="card-mark" />
          <div><h3>参数</h3><p>只显示当前工具会用到的选项。</p></div>
        </div>
        <div class="control-grid">
          <div v-for="control in activeControls" :key="control.key" class="control-field">
            <span class="control-label">{{ control.label }}</span>
            <template v-if="control.type === 'range'">
              <input v-model.number="params[control.key]" class="control-range" type="range" :min="control.min" :max="control.max" :step="control.step || 1" />
              <span class="range-row"><small>{{ control.low }}</small><strong>{{ params[control.key] }}</strong><small>{{ control.high }}</small></span>
            </template>
            <template v-else-if="control.type === 'chips'">
              <span class="chip-row">
                <button v-for="option in control.options" :key="option" class="param-chip" :class="{ active: params[control.key] === option }" :aria-pressed="params[control.key] === option" type="button" @click="params[control.key] = option">
                  {{ String(option).toUpperCase() }}
                </button>
              </span>
            </template>
            <template v-else-if="control.type === 'select'">
              <select v-model.number="params[control.key]" class="control-input">
                <option v-for="option in control.options" :key="option" :value="option">{{ option }}{{ control.key === 'fps' ? ' fps' : control.key === 'width' ? ' px' : '' }}</option>
              </select>
            </template>
            <template v-else-if="control.type === 'text'">
              <input v-model="params[control.key]" class="control-input" type="text" :placeholder="control.placeholder || ''" />
            </template>
            <template v-else>
              <input v-model.number="params[control.key]" class="control-input" type="number" :min="control.min" :step="control.step || 1" />
            </template>
          </div>
        </div>
        <div v-if="currentModeNote" class="mode-note">
          <div><small>适合</small><p>{{ currentModeNote.good }}</p></div>
          <div><small>不适合</small><p>{{ currentModeNote.bad }}</p></div>
          <div><small>说明</small><p>{{ currentModeNote.note }}</p></div>
        </div>
      </section>

      <section v-if="selectedFiles.length || result" class="work-card">
        <div class="card-head">
          <span class="card-mark" />
          <div><h3>{{ result ? '处理完成' : '预览' }}</h3><p>{{ result ? result.filename : fileSummary }}</p></div>
        </div>
        <div class="preview-shell">
          <video v-if="previewUrl && suite.uploadKind === 'video'" :src="previewUrl" controls />
          <img v-else-if="previewUrl && suite.uploadKind === 'image'" :src="previewUrl" alt="" />
          <audio v-else-if="previewUrl && suite.uploadKind === 'audio'" :src="previewUrl" controls />
          <div v-else class="file-stack">
            <div v-for="file in selectedFiles" :key="file.name" class="file-row"><Icon icon="ph:file" width="16" /><span>{{ file.name }}</span><small>{{ formatSize(file.size) }}</small></div>
          </div>
        </div>
        <div v-if="result" class="result-card">
          <div><small>源文件</small><strong>{{ sourceName }}</strong></div>
          <div><small>输出文件</small><strong>{{ result.filename }}</strong></div>
          <div><small>输出格式</small><strong>{{ outputFormat }}</strong></div>
          <div><small>源文件大小</small><strong>{{ sourceSize }}</strong></div>
        </div>
        <div v-if="result" class="download-strip">
          <span><Icon icon="ph:check-circle" width="18" /> 已完成</span>
          <button type="button" @click="saveFile">保存</button>
          <button type="button" class="ghost" @click="resetWorkspace">重新处理</button>
        </div>
      </section>
    </main>

    <aside class="side-panel">
      <div class="visual-card">
        <MediaVisual :suite="suite" variant="panel" />
        <div class="visual-overlay"><span>{{ suite.title }}</span><strong>{{ activeTool.action }}</strong></div>
      </div>
      <section class="side-card">
        <h3><Icon icon="ph:lightning" width="16" /> 现在可以做</h3>
        <ul><li v-for="tip in activeTips" :key="tip">{{ tip }}</li></ul>
      </section>
      <section class="side-card">
        <h3><Icon icon="ph:pulse" width="16" /> 记录</h3>
        <div class="log-list"><div v-for="entry in activityLog" :key="entry.id" class="log-row" :class="entry.type"><span /><p>{{ entry.msg }}</p><small>{{ entry.time }}</small></div></div>
      </section>
    </aside>
  </div>
</template>

<script>
import { Icon } from '@iconify/vue'
import MediaVisual from './MediaVisual.vue'
import UploadZone from './UploadZone.vue'
import { analyzeMedia, downloadUrl, pollProgress, uploadAudio, uploadImage, uploadVideo } from '../api/index.js'

const uploaders = { video: uploadVideo, image: uploadImage, audio: uploadAudio }
const mediaSwitchItems = [
  { key: 'video', path: '/video', label: '视频', icon: 'ph:video-camera' },
  { key: 'image', path: '/image', label: '图片', icon: 'ph:image' },
  { key: 'audio', path: '/audio', label: '音频', icon: 'ph:music-notes' },
]

export default {
  name: 'ProcessingWorkspace',
  components: { Icon, MediaVisual, UploadZone },
  props: { suite: { type: Object, required: true } },
  data() {
    return {
      activeTool: this.suite.tools[0],
      params: {},
      selectedFiles: [],
      previewUrl: '',
      result: null,
      uploadKeySeed: 0,
      activityLog: [],
      analysis: null,
      analysisError: '',
      analyzing: false,
      taskId: null,
      processingPercent: 0,
      processingSpeed: 0,
      cancelPoll: null,
      mediaSwitchItems,
      toolSwitching: false,
      switchTimer: 0,
      pageReady: false,
    }
  },
  computed: {
    activeControls() { return this.activeTool.controls || [] },
    activeTips() { return this.activeTool.tips || ['选择文件后开始处理。'] },
    uploadKey() { return `${this.suite.key}-${this.activeTool.id}-${this.uploadKeySeed}` },
    fileSummary() {
      if (!this.selectedFiles.length) return '还没有选择文件'
      return this.selectedFiles.length === 1 ? this.selectedFiles[0].name : `${this.selectedFiles.length} 个文件已选择`
    },
    sourceName() { return this.analysis?.filename || this.selectedFiles[0]?.name || '-' },
    sourceSize() { return this.analysis?.size_label || (this.selectedFiles[0] ? this.formatSize(this.selectedFiles[0].size) : '-') },
    outputFormat() { return this.result?.filename?.split('.').pop()?.toUpperCase() || '-' },
    currentModeNote() { return this.activeTool.modeNotes?.[this.params.mode] || null },
    analysisItems() {
      if (!this.analysis) return []
      const m = this.analysis.metadata || {}
      const base = [
        { label: '格式', value: String(this.analysis.format || '-').toUpperCase() },
        { label: '大小', value: this.analysis.size_label || '-' },
      ]
      if (this.analysis.kind === 'image') return [...base, { label: '尺寸', value: `${m.width || '-'} x ${m.height || '-'}` }, { label: '色彩', value: m.has_alpha ? `${m.mode} / 透明` : (m.mode || '-') }]
      if (this.analysis.kind === 'video') return [...base, { label: '时长', value: this.formatDuration(m.duration) }, { label: '分辨率', value: `${m.width || '-'} x ${m.height || '-'}` }, { label: '编码', value: m.video_codec || '-' }]
      return [...base, { label: '时长', value: this.formatDuration(m.duration) }, { label: '采样率', value: m.sample_rate ? `${m.sample_rate} Hz` : '-' }, { label: '声道', value: m.channels || '-' }]
    },
  },
  watch: {
    suite: { immediate: true, handler(nextSuite) { this.activeTool = nextSuite.tools[0]; this.resetParams(); this.resetWorkspace(false); this.triggerToolMotion(); this.addLog(`进入${nextSuite.title}`) } },
  },
  mounted() {
    requestAnimationFrame(() => { this.pageReady = true })
  },
  beforeUnmount() {
    if (this.switchTimer) window.clearTimeout(this.switchTimer)
    this.revokePreview()
  },
  methods: {
    selectTool(tool) {
      if (tool.id === this.activeTool.id) return
      this.activeTool = tool
      this.resetParams()
      this.resetWorkspace(false)
      this.triggerToolMotion()
      this.addLog(`切换到${tool.title}`)
    },
    triggerToolMotion() {
      if (this.switchTimer) window.clearTimeout(this.switchTimer)
      this.toolSwitching = false
      this.$nextTick(() => {
        this.toolSwitching = true
        this.switchTimer = window.setTimeout(() => { this.toolSwitching = false }, 620)
      })
    },
    resetParams() { this.params = { ...(this.activeTool.params || {}) } },
    onFileSelected(fileOrFiles) {
      this.revokePreview()
      const files = Array.isArray(fileOrFiles) ? fileOrFiles : [fileOrFiles]
      this.selectedFiles = files
      this.result = null
      this.analysis = null
      this.analysisError = ''
      const first = files[0]
      if (first && !this.activeTool.multi) this.previewUrl = URL.createObjectURL(first)
      this.addLog(files.length > 1 ? `选择了 ${files.length} 个文件` : `选择 ${first.name}`)
      if (first && !this.activeTool.multi) this.runAnalyze(first)
    },
    async runAnalyze(file) {
      this.analyzing = true
      try { this.analysis = await analyzeMedia(file); this.addLog('文件体检完成', 'done') }
      catch { this.analysisError = '暂时无法读取文件信息'; this.addLog('文件体检失败', 'error') }
      finally { this.analyzing = false }
    },
    async submitFiles(fileOrFiles) {
      this.processingPercent = 0; this.processingSpeed = 0
      this.addLog(`开始${this.activeTool.action}`, 'active')
      const result = await uploaders[this.suite.uploadKind](this.activeTool.endpoint, fileOrFiles, this.cleanParams(), { multi: Boolean(this.activeTool.multi) })

      // Async tasks: wait for progress to complete before resolving
      if (result.task_id) {
        this.taskId = result.task_id
        return new Promise((resolve, reject) => {
          if (this.cancelPoll) this.cancelPoll()
          this.cancelPoll = pollProgress(
            this.taskId,
            (data) => { this.processingPercent = data.percent; this.processingSpeed = data.speed },
            () => {
              this.processingPercent = 100
              this.cancelPoll = null
              resolve(result)
            },
            () => { this.addLog('进度获取失败', 'error'); reject(new Error('进度获取失败')) },
          )
        })
      }
      return result
    },
    startPolling() {
      // handled inside submitFiles for async tasks
    },
    onDone(result) { this.result = result; this.processingPercent = 100; this.addLog(`完成 ${result.filename}`, 'done') },
    onReset() { this.resetWorkspace(false) },
    resetWorkspace(resetUpload = true) {
      if (this.cancelPoll) { this.cancelPoll(); this.cancelPoll = null }
      this.taskId = null; this.processingPercent = 0; this.processingSpeed = 0
      this.revokePreview(); this.selectedFiles = []; this.result = null; this.analysis = null; this.analysisError = ''; this.analyzing = false
      if (resetUpload) { this.uploadKeySeed += 1; this.addLog('重置工作区') }
    },
    revokePreview() { if (this.previewUrl) URL.revokeObjectURL(this.previewUrl); this.previewUrl = '' },
    cleanParams() { return Object.fromEntries(Object.entries(this.params).filter(([, value]) => value !== '' && value !== null && value !== undefined)) },
    async saveFile() {
      if (!this.result) return
      const name = this.result.filename
      try {
        if (window.showSaveFilePicker) {
          const handle = await window.showSaveFilePicker({ suggestedName: name })
          const response = await fetch(downloadUrl(name))
          const blob = await response.blob()
          const writable = await handle.createWritable()
          await writable.write(blob)
          await writable.close()
        } else {
          const a = document.createElement('a'); a.href = downloadUrl(name); a.download = name; a.click()
        }
        this.addLog(`保存 ${name}`, 'done')
      } catch (error) { if (error?.name !== 'AbortError') this.addLog('保存失败', 'error') }
    },
    addLog(msg, type = 'info') {
      const now = new Date(); const time = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`
      this.activityLog.unshift({ id: `${Date.now()}-${Math.random()}`, msg, time, type })
      if (this.activityLog.length > 8) this.activityLog.pop()
    },
    formatSize(bytes) { if (bytes < 1024) return `${bytes} B`; if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`; return `${(bytes / 1024 / 1024).toFixed(1)} MB` },
    formatDuration(seconds) { if (!seconds) return '-'; const m = Math.floor(seconds / 60); const s = Math.round(seconds % 60); return m ? `${m}分${s}秒` : `${s}秒` },
  },
}
</script>

<style scoped>
.process-page { min-height: calc(100vh - 4.25rem); position: relative; z-index: 2; display: grid; grid-template-columns: 260px minmax(0, 1fr) 300px; gap: 1rem; padding: 1rem; background: radial-gradient(circle at 18% 0%, rgba(212,135,94,0.12), transparent 28rem), radial-gradient(circle at 88% 24%, rgba(138,94,55,0.12), transparent 24rem), linear-gradient(135deg, rgba(22,19,16,0.82), rgba(13,12,10,0.96)); }
.process-page::before { content: ''; position: fixed; inset: 4.25rem 0 0; pointer-events: none; opacity: 0.08; background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.88' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.55'/%3E%3C/svg%3E"); mix-blend-mode: screen; }
.process-page::after { content: ''; position: fixed; inset: 4.25rem 0 0; pointer-events: none; opacity: 0.1; background: repeating-linear-gradient(90deg, transparent 0 82px, rgba(212,135,94,0.035) 83px, transparent 84px); transform: translateX(-16px); transition: opacity 0.42s cubic-bezier(0.16,1,0.3,1), transform 0.42s cubic-bezier(0.16,1,0.3,1); }
.process-page.is-switching::after { opacity: 0.22; transform: translateX(0); }
.tool-rail, .side-panel { position: sticky; top: 5.25rem; height: calc(100vh - 6.25rem); }
.tool-rail, .work-card, .side-card, .visual-card { border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; background: linear-gradient(155deg, rgba(42,36,30,0.76), rgba(16,14,12,0.78)), radial-gradient(circle at 12% 0%, rgba(212,135,94,0.07), transparent 16rem); backdrop-filter: blur(18px); box-shadow: 0 18px 60px rgba(0,0,0,0.25); }
.tool-rail, .process-main, .side-panel { opacity: 0; animation: workspaceEnter 0.72s cubic-bezier(0.16,1,0.3,1) forwards; }
.process-main { animation-delay: 0.06s; }
.side-panel { animation-delay: 0.12s; }
.tool-rail { display: flex; flex-direction: column; padding: 1rem; }
.rail-home { display: inline-flex; align-items: center; gap: 0.4rem; width: max-content; color: var(--text-tertiary); text-decoration: none; font-size: 0.75rem; font-family: var(--font-mono); transition: color 0.24s cubic-bezier(0.2,0.9,0.2,1), transform 0.24s cubic-bezier(0.2,0.9,0.2,1); }
.rail-home:hover { color: var(--accent); transform: translateX(-2px); }
.media-switch { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.35rem; margin-top: 0.9rem; padding: 0.25rem; border: 1px solid rgba(255,255,255,0.06); border-radius: 13px; background: rgba(0,0,0,0.18); }
.media-switch-link { min-width: 0; min-height: 2.35rem; display: inline-flex; align-items: center; justify-content: center; gap: 0.35rem; border: 1px solid transparent; border-radius: 10px; color: var(--text-tertiary); text-decoration: none; font-size: 0.74rem; font-weight: 800; transition: color 0.24s cubic-bezier(0.2,0.9,0.2,1), border-color 0.24s cubic-bezier(0.2,0.9,0.2,1), background 0.24s cubic-bezier(0.2,0.9,0.2,1), transform 0.24s cubic-bezier(0.2,0.9,0.2,1); }
.media-switch-link:hover { color: var(--text-primary); border-color: rgba(212,135,94,0.2); background: rgba(255,255,255,0.04); transform: translateY(-1px); }
.media-switch-link.active { color: var(--bg); border-color: var(--accent); background: var(--accent); box-shadow: 0 10px 26px rgba(212,135,94,0.2); }
.rail-heading { margin: 1.4rem 0 1rem; }
.rail-eyebrow, .stage-badge { display: inline-flex; align-items: center; gap: 0.35rem; color: var(--accent); font-family: var(--font-mono); font-size: 0.68rem; letter-spacing: 0.08em; }
.rail-heading h1 { margin-top: 0.2rem; color: var(--text-primary); font-family: var(--font-display); font-size: 1.7rem; line-height: 1.14; }
.rail-heading p { margin-top: 0.55rem; color: var(--text-tertiary); font-size: 0.78rem; line-height: 1.7; }
.rail-nav { display: flex; flex-direction: column; gap: 0.45rem; overflow-y: auto; padding-right: 0.1rem; }
.tool-pill { position: relative; overflow: hidden; display: grid; grid-template-columns: 2.15rem 1fr; gap: 0.7rem; width: 100%; padding: 0.75rem; border: 1px solid rgba(255,255,255,0.055); border-radius: 12px; color: var(--text-secondary); text-align: left; cursor: pointer; background: rgba(12,11,10,0.24); transition: border-color 0.26s cubic-bezier(0.2,0.9,0.2,1), transform 0.26s cubic-bezier(0.2,0.9,0.2,1), background 0.26s cubic-bezier(0.2,0.9,0.2,1); }
.tool-pill::after { content: ''; position: absolute; left: 3.6rem; right: 0.75rem; bottom: 0.54rem; height: 1px; border-radius: 999px; opacity: 0; background: linear-gradient(90deg, rgba(212,135,94,0), rgba(212,135,94,0.78), rgba(212,135,94,0.08)); transform: scaleX(0.2); transform-origin: left center; transition: opacity 0.28s cubic-bezier(0.16,1,0.3,1), transform 0.38s cubic-bezier(0.16,1,0.3,1); }
.tool-pill:hover { border-color: rgba(212,135,94,0.22); transform: translateX(4px); }
.tool-pill.active { color: var(--text-primary); border-color: rgba(212,135,94,0.34); background: linear-gradient(135deg, rgba(212,135,94,0.18), rgba(212,135,94,0.035)), rgba(18,15,12,0.72); box-shadow: inset 3px 0 0 var(--accent); }
.tool-pill.active::after { opacity: 0.95; transform: scaleX(1); animation: railLinePulse 1.7s cubic-bezier(0.65,0,0.35,1) infinite alternate; }
.tool-pill-icon { width: 2.15rem; height: 2.15rem; display: grid; place-items: center; border-radius: 10px; color: var(--accent); background: rgba(212,135,94,0.09); }
.tool-pill strong { display: block; font-size: 0.82rem; }
.tool-pill small { display: block; margin-top: 0.15rem; color: var(--text-tertiary); font-size: 0.68rem; line-height: 1.4; }
.process-main { min-width: 0; display: flex; flex-direction: column; gap: 1rem; }
.top-stage { display: grid; grid-template-columns: minmax(0, 1fr) 310px; gap: 1rem; align-items: end; min-height: 190px; padding: 1.5rem; border-radius: 18px; border: 1px solid rgba(255,255,255,0.06); background: linear-gradient(140deg, rgba(52,43,35,0.72), rgba(18,16,14,0.82)), radial-gradient(circle at 75% 20%, rgba(212,135,94,0.16), transparent 18rem); overflow: hidden; position: relative; }
.top-stage::before { content: ''; position: absolute; inset: 0; pointer-events: none; opacity: 0.16; background: linear-gradient(120deg, transparent 0 28%, rgba(212,135,94,0.18) 30%, transparent 34% 100%), repeating-linear-gradient(90deg, rgba(255,255,255,0.025) 0 1px, transparent 1px 42px); transform: translateX(-18%); transition: transform 0.52s cubic-bezier(0.16,1,0.3,1), opacity 0.52s cubic-bezier(0.16,1,0.3,1); }
.top-stage::after { content: ''; position: absolute; inset: 0.8rem; pointer-events: none; border-radius: 14px; border: 1px solid rgba(212,135,94,0.16); opacity: 0; box-shadow: inset 0 0 34px rgba(212,135,94,0.05); transition: opacity 0.32s cubic-bezier(0.16,1,0.3,1); }
.process-page.is-switching .top-stage::before { opacity: 0.32; transform: translateX(0); }
.process-page.is-switching .top-stage::after { opacity: 1; }
.process-page.is-switching .top-stage .stage-copy { animation: toolCopySwitch 0.48s cubic-bezier(0.16,1,0.3,1); }
.process-page.is-switching .stage-stats .stat-tile { animation: statSwitch 0.52s cubic-bezier(0.16,1,0.3,1); }
.process-page.is-switching .stage-stats .stat-tile:nth-child(2) { animation-delay: 0.04s; }
.process-page.is-switching .stage-stats .stat-tile:nth-child(3) { animation-delay: 0.08s; }
.stage-copy h2 { margin-top: 0.6rem; color: var(--text-primary); font-family: var(--font-display); font-size: clamp(2rem, 5vw, 4.4rem); line-height: 0.98; }
.stage-copy p { max-width: 28rem; margin-top: 0.85rem; color: var(--text-secondary); font-size: 0.95rem; }
.stage-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.55rem; }
.stat-tile { min-height: 82px; padding: 0.8rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); background: rgba(0,0,0,0.18); }
.stat-tile span { display: block; color: var(--text-primary); font-family: var(--font-mono); font-size: 1.1rem; }
.stat-tile small { color: var(--text-tertiary); font-size: 0.67rem; }
.work-card { position: relative; overflow: hidden; padding: 1.25rem; }
.work-card > * { position: relative; z-index: 1; }
.work-card::before { content: ''; position: absolute; inset: 0; pointer-events: none; opacity: 0; background: radial-gradient(circle at 14% 0%, rgba(212,135,94,0.12), transparent 16rem), linear-gradient(120deg, transparent 0 42%, rgba(212,135,94,0.055) 48%, transparent 58%); transform: translateX(-18px); transition: opacity 0.34s cubic-bezier(0.16,1,0.3,1), transform 0.44s cubic-bezier(0.16,1,0.3,1); }
.work-card:hover::before, .process-page.is-switching .work-card::before { opacity: 0.76; transform: translateX(0); }
.process-page.is-switching .work-card { animation: cardSwitch 0.46s cubic-bezier(0.16,1,0.3,1); }
.card-head { display: flex; gap: 0.65rem; margin-bottom: 1rem; align-items: flex-start; }
.card-mark { width: 0.55rem; height: 0.55rem; margin-top: 0.45rem; border-radius: 999px; background: var(--accent); box-shadow: 0 0 18px rgba(212,135,94,0.52); }
.card-head h3 { color: var(--text-primary); font-size: 0.95rem; }
.card-head p { color: var(--text-tertiary); font-size: 0.74rem; margin-top: 0.1rem; }
.analysis-grid, .result-card { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.65rem; }
.analysis-item, .result-card > div { padding: 0.8rem; border-radius: 12px; background: rgba(0,0,0,0.18); border: 1px solid rgba(255,255,255,0.055); min-width: 0; }
.analysis-item small, .result-card small { display: block; color: var(--text-tertiary); font-size: 0.66rem; }
.analysis-item strong, .result-card strong { display: block; color: var(--text-primary); font-size: 0.82rem; margin-top: 0.2rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.suggestions { list-style: none; display: grid; gap: 0.45rem; margin-top: 0.8rem; }
.suggestions li { color: var(--text-secondary); font-size: 0.76rem; padding-left: 0.6rem; border-left: 2px solid rgba(212,135,94,0.32); }
.control-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.8rem; }
.control-field { display: flex; flex-direction: column; gap: 0.55rem; padding: 0.85rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.055); background: rgba(0,0,0,0.16); }
.control-label { color: var(--text-secondary); font-size: 0.76rem; font-weight: 700; }
.control-input, .control-range { width: 100%; }
.control-input { min-height: 2.35rem; border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 0 0.7rem; color: var(--text-primary); background: rgba(0,0,0,0.28); outline: none; }
.control-input:focus { border-color: rgba(212,135,94,0.42); box-shadow: 0 0 0 3px rgba(212,135,94,0.08), inset 0 1px 0 rgba(255,255,255,0.035); }
.control-range { accent-color: var(--accent); }
.control-range:focus-visible { outline: none; filter: drop-shadow(0 0 10px rgba(212,135,94,0.24)); }
.range-row { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 0.5rem; }
.range-row small { color: var(--text-tertiary); font-size: 0.65rem; }
.range-row small:last-child { text-align: right; }
.range-row strong { color: var(--accent); font-family: var(--font-mono); font-size: 0.78rem; }
.chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.param-chip { min-height: 2rem; border: 1px solid rgba(255,255,255,0.075); border-radius: 10px; padding: 0 0.7rem; color: var(--text-tertiary); background: rgba(0,0,0,0.22); cursor: pointer; font-family: var(--font-mono); font-size: 0.68rem; transition: color 0.22s cubic-bezier(0.2,0.9,0.2,1), border-color 0.22s cubic-bezier(0.2,0.9,0.2,1), transform 0.22s cubic-bezier(0.2,0.9,0.2,1), background 0.22s cubic-bezier(0.2,0.9,0.2,1); }
.param-chip:not(.active):hover { color: var(--text-primary); border-color: rgba(212,135,94,0.5); transform: translateY(-1px); background: rgba(255,255,255,0.035); box-shadow: inset 0 0 0 1px rgba(212,135,94,0.16); }
.param-chip.active { color: var(--bg); border-color: var(--accent); background: var(--accent); transform: translateY(0); animation: chipSettle 0.24s cubic-bezier(0.16,1,0.3,1); }
.param-chip.active:hover { color: var(--bg); border-color: var(--accent); background: var(--accent); transform: translateY(0); box-shadow: none; }
.mode-note { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.65rem; margin-top: 0.85rem; padding: 0.85rem; border: 1px solid rgba(212,135,94,0.14); border-radius: 14px; background: linear-gradient(145deg, rgba(212,135,94,0.095), rgba(0,0,0,0.18)), rgba(255,255,255,0.025); box-shadow: inset 0 1px 0 rgba(255,255,255,0.045); }
.mode-note div { min-width: 0; padding-left: 0.65rem; border-left: 2px solid rgba(212,135,94,0.32); }
.mode-note small { display: block; color: var(--accent); font-family: var(--font-mono); font-size: 0.64rem; }
.mode-note p { margin-top: 0.22rem; color: var(--text-secondary); font-size: 0.74rem; line-height: 1.55; overflow-wrap: anywhere; }
.preview-shell { min-height: 220px; display: grid; place-items: center; border-radius: 14px; overflow: hidden; background: linear-gradient(135deg, rgba(0,0,0,0.26), rgba(212,135,94,0.035)), rgba(0,0,0,0.2); }
.preview-shell video, .preview-shell img, .preview-shell audio { width: 100%; max-height: 420px; display: block; }
.preview-shell img { height: 100%; object-fit: contain; }
.preview-shell audio { padding: 1.5rem; }
.file-stack { width: 100%; padding: 1rem; display: flex; flex-direction: column; gap: 0.55rem; }
.file-row { display: grid; grid-template-columns: 1.5rem 1fr auto; align-items: center; gap: 0.5rem; padding: 0.7rem; border-radius: 10px; color: var(--text-secondary); background: rgba(255,255,255,0.035); }
.file-row span { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.file-row small { color: var(--text-tertiary); font-family: var(--font-mono); }
.download-strip { display: flex; align-items: center; gap: 0.6rem; margin-top: 1rem; flex-wrap: wrap; }
.download-strip span { display: inline-flex; align-items: center; gap: 0.35rem; color: #66c28c; font-size: 0.8rem; font-weight: 700; margin-right: auto; }
.download-strip button { min-height: 2.2rem; border: 0; border-radius: 10px; padding: 0 0.9rem; color: var(--bg); background: var(--accent); cursor: pointer; font-weight: 700; }
.download-strip .ghost { color: var(--text-secondary); border: 1px solid rgba(255,255,255,0.08); background: rgba(255,255,255,0.04); }
.side-panel { display: flex; flex-direction: column; gap: 1rem; }
.visual-card { min-height: 360px; position: relative; overflow: hidden; }
.process-page.is-switching .visual-card { animation: sideVisualSwitch 0.54s cubic-bezier(0.16,1,0.3,1); }
.visual-card :deep(.media-visual) { min-height: 360px; }
.visual-overlay { position: absolute; left: 1rem; right: 1rem; bottom: 1rem; display: flex; justify-content: space-between; align-items: end; gap: 1rem; padding-top: 5rem; background: linear-gradient(180deg, transparent, rgba(0,0,0,0.72)); }
.visual-overlay span { color: var(--text-secondary); font-size: 0.72rem; }
.visual-overlay strong { color: var(--text-primary); font-family: var(--font-display); font-size: 1.4rem; }
.side-card { padding: 1rem; }
.side-card h3 { display: flex; align-items: center; gap: 0.4rem; color: var(--text-primary); font-size: 0.86rem; margin-bottom: 0.75rem; }
.side-card ul { list-style: none; display: flex; flex-direction: column; gap: 0.55rem; }
.side-card li { padding-left: 0.65rem; border-left: 2px solid rgba(212,135,94,0.28); color: var(--text-tertiary); font-size: 0.74rem; line-height: 1.55; }
.log-list { display: flex; flex-direction: column; gap: 0.45rem; }
.log-row { display: grid; grid-template-columns: 0.55rem 1fr auto; gap: 0.5rem; align-items: center; color: var(--text-tertiary); }
.log-row span { width: 0.42rem; height: 0.42rem; border-radius: 50%; background: rgba(255,255,255,0.18); }
.log-row.active span { background: var(--accent); }
.log-row.done span { background: #66c28c; }
.log-row.error span { background: #de6b5f; }
.log-row p { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.7rem; }
.log-row small { color: var(--text-tertiary); font-family: var(--font-mono); font-size: 0.6rem; }

@keyframes workspaceEnter {
  from {
    opacity: 0;
    transform: translateY(18px);
    filter: brightness(0.86) blur(2px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
    filter: brightness(1) blur(0);
  }
}

@keyframes toolCopySwitch {
  0% {
    opacity: 0.55;
    transform: translateY(12px);
    filter: brightness(0.82);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
    filter: brightness(1);
  }
}

@keyframes statSwitch {
  0% {
    transform: translateY(8px) scale(0.98);
    border-color: rgba(212,135,94,0.12);
  }
  100% {
    transform: translateY(0) scale(1);
    border-color: rgba(255,255,255,0.06);
  }
}

@keyframes cardSwitch {
  0% {
    transform: translateY(8px);
    border-color: rgba(212,135,94,0.22);
  }
  100% {
    transform: translateY(0);
    border-color: rgba(255,255,255,0.06);
  }
}

@keyframes sideVisualSwitch {
  0% {
    transform: translateX(12px) scale(0.985);
    filter: brightness(0.82);
  }
  100% {
    transform: translateX(0) scale(1);
    filter: brightness(1);
  }
}

@keyframes railLinePulse {
  from {
    filter: brightness(0.78);
  }
  to {
    filter: brightness(1.18);
  }
}

@keyframes chipSettle {
  0% {
    transform: translateY(1px) scale(0.96);
  }
  70% {
    transform: translateY(-1px) scale(1.03);
  }
  100% {
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 1180px) { .process-page { grid-template-columns: 220px minmax(0, 1fr); } .side-panel { display: none; } }
@media (max-width: 820px) {
  .process-page { min-height: calc(100vh - 3.85rem); display: flex; flex-direction: column; padding: 0.75rem; }
  .process-page::before { inset: 3.85rem 0 0; }
  .tool-rail { position: relative; top: auto; height: auto; }
  .media-switch { display: flex; overflow-x: auto; scrollbar-width: none; }
  .media-switch::-webkit-scrollbar { display: none; }
  .media-switch-link { min-width: 5.4rem; }
  .rail-nav { flex-direction: row; overflow-x: auto; padding-bottom: 0.35rem; }
  .tool-pill { min-width: 210px; }
  .top-stage, .analysis-grid, .result-card, .control-grid, .mode-note { grid-template-columns: 1fr; }
  .stage-stats { grid-template-columns: repeat(3, 1fr); }
}
</style>
