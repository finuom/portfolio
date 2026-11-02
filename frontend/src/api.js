import { ref } from 'vue'

const API_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

// Mostra primeiro o snapshot estático (instantâneo) e depois troca pelos dados
// ao vivo da API, para a página nunca abrir vazia enquanto a função "acorda".
export function usePortfolio() {
  const data = ref(null)
  const live = ref(false)
  const error = ref(null)

  fetch('/snapshot.json')
    .then((r) => (r.ok ? r.json() : null))
    .then((snap) => {
      if (snap && !data.value) data.value = snap
    })
    .catch(() => {})

  const loadLive = async (attempt = 0) => {
    try {
      const r = await fetch(`${API_URL}/api/portfolio`)
      if (!r.ok) throw new Error(`HTTP ${r.status}`)
      data.value = await r.json()
      live.value = true
    } catch (e) {
      if (attempt < 4) setTimeout(() => loadLive(attempt + 1), 4000 * (attempt + 1))
      else if (!data.value) error.value = e.message
    }
  }
  loadLive()

  return { data, live, error }
}
