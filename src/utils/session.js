export const AUTH_TOKEN_KEY = 'vlade_auth_token'
export const AUTH_USER_KEY = 'vlade_user'
export const AUTH_CHANGE_EVENT = 'vlade-auth-change'

export function getToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY) || ''
}

export function getStoredUser() {
  try {
    return JSON.parse(localStorage.getItem(AUTH_USER_KEY) || 'null')
  } catch {
    return null
  }
}

export function hasAuthSession() {
  return Boolean(getToken())
}

export function notifyAuthChange() {
  window.dispatchEvent(new Event(AUTH_CHANGE_EVENT))
}

export function storeSession(token, user) {
  localStorage.setItem(AUTH_TOKEN_KEY, token)
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify(user))
  notifyAuthChange()
}

export function clearSession() {
  localStorage.removeItem(AUTH_TOKEN_KEY)
  localStorage.removeItem(AUTH_USER_KEY)
  notifyAuthChange()
}

export function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export function safeRedirectPath(rawPath, fallback = '/video') {
  if (typeof rawPath !== 'string') return fallback
  const path = rawPath.trim()
  if (!path || !path.startsWith('/') || path.startsWith('//')) return fallback
  if (path.startsWith('/auth')) return fallback
  if (path.startsWith('/api')) return fallback
  return path
}

export function authRouteFor(path) {
  return {
    path: '/auth',
    query: { redirect: safeRedirectPath(path) },
  }
}
