<script setup>
import { computed } from 'vue'

const props = defineProps({ profile: Object, stats: Object, timeline: Array })

const cards = computed(() => [
  { value: props.stats.repos, label: 'repositórios', hint: `${props.stats.public} públicos · ${props.stats.private} privados` },
  { value: props.stats.languages, label: 'linguagens', hint: 'de C a Vue' },
  { value: props.stats.years, label: 'anos no GitHub', hint: 'desde ' + (new Date().getFullYear() - props.stats.years) },
  { value: lastPush.value, label: 'último push', hint: 'sempre construindo' },
])

const lastPush = computed(() => {
  if (!props.stats.last_push) return '—'
  const days = Math.floor((Date.now() - new Date(props.stats.last_push)) / 864e5)
  if (days <= 0) return 'hoje'
  if (days === 1) return 'ontem'
  if (days < 30) return `${days}d`
  return `${Math.floor(days / 30)}m`
})

const maxYear = computed(() => Math.max(1, ...props.timeline.map((t) => t.repos)))
</script>

<template>
  <section id="sobre">
    <div class="container about-grid">
      <div>
        <p class="section-label" v-reveal>// sobre mim</p>
        <h2 class="section-title" v-reveal="60">
          Do <span class="grad-text">back-end</span> ao <span class="grad-text">modelo</span>.
        </h2>
        <p class="about" v-reveal="120">{{ profile.about }}</p>

        <div class="timeline glass" v-reveal="180">
          <p class="tl-title">Repositórios criados por ano</p>
          <div class="bars">
            <div v-for="t in timeline" :key="t.year" class="bar-col">
              <div class="bar" :style="{ height: (t.repos / maxYear) * 100 + '%' }">
                <span>{{ t.repos }}</span>
              </div>
              <small>{{ t.year }}</small>
            </div>
          </div>
        </div>
      </div>

      <div class="stats">
        <div v-for="(c, i) in cards" :key="c.label" class="stat glass" v-reveal="i * 90">
          <strong class="grad-text">{{ c.value }}</strong>
          <span>{{ c.label }}</span>
          <small>{{ c.hint }}</small>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about-grid {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 56px;
  align-items: start;
}
.about {
  color: var(--muted);
  font-size: 1.12rem;
  line-height: 1.75;
  margin: 0 0 32px;
}
.stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.stat {
  padding: 26px 22px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  transition: border-color 0.3s, transform 0.3s;
}
.stat:hover {
  border-color: var(--border-strong);
  transform: translateY(-4px);
}
.stat strong {
  font-size: 2.6rem;
  font-weight: 700;
  line-height: 1.1;
}
.stat span {
  font-weight: 600;
}
.stat small {
  color: var(--muted);
  font-size: 0.82rem;
}

.timeline {
  padding: 22px 24px 18px;
}
.tl-title {
  margin: 0 0 18px;
  font-family: var(--mono);
  font-size: 0.82rem;
  color: var(--muted);
}
.bars {
  display: flex;
  align-items: flex-end;
  gap: 14px;
  height: 120px;
}
.bar-col {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}
.bar {
  width: 100%;
  max-width: 44px;
  min-height: 6px;
  border-radius: 8px 8px 3px 3px;
  background: linear-gradient(to top, rgba(34, 211, 238, 0.35), var(--violet));
  position: relative;
  transition: filter 0.3s;
}
.bar:hover {
  filter: brightness(1.3);
}
.bar span {
  position: absolute;
  top: -22px;
  left: 50%;
  translate: -50% 0;
  font-size: 0.8rem;
  font-family: var(--mono);
}
.bar-col small {
  font-family: var(--mono);
  color: var(--muted);
  font-size: 0.75rem;
}

@media (max-width: 860px) {
  .about-grid {
    grid-template-columns: 1fr;
  }
}
</style>
