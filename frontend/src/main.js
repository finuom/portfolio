import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

const app = createApp(App)

// v-reveal: anima o elemento quando ele entra na tela.
const observer = new IntersectionObserver(
  (entries) => {
    for (const e of entries) {
      if (e.isIntersecting) {
        e.target.classList.add('revealed')
        observer.unobserve(e.target)
      }
    }
  },
  { threshold: 0.12 },
)
app.directive('reveal', {
  mounted(el, binding) {
    el.classList.add('reveal')
    if (binding.value) el.style.transitionDelay = `${binding.value}ms`
    observer.observe(el)
  },
})

app.mount('#app')
