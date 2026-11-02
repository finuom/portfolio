<script setup>
import { ref } from 'vue'

defineProps({ project: Object })

// Inclinação 3D + "lanterna" que segue o cursor.
const card = ref(null)
function onMove(e) {
  const el = card.value
  const r = el.getBoundingClientRect()
  const x = (e.clientX - r.left) / r.width
  const y = (e.clientY - r.top) / r.height
  el.style.setProperty('--mx', `${x * 100}%`)
  el.style.setProperty('--my', `${y * 100}%`)
  el.style.transform = `perspective(900px) rotateX(${(0.5 - y) * 7}deg) rotateY(${(x - 0.5) * 9}deg) translateY(-4px)`
}
function onLeave() {
  card.value.style.transform = ''
}

const fmt = (iso) => new Date(iso).toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' })
</script>

<template>
  <component
    :is="project.url ? 'a' : 'article'"
    ref="card"
    class="card glass"
    :class="{ featured: project.featured }"
    :href="project.url || undefined"
    :target="project.url ? '_blank' : undefined"
    rel="noopener"
    @mousemove="onMove"
    @mouseleave="onLeave"
  >
    <div class="spot"></div>
    <header>
      <span class="cat">{{ project.category }}</span>
      <span v-if="project.private" class="priv">🔒 privado</span>
      <span v-else class="arrow" aria-hidden="true">↗</span>
    </header>
    <h3>{{ project.title }}</h3>
    <p>{{ project.description || 'Sem descrição ainda.' }}</p>

    <div class="tags">
      <span v-for="t in project.tags" :key="t">{{ t }}</span>
    </div>

    <div class="langbar" v-if="project.languages.length">
      <i v-for="l in project.languages" :key="l.name" :style="{ width: l.percent + '%', background: l.color }" :title="`${l.name} ${l.percent}%`"></i>
    </div>
    <footer>
      <span class="langs">
        <span v-for="l in project.languages.slice(0, 3)" :key="l.name"><i :style="{ background: l.color }"></i>{{ l.name }}</span>
      </span>
      <span class="date">{{ fmt(project.pushed_at) }}</span>
    </footer>
  </component>
</template>

<style scoped>
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 24px;
  overflow: hidden;
  transition: transform 0.25s ease-out, border-color 0.3s, box-shadow 0.3s;
  will-change: transform;
}
.card:hover {
  border-color: var(--border-strong);
  box-shadow: 0 20px 50px -20px rgba(167, 139, 250, 0.45);
}
.spot {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(380px circle at var(--mx, 50%) var(--my, 0%), rgba(34, 211, 238, 0.12), transparent 45%);
  opacity: 0;
  transition: opacity 0.3s;
}
.card:hover .spot {
  opacity: 1;
}
.featured::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: var(--grad);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.55;
  pointer-events: none;
}
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.cat {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: var(--cyan);
  padding: 4px 10px;
  border-radius: 99px;
  background: rgba(34, 211, 238, 0.08);
  border: 1px solid rgba(34, 211, 238, 0.2);
}
.priv {
  font-size: 0.78rem;
  color: var(--muted);
}
.arrow {
  font-size: 1.2rem;
  color: var(--muted);
  transition: transform 0.3s, color 0.3s;
}
.card:hover .arrow {
  transform: translate(3px, -3px);
  color: var(--cyan);
}
h3 {
  margin: 0 0 10px;
  font-size: 1.3rem;
  letter-spacing: -0.01em;
}
p {
  color: var(--muted);
  line-height: 1.6;
  margin: 0 0 18px;
  font-size: 0.95rem;
  flex: 1;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 18px;
}
.tags span {
  font-size: 0.75rem;
  padding: 3px 9px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  color: #c9cbe3;
}
.langbar {
  display: flex;
  height: 4px;
  border-radius: 99px;
  overflow: hidden;
  margin-bottom: 12px;
  background: rgba(255, 255, 255, 0.05);
}
footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--muted);
  font-family: var(--mono);
}
.langs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.langs span {
  display: flex;
  align-items: center;
  gap: 5px;
}
.langs i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
</style>
