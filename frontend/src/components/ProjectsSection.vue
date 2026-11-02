<script setup>
import { computed, ref } from 'vue'
import ProjectCard from './ProjectCard.vue'

const props = defineProps({ projects: Array })
const filter = ref('Destaques')

const categories = computed(() => ['Destaques', 'Todos', ...new Set(props.projects.map((p) => p.category))])
const visible = computed(() => {
  if (filter.value === 'Todos') return props.projects
  if (filter.value === 'Destaques') return props.projects.filter((p) => p.featured)
  return props.projects.filter((p) => p.category === filter.value)
})
</script>

<template>
  <section id="projetos">
    <div class="container">
      <p class="section-label" v-reveal>// projetos</p>
      <h2 class="section-title" v-reveal="60">Coisas que eu <span class="grad-text">construí</span></h2>

      <div class="filters" v-reveal="100" role="tablist">
        <button
          v-for="c in categories"
          :key="c"
          role="tab"
          :aria-selected="filter === c"
          :class="{ on: filter === c }"
          @click="filter = c"
        >
          {{ c }}
        </button>
      </div>

      <TransitionGroup name="grid" tag="div" class="grid">
        <ProjectCard v-for="p in visible" :key="p.name" :project="p" />
      </TransitionGroup>
    </div>
  </section>
</template>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 10px 0 36px;
}
.filters button {
  font: inherit;
  font-size: 0.9rem;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  padding: 8px 18px;
  border-radius: 99px;
  cursor: pointer;
  transition: all 0.25s;
}
.filters button:hover {
  color: var(--text);
  border-color: var(--border-strong);
}
.filters button.on {
  color: #0a0a14;
  background: var(--grad);
  border-color: transparent;
  font-weight: 600;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 320px), 1fr));
  gap: 22px;
}
.grid-enter-active,
.grid-leave-active {
  transition: opacity 0.35s, transform 0.35s;
}
.grid-enter-from,
.grid-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(12px);
}
.grid-leave-active {
  position: absolute;
  visibility: hidden;
}
</style>
