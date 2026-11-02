<script setup>
import { computed, ref } from 'vue'

const props = defineProps({ languages: Array })
const hovered = ref(null)

// Constelação: cada linguagem é uma estrela; o tamanho vem da presença dela
// nos projetos. Posições numa espiral áurea, ligadas às vizinhas mais próximas.
const SIZE = 420
const nodes = computed(() => {
  const max = Math.max(...props.languages.map((l) => l.percent), 1)
  return props.languages.map((l, i) => {
    const a = i * 2.39996
    const rad = 34 + Math.sqrt(i) * 54
    return {
      ...l,
      x: SIZE / 2 + Math.cos(a) * rad,
      y: SIZE / 2 + Math.sin(a) * rad,
      r: 6 + (l.percent / max) * 18,
      delay: (i * 0.37) % 4,
    }
  })
})

const links = computed(() => {
  const out = []
  const ns = nodes.value
  ns.forEach((a, i) => {
    const near = ns
      .map((b, j) => ({ j, d: Math.hypot(a.x - b.x, a.y - b.y) }))
      .filter((o) => o.j !== i)
      .sort((p, q) => p.d - q.d)
      .slice(0, 2)
    for (const { j } of near) if (i < j || !near.some((n) => n.j === i)) out.push([a, ns[j]])
  })
  return out
})

const top = computed(() => props.languages.slice(0, 8))
</script>

<template>
  <section id="skills">
    <div class="container">
      <p class="section-label" v-reveal>// tecnologias</p>
      <h2 class="section-title" v-reveal="60">Minha <span class="grad-text">constelação</span> de linguagens</h2>
      <p class="sub" v-reveal="100">
        Calculado a partir do código de todos os meus repositórios — públicos e privados. Cada projeto pesa igual, então um notebook gigante não esconde o resto.
      </p>

      <div class="skills-grid">
        <div class="constellation" v-reveal="140">
          <svg :viewBox="`0 0 ${SIZE} ${SIZE}`" role="img" aria-label="Constelação de linguagens">
            <defs>
              <radialGradient id="glow">
                <stop offset="0" stop-color="#fff" stop-opacity=".9" />
                <stop offset="1" stop-color="#fff" stop-opacity="0" />
              </radialGradient>
            </defs>
            <line
              v-for="([a, b], i) in links"
              :key="'l' + i"
              :x1="a.x" :y1="a.y" :x2="b.x" :y2="b.y"
              class="link"
              :class="{ lit: hovered === a.name || hovered === b.name }"
            />
            <g
              v-for="n in nodes"
              :key="n.name"
              class="node"
              :class="{ dim: hovered && hovered !== n.name }"
              :style="{ animationDelay: `-${n.delay}s` }"
              @mouseenter="hovered = n.name"
              @mouseleave="hovered = null"
            >
              <circle :cx="n.x" :cy="n.y" :r="n.r * 2.2" :fill="n.color" opacity=".18" />
              <circle :cx="n.x" :cy="n.y" :r="n.r" :fill="n.color" />
              <circle :cx="n.x - n.r * 0.3" :cy="n.y - n.r * 0.3" :r="n.r * 0.45" fill="url(#glow)" opacity=".6" />
              <text :x="n.x" :y="n.y + n.r + 15" text-anchor="middle">{{ n.name }}</text>
            </g>
          </svg>
        </div>

        <ul class="bars">
          <li
            v-for="(l, i) in top"
            :key="l.name"
            v-reveal="i * 60"
            :class="{ active: hovered === l.name }"
            @mouseenter="hovered = l.name"
            @mouseleave="hovered = null"
          >
            <div class="row">
              <span class="name"><i :style="{ background: l.color }"></i>{{ l.name }}</span>
              <span class="pct">{{ l.percent.toFixed(1) }}%</span>
            </div>
            <div class="track">
              <div class="fill" :style="{ width: l.percent / top[0].percent * 100 + '%', background: `linear-gradient(90deg, ${l.color}, var(--violet))` }"></div>
            </div>
            <small>em {{ l.repos }} {{ l.repos === 1 ? 'projeto' : 'projetos' }}</small>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<style scoped>
.sub {
  color: var(--muted);
  max-width: 620px;
  line-height: 1.6;
  margin: 0 0 40px;
}
.skills-grid {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 48px;
  align-items: center;
}
.constellation svg {
  width: 100%;
  height: auto;
  overflow: visible;
}
.link {
  stroke: rgba(167, 139, 250, 0.28);
  stroke-width: 1;
  transition: stroke 0.3s;
}
.link.lit {
  stroke: rgba(34, 211, 238, 0.9);
  stroke-width: 1.6;
}
.node {
  cursor: default;
  animation: twinkle 4s ease-in-out infinite;
  transition: opacity 0.3s;
  transform-box: fill-box;
}
.node.dim {
  opacity: 0.3;
}
.node text {
  fill: var(--text);
  font-family: var(--mono);
  font-size: 11px;
}
@keyframes twinkle {
  50% { filter: brightness(1.35); }
}

.bars {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 18px;
}
.bars li {
  transition: transform 0.25s;
}
.bars li.active {
  transform: translateX(6px);
}
.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 7px;
}
.name {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}
.name i {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.pct {
  font-family: var(--mono);
  color: var(--muted);
  font-size: 0.9rem;
}
.track {
  height: 8px;
  border-radius: 99px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}
.fill {
  height: 100%;
  border-radius: 99px;
  transition: width 1s cubic-bezier(0.2, 0.7, 0.2, 1);
}
.bars small {
  color: var(--muted);
  font-size: 0.78rem;
}

@media (max-width: 860px) {
  .skills-grid {
    grid-template-columns: 1fr;
  }
}
</style>
