<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps({ profile: Object, stats: Object })

// Efeito de digitação alternando entre os papéis do perfil.
const typed = ref('')
let timer
function typeLoop(roles, i = 0, pos = 0, deleting = false) {
  const word = roles[i % roles.length]
  typed.value = word.slice(0, pos)
  let next = 70
  if (!deleting && pos === word.length) {
    deleting = true
    next = 1800
  } else if (deleting && pos === 0) {
    deleting = false
    i++
    next = 350
  } else {
    pos += deleting ? -1 : 1
    next = deleting ? 35 : 70
  }
  timer = setTimeout(() => typeLoop(roles, i, pos, deleting), next)
}

function start() {
  clearTimeout(timer)
  const roles = props.profile?.roles?.length ? props.profile.roles : [props.profile?.headline || '']
  typeLoop(roles)
}
onMounted(start)
watch(() => props.profile?.roles?.join('|'), start)
onBeforeUnmount(() => clearTimeout(timer))
</script>

<template>
  <section id="inicio" class="hero">
    <div class="container hero-grid">
      <div class="hero-text">
        <p class="hello" v-reveal>
          <span class="dot"></span> Olá, eu sou
        </p>
        <h1 v-reveal="80">
          <span class="grad-text">{{ profile.name }}</span>
        </h1>
        <p class="typed" v-reveal="160">
          <span class="prompt">&gt;</span> {{ typed }}<span class="caret">▍</span>
        </p>
        <p class="bio" v-reveal="240">{{ profile.headline }}</p>
        <div class="cta" v-reveal="320">
          <a href="#projetos" class="btn btn-primary">Ver projetos →</a>
          <a :href="profile.html_url" target="_blank" rel="noopener" class="btn btn-ghost">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.37-3.88-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.71.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.7 1.26 3.36.96.1-.75.4-1.26.73-1.55-2.55-.29-5.24-1.28-5.24-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.77.11 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.7 5.4-5.26 5.69.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/></svg>
            @{{ profile.login }}
          </a>
        </div>
      </div>

      <div class="avatar-wrap" v-reveal="200">
        <div class="ring"></div>
        <div class="orbit o1"><span></span></div>
        <div class="orbit o2"><span></span></div>
        <img :src="profile.avatar_url" :alt="profile.name" class="avatar" width="260" height="260" />
        <div class="badge glass">
          <strong>{{ stats.repos }}</strong> repositórios<br />
          <small>{{ stats.private }} privados · {{ stats.languages }} linguagens</small>
        </div>
      </div>
    </div>
    <a href="#sobre" class="scroll-hint" aria-label="Rolar para baixo"><span></span></a>
  </section>
</template>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: 120px;
}
.hero-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: 48px;
  align-items: center;
}
.hello {
  font-family: var(--mono);
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #4ade80;
  box-shadow: 0 0 12px #4ade80;
  animation: pulse 2s infinite;
}
h1 {
  font-size: clamp(2.6rem, 7vw, 5rem);
  line-height: 1.02;
  letter-spacing: -0.035em;
  margin: 0 0 18px;
  font-weight: 700;
}
.typed {
  font-family: var(--mono);
  font-size: clamp(1rem, 2.2vw, 1.3rem);
  color: var(--text);
  min-height: 1.6em;
  margin: 0 0 20px;
}
.prompt {
  color: var(--cyan);
}
.caret {
  color: var(--violet);
  animation: blink 1s steps(1) infinite;
}
.bio {
  color: var(--muted);
  font-size: 1.1rem;
  max-width: 520px;
  line-height: 1.6;
  margin: 0 0 32px;
}
.cta {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.avatar-wrap {
  position: relative;
  width: min(340px, 80vw);
  aspect-ratio: 1;
  justify-self: center;
  display: grid;
  place-items: center;
}
.ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: conic-gradient(from 0deg, var(--cyan), var(--violet), var(--pink), var(--cyan));
  filter: blur(26px);
  opacity: 0.55;
  animation: spin 9s linear infinite;
}
.avatar {
  position: relative;
  width: 76%;
  height: 76%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 0 8px rgba(7, 7, 15, 0.8);
}
.orbit {
  position: absolute;
  inset: -6%;
  border-radius: 50%;
  border: 1px dashed rgba(167, 139, 250, 0.25);
  animation: spin 14s linear infinite;
}
.orbit.o2 {
  inset: 6%;
  border-color: rgba(34, 211, 238, 0.2);
  animation-duration: 9s;
  animation-direction: reverse;
}
.orbit span {
  position: absolute;
  top: -5px;
  left: 50%;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 16px var(--cyan);
}
.o2 span {
  background: var(--pink);
  box-shadow: 0 0 16px var(--pink);
}
.badge {
  position: absolute;
  bottom: 2%;
  right: -4%;
  padding: 12px 16px;
  font-size: 0.9rem;
  line-height: 1.4;
  animation: float 5s ease-in-out infinite;
}
.badge strong {
  font-size: 1.4rem;
}
.badge small {
  color: var(--muted);
}

.scroll-hint {
  position: absolute;
  bottom: 28px;
  left: 50%;
  translate: -50% 0;
  width: 26px;
  height: 42px;
  border: 2px solid var(--border-strong);
  border-radius: 14px;
}
.scroll-hint span {
  position: absolute;
  top: 8px;
  left: 50%;
  width: 4px;
  height: 8px;
  margin-left: -2px;
  border-radius: 2px;
  background: var(--cyan);
  animation: scroll 1.8s infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
@keyframes blink { 50% { opacity: 0; } }
@keyframes pulse { 50% { opacity: 0.4; } }
@keyframes float { 50% { transform: translateY(-10px); } }
@keyframes scroll {
  0% { opacity: 0; transform: translateY(0); }
  40% { opacity: 1; }
  100% { opacity: 0; transform: translateY(14px); }
}

@media (max-width: 860px) {
  .hero-grid {
    grid-template-columns: 1fr;
    text-align: left;
  }
  .avatar-wrap {
    order: -1;
    width: min(240px, 70vw);
  }
  .badge {
    right: -12%;
  }
  .scroll-hint {
    display: none;
  }
}
</style>
