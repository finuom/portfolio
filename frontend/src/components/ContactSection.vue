<script setup>
defineProps({ profile: Object, generatedAt: String, live: Boolean })
</script>

<template>
  <section id="contato">
    <div class="container">
      <div class="contact glass" v-reveal>
        <p class="section-label">// contato</p>
        <h2 class="section-title">Vamos <span class="grad-text">construir algo</span> juntos?</h2>
        <p class="sub">Estou aberto a oportunidades, projetos e boas conversas sobre software e IA.</p>
        <div class="links">
          <a v-if="profile.contacts.email" :href="`mailto:${profile.contacts.email}`" class="btn btn-primary">✉ {{ profile.contacts.email }}</a>
          <a v-if="profile.contacts.github" :href="profile.contacts.github" target="_blank" rel="noopener" class="btn btn-ghost">GitHub</a>
          <a v-if="profile.contacts.linkedin" :href="profile.contacts.linkedin" target="_blank" rel="noopener" class="btn btn-ghost">LinkedIn</a>
        </div>
      </div>
      <footer>
        <span>© {{ new Date().getFullYear() }} {{ profile.name }}</span>
        <span class="status" :title="generatedAt">
          <i :class="{ live }"></i>
          {{ live ? 'dados ao vivo do GitHub' : 'dados em cache' }} · Vue + FastAPI
        </span>
      </footer>
    </div>
  </section>
</template>

<style scoped>
#contato {
  padding-bottom: 40px;
}
.contact {
  text-align: center;
  padding: 64px 28px;
  position: relative;
  overflow: hidden;
}
.contact::after {
  content: '';
  position: absolute;
  width: 420px;
  height: 420px;
  left: 50%;
  top: -260px;
  translate: -50% 0;
  background: radial-gradient(circle, rgba(167, 139, 250, 0.35), transparent 65%);
  pointer-events: none;
}
.sub {
  color: var(--muted);
  margin: 0 auto 32px;
  max-width: 480px;
  line-height: 1.6;
}
.links {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 14px;
}
footer {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 48px;
  color: var(--muted);
  font-size: 0.85rem;
  font-family: var(--mono);
}
.status {
  display: flex;
  align-items: center;
  gap: 8px;
}
.status i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #facc15;
}
.status i.live {
  background: #4ade80;
  box-shadow: 0 0 10px #4ade80;
}
</style>
