import { authHeaders, clearSession } from '../utils/session.js'

const LOCAL_API_BASE = '/api'

function normalizeApiBase(rawBase) {
  const base = String(rawBase || LOCAL_API_BASE).trim().replace(/\/+$/, '')
  if (!base) return LOCAL_API_BASE

  // 线上如果只填后端域名，自动补 /api，因为 FastAPI 路由统一挂在 /api 下。
  if (/^https?:\/\//i.test(base)) {
    try {
      const url = new URL(base)
      if (!url.pathname || url.pathname === '/') {
        url.pathname = LOCAL_API_BASE
        return url.toString().replace(/\/+$/, '')
      }
    } catch {
      return LOCAL_API_BASE
    }
  }

  return base
}

const BASE = normalizeApiBase(import.meta.env.VITE_API_BASE_URL)
const API_CONNECT_ERROR = '后端接口没有连上，请确认后端已启动，或在 Netlify 配置 VITE_API_BASE_URL 指向 FastAPI 后端。'

async function apiFetch(path, options = {}) {
  const url = path.startsWith('http') ? path : `${BASE}${path}`
  try {
    return await fetch(url, options)
  } catch {
    throw new Error(API_CONNECT_ERROR)
  }
}

async function readJson(res) {
  const contentType = res.headers.get('content-type') || ''
  if (!contentType.includes('application/json')) {
    throw new Error(API_CONNECT_ERROR)
  }
  return res.json()
}

function appendPayload(form, fileOrFiles, multi = false) {
  const files = Array.isArray(fileOrFiles) ? fileOrFiles : [fileOrFiles]
  const field = multi ? 'files' : 'file'
  for (const file of files) form.append(field, file)
}

async function readError(res) {
  let detail = ''
  const contentType = res.headers.get('content-type') || ''
  try {
    if (contentType.includes('application/json')) {
      const body = await res.json()
      detail = body.detail || ''
    } else {
      const text = await res.text()
      if (text.trim().startsWith('<')) {
        detail = API_CONNECT_ERROR
      }
    }
  } catch {
    detail = ''
  }
  if (res.status === 401) {
    clearSession()
    return detail && !['请先登录', '登录已过期'].includes(detail)
      ? detail
      : '请先登录后再处理文件'
  }
  if (res.status === 404 || res.status >= 500) {
    return detail || API_CONNECT_ERROR
  }
  return detail || '处理失败'
}

async function requestJson(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...authHeaders(),
    ...(options.headers || {}),
  }

  const res = await apiFetch(path, {
    ...options,
    headers,
  })
  if (!res.ok) throw new Error(await readError(res))
  return readJson(res)
}

async function uploadMedia(kind, endpoint, fileOrFiles, params = {}, options = {}) {
  const form = new FormData()
  appendPayload(form, fileOrFiles, options.multi)
  for (const [key, value] of Object.entries(params)) {
    form.append(key, String(value))
  }

  const res = await apiFetch(`/${kind}/${endpoint}`, {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  })
  if (!res.ok) throw new Error(await readError(res))
  return readJson(res)
}

export async function analyzeMedia(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await apiFetch('/analyze', {
    method: 'POST',
    headers: authHeaders(),
    body: form,
  })
  if (!res.ok) throw new Error(await readError(res))
  return readJson(res)
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
  const res = await apiFetch(`/download/${filename}`, { headers: authHeaders() })
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
      const res = await apiFetch(`/video/progress/${taskId}`, { headers: authHeaders() })
      if (!res.ok) {
        clearInterval(interval)
        onError?.(new Error(await readError(res)))
        return
      }
      const data = await readJson(res)
      onProgress?.(data)
      if (data.done) { clearInterval(interval); onDone?.(data) }
    } catch (error) {
      clearInterval(interval)
      onError?.(error)
    }
  }, 600)
  return () => clearInterval(interval)
}
