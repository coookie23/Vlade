import { authHeaders, clearSession } from '../utils/session.js'

const BASE = '/api'

function appendPayload(form, fileOrFiles, multi = false) {
  const files = Array.isArray(fileOrFiles) ? fileOrFiles : [fileOrFiles]
  const field = multi ? 'files' : 'file'
  for (const file of files) form.append(field, file)
}

async function readError(res) {
  let detail = ''
  try {
    const body = await res.json()
    detail = body.detail || ''
  } catch {
    detail = ''
  }
  if (res.status === 401) {
    clearSession()
    return detail && !['请先登录', '登录已过期'].includes(detail)
      ? detail
      : '请先登录后再处理文件'
  }
  return detail || '处理失败'
}

async function requestJson(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...authHeaders(),
    ...(options.headers || {}),
  }

  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers,
  })
  if (!res.ok) throw new Error(await readError(res))
  return res.json()
}

async function uploadMedia(kind, endpoint, fileOrFiles, params = {}, options = {}) {
  const form = new FormData()
  appendPayload(form, fileOrFiles, options.multi)
  for (const [key, value] of Object.entries(params)) {
    form.append(key, String(value))
  }

  const res = await fetch(`${BASE}/${kind}/${endpoint}`, {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  })
  if (!res.ok) throw new Error(await readError(res))
  return res.json()
}

export async function analyzeMedia(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${BASE}/analyze`, {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  })
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

export async function downloadFile(filename) {
  const res = await fetch(downloadUrl(filename), { headers: authHeaders() })
  if (!res.ok) throw new Error(await readError(res))
  return res.blob()
}

export async function registerUser(payload) {
  return requestJson('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function loginUser(payload) {
  return requestJson('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export async function getCurrentUser() {
  return requestJson('/auth/me')
}

export async function logoutUser() {
  return requestJson('/auth/logout', { method: 'POST' })
}

export function pollProgress(taskId, onProgress, onDone, onError) {
  const interval = setInterval(async () => {
    try {
      const res = await fetch(`${BASE}/video/progress/${taskId}`, { headers: authHeaders() })
      if (!res.ok) {
        clearInterval(interval)
        onError?.(new Error(await readError(res)))
        return
      }
      const data = await res.json()
      onProgress?.(data)
      if (data.done) { clearInterval(interval); onDone?.(data) }
    } catch (error) {
      clearInterval(interval)
      onError?.(error)
    }
  }, 600)
  return () => clearInterval(interval)
}
