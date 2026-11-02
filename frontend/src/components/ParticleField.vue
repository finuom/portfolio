<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'

// Fundo de partículas conectadas: pontos que se movem devagar e se ligam por
// linhas quando estão perto. O mouse puxa os pontos e cria ligações próprias;
// um clique solta uma pequena explosão de novos pontos.
const canvas = ref(null)

const LINK_DIST = 130
const MOUSE_DIST = 190
const MAX_PARTICLES = 220

let ctx, w, h, dpr, raf
let particles = []
const mouse = { x: -9999, y: -9999, active: false }
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

function hueFor(x) {
  // ciano (190) à esquerda → violeta (265) à direita
  return 190 + (x / w) * 75
}

function spawn(x = Math.random() * w, y = Math.random() * h, speed = 0.35) {
  const a = Math.random() * Math.PI * 2
  const s = (0.3 + Math.random()) * speed
  return { x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, r: 1 + Math.random() * 1.8, life: Infinity }
}

function resize() {
  dpr = Math.min(window.devicePixelRatio || 1, 2)
  w = window.innerWidth
  h = window.innerHeight
  canvas.value.width = w * dpr
  canvas.value.height = h * dpr
  canvas.value.style.width = w + 'px'
  canvas.value.style.height = h + 'px'
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  const target = Math.min(Math.round((w * h) / 9500), 150)
  particles = particles.filter((p) => p.x < w && p.y < h).slice(0, target)
  while (particles.length < target) particles.push(spawn())
}

function step() {
  for (const p of particles) {
    if (mouse.active) {
      const dx = mouse.x - p.x
      const dy = mouse.y - p.y
      const d = Math.hypot(dx, dy)
      if (d < MOUSE_DIST && d > 1) {
        // atração suave, com repulsão bem de perto para não aglomerar
        const f = d < 50 ? -0.04 : 0.012 * (1 - d / MOUSE_DIST)
        p.vx += (dx / d) * f
        p.vy += (dy / d) * f
      }
    }
    // atrito leve de volta para a velocidade de cruzeiro
    const sp = Math.hypot(p.vx, p.vy)
    if (sp > 0.6) {
      p.vx *= 0.97
      p.vy *= 0.97
    }
    p.x += p.vx
    p.y += p.vy
    if (p.x < -10) p.x = w + 10
    if (p.x > w + 10) p.x = -10
    if (p.y < -10) p.y = h + 10
    if (p.y > h + 10) p.y = -10
    if (p.life !== Infinity) p.life -= 1
  }
  particles = particles.filter((p) => p.life > 0)
}

function draw() {
  ctx.clearRect(0, 0, w, h)
  const n = particles.length

  ctx.lineWidth = 0.8
  for (let i = 0; i < n; i++) {
    const a = particles[i]
    for (let j = i + 1; j < n; j++) {
      const b = particles[j]
      const dx = a.x - b.x
      if (dx > LINK_DIST || dx < -LINK_DIST) continue
      const dy = a.y - b.y
      if (dy > LINK_DIST || dy < -LINK_DIST) continue
      const d2 = dx * dx + dy * dy
      if (d2 < LINK_DIST * LINK_DIST) {
        const alpha = 1 - Math.sqrt(d2) / LINK_DIST
        ctx.strokeStyle = `hsla(${hueFor((a.x + b.x) / 2)}, 90%, 65%, ${alpha * 0.35})`
        ctx.beginPath()
        ctx.moveTo(a.x, a.y)
        ctx.lineTo(b.x, b.y)
        ctx.stroke()
      }
    }
  }

  if (mouse.active) {
    ctx.lineWidth = 1
    for (const p of particles) {
      const d = Math.hypot(mouse.x - p.x, mouse.y - p.y)
      if (d < MOUSE_DIST) {
        ctx.strokeStyle = `hsla(${hueFor(p.x)}, 95%, 72%, ${(1 - d / MOUSE_DIST) * 0.6})`
        ctx.beginPath()
        ctx.moveTo(mouse.x, mouse.y)
        ctx.lineTo(p.x, p.y)
        ctx.stroke()
      }
    }
  }

  for (const p of particles) {
    const fade = p.life === Infinity ? 1 : Math.min(1, p.life / 60)
    ctx.fillStyle = `hsla(${hueFor(p.x)}, 95%, 75%, ${0.85 * fade})`
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
    ctx.fill()
  }
}

function loop() {
  step()
  draw()
  raf = requestAnimationFrame(loop)
}

function onMove(e) {
  mouse.x = e.clientX
  mouse.y = e.clientY
  mouse.active = true
}
function onLeave() {
  mouse.active = false
}
function onClick(e) {
  if (e.target.closest('a, button, input, .card')) return
  for (let i = 0; i < 8 && particles.length < MAX_PARTICLES; i++) {
    const p = spawn(e.clientX, e.clientY, 2.4)
    p.life = 420 + Math.random() * 240
    particles.push(p)
  }
}
function onVisibility() {
  cancelAnimationFrame(raf)
  if (!document.hidden && !reduceMotion) loop()
}

onMounted(() => {
  ctx = canvas.value.getContext('2d')
  resize()
  window.addEventListener('resize', resize)
  if (reduceMotion) {
    draw()
    return
  }
  window.addEventListener('pointermove', onMove)
  document.addEventListener('pointerleave', onLeave)
  window.addEventListener('click', onClick)
  document.addEventListener('visibilitychange', onVisibility)
  loop()
})

onBeforeUnmount(() => {
  cancelAnimationFrame(raf)
  window.removeEventListener('resize', resize)
  window.removeEventListener('pointermove', onMove)
  document.removeEventListener('pointerleave', onLeave)
  window.removeEventListener('click', onClick)
  document.removeEventListener('visibilitychange', onVisibility)
})
</script>

<template>
  <canvas ref="canvas" class="particles" aria-hidden="true"></canvas>
</template>

<style scoped>
.particles {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
</style>
