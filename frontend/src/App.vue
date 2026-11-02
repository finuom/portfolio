<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { usePortfolio } from './api'
import ParticleField from './components/ParticleField.vue'
import HeroSection from './components/HeroSection.vue'
import AboutSection from './components/AboutSection.vue'
import SkillsSection from './components/SkillsSection.vue'
import ProjectsSection from './components/ProjectsSection.vue'
import ContactSection from './components/ContactSection.vue'

const { data, live, error } = usePortfolio()

const links = [
  ['#sobre', 'Sobre'],
  ['#skills', 'Tecnologias'],
  ['#projetos', 'Projetos'],
  ['#contato', 'Contato'],
]
const scrolled = ref(false)
const onScroll = () => (scrolled.value = window.scrollY > 30)
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <ParticleField />

  <nav :class="{ scrolled }">
    <div class="container nav-inner">
      <a href="#inicio" class="logo"><span class="grad-text">&lt;</span>mounif<span class="grad-text">/&gt;</span></a>
      <div class="nav-links">
        <a v-for="[href, label] in links" :key="href" :href="href">{{ label }}</a>
      </div>
    </div>
  </nav>

  <main v-if="data">
    <HeroSection :profile="data.profile" :stats="data.stats" />
    <AboutSection :profile="data.profile" :stats="data.stats" :timeline="data.timeline" />
    <SkillsSection :languages="data.languages" />
    <ProjectsSection :projects="data.projects" />
    <ContactSection :profile="data.profile" :generated-at="data.generated_at" :live="live" />
  </main>

  <div v-else class="loading">
    <div class="loader"></div>
    <p v-if="error">Não foi possível carregar os dados ({{ error }}).</p>
    <p v-else>Conectando os pontos…</p>
  </div>
</template>

<style scoped>
nav {
  position: fixed;
  inset: 0 0 auto;
  z-index: 10;
  padding: 20px 0;
  transition: padding 0.3s, background 0.3s, border-color 0.3s;
  border-bottom: 1px solid transparent;
}
nav.scrolled {
  padding: 12px 0;
  background: rgba(7, 7, 15, 0.7);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-color: var(--border);
}
.nav-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-family: var(--mono);
  font-weight: 500;
  font-size: 1.1rem;
}
.nav-links {
  display: flex;
  gap: 28px;
}
.nav-links a {
  color: var(--muted);
  font-size: 0.95rem;
  position: relative;
  transition: color 0.2s;
}
.nav-links a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  height: 2px;
  width: 100%;
  background: var(--grad);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s;
}
.nav-links a:hover {
  color: var(--text);
}
.nav-links a:hover::after {
  transform: scaleX(1);
}
main {
  position: relative;
  z-index: 1;
}
.loading {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: grid;
  place-content: center;
  justify-items: center;
  gap: 18px;
  color: var(--muted);
  font-family: var(--mono);
}
.loader {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: var(--cyan);
  animation: spin 0.9s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
@media (max-width: 640px) {
  .nav-links {
    gap: 16px;
  }
  .nav-links a:nth-child(2) {
    display: none;
  }
  .nav-links a {
    font-size: 0.88rem;
  }
}
</style>
