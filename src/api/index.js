const BASE = '/api'

function appendPayload(form, fileOrFiles, multi = false) {
  const files = Array.isArray(fileOrFiles) ? fileOrFiles : [fileOrFiles]
  const field = multi ? 'files' : 'file'
  for (const file of files) form.append(field, file)
}

async function readError(res) {
  try {
    const body = await res.json()
    return body.detail || '处理失败'
  } catch {
    return '处理失败'
  }
}

async function uploadMedia(kind, endpoint, fileOrFiles, params = {}, options = {}) {
  const form = new FormData()
  appendPayload(form, fileOrFiles, options.multi)
  for (const [key, value] of Object.entries(params)) {
    form.append(key, String(value))
  }

  const res = await fetch(`${BASE}/${kind}/${endpoint}`, {
    method: 'POST',
    body: form,
  })
  if (!res.ok) throw new Error(await readError(res))
  return res.json()
}

export async function analyzeMedia(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${BASE}/analyze`, { method: 'POST', body: form })
  if (!res.ok) throw new Error(await readError(res))
  return res.json()
}

export function uploadVideo(endpoint, fileOrFiles, params = {}, options = {}) {
  return uploadMedia('video', endpoint, fileOrFiles, params, options)
}

export function uploadAudio(endpoint, fileOrFiles, params = {}, options = {}) {
  return uploadMedia('audio', endpoint, fileOrFiles, params, options)
}

export function uploadImage(endpoint, fileOrFiles, params = {}, options = {}) {
  return uploadMedia('image', endpoint, fileOrFiles, params, options)
}

export function downloadUrl(filename) {
  return `${BASE}/download/${filename}`
}

export function pollProgress(taskId, onProgress, onDone, onError) {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`${BASE}/video/progress/${taskId}`)
      if (!res.ok) { clearInterval(interval); onError?.(); return }
      const data = await res.json()
      onProgress?.(data)
      if (data.done) { clearInterval(interval); onDone?.(data) }
    } catch { /* retry next tick */ }
  }, 600)
  return () => clearInterval(interval)
}
