# Portfólio — Mounif Tormos

Portfólio gerado a partir dos repositórios do GitHub (públicos **e** privados).

- **frontend/**: Vue 3 + Vite, com fundo de partículas conectadas, constelação de linguagens e cards com efeito 3D
- **backend/**: FastAPI, que consulta a API do GitHub com token e calcula linguagens, destaques e linha do tempo. O resultado fica em cache por 1h
- **api/index.py**: entrada que roda o FastAPI como função serverless na Vercel. Frontend e backend ficam no mesmo projeto e no mesmo domínio

## Rodar localmente

```bash
# backend
cd backend
cp .env.example .env   # preencha GITHUB_TOKEN
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload --port 8000

# frontend (outro terminal)
cd frontend
npm install
npm run dev            # http://localhost:5173 (o /api é encaminhado para :8000)
```

## Personalizar

Edite `backend/portfolio.config.json`: nome, frase de apresentação, papéis do efeito de digitação, texto "sobre", contatos,
projetos em destaque (`featured`), repositórios ocultos (`hidden`) e títulos, descrições e tags de cada projeto.

### Repositórios privados

A variável `PRIVATE_REPOS` controla como os privados aparecem:

| valor       | efeito                                                    |
|-------------|-----------------------------------------------------------|
| `stats`     | entram só nas estatísticas e linguagens (padrão)          |
| `anonymous` | aparecem como cards "Projeto privado", sem nome nem link  |
| `full`      | aparecem com nome e descrição, sem link para o código     |

## Snapshot (carregamento instantâneo)

O frontend mostra primeiro `frontend/public/snapshot.json`, que é estático e instantâneo, e depois troca pelos dados ao vivo
da API. Assim a página nunca abre vazia, nem quando a função serverless está "fria". Para atualizar o snapshot:

```bash
cd backend && .venv/bin/python -m app.snapshot
```

## Deploy gratuito na Vercel

Frontend (Vue) e backend (FastAPI) sobem juntos num único projeto. As configurações estão no `vercel.json`.

### 1. Subir para o GitHub
Crie um repositório vazio chamado `portfolio` e envie esta pasta. O `.env` (com o token) está no `.gitignore` e **não** vai junto.

```bash
git init && git add . && git commit -m "Portfólio"
git branch -M main
git remote add origin https://github.com/finuom/portfolio.git
git push -u origin main
```

### 2. Importar na Vercel
1. Em [vercel.com](https://vercel.com), entre com o GitHub → **Add New… → Project** → escolha o repositório `portfolio`.
2. **Root Directory**: deixe a raiz (`./`). **Framework Preset**: *Other*. Build e saída já vêm do `vercel.json`.
3. Em **Environment Variables**, adicione:
   - `GITHUB_USERNAME` = `finuom`
   - `GITHUB_TOKEN` = o token do seu `.env`
   - `PRIVATE_REPOS` = `stats` (opcional; é o padrão)
4. Clique em **Deploy**. Pronto: o site fica em `https://portfolio-xxx.vercel.app` e a API em `/api/portfolio`.

Para ter um endereço melhor, como `mounif.vercel.app`, vá em *Settings → Domains*.

> Se você mudar uma variável de ambiente depois do deploy, faça *Deployments → ⋯ → Redeploy* para ela valer.

Cada `git push` na `main` refaz o deploy automaticamente. A resposta da API fica 1h no cache da CDN da Vercel, então o
GitHub é consultado no máximo uma vez por hora.
