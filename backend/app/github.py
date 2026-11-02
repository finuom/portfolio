"""Coleta dados do GitHub e monta o payload do portfólio."""
import asyncio
import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import httpx

API = "https://api.github.com"
CONFIG_PATH = Path(__file__).resolve().parent.parent / "portfolio.config.json"

LANG_COLORS = {
    "Python": "#3572A5", "Vue": "#41b883", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Java": "#b07219", "C": "#8b8b9e", "C++": "#f34b7d", "HTML": "#e34c26", "CSS": "#663399",
    "SCSS": "#c6538c", "Jupyter Notebook": "#DA5B0B", "Shell": "#89e051", "TeX": "#3D6117",
    "PLpgSQL": "#336790", "Go": "#00ADD8", "Rust": "#dea584",
}


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


async def _list_repos(client: httpx.AsyncClient, username: str) -> list[dict]:
    # Com token, /user/repos inclui os privados; sem token, só os públicos.
    authed = "Authorization" in client.headers
    url = f"{API}/user/repos" if authed else f"{API}/users/{username}/repos"
    params = {"per_page": 100, "sort": "pushed"}
    if authed:
        params.update(affiliation="owner", visibility="all")
    else:
        params["type"] = "owner"

    repos, page = [], 1
    while True:
        r = await client.get(url, params={**params, "page": page})
        r.raise_for_status()
        batch = r.json()
        repos.extend(batch)
        if len(batch) < 100:
            return repos
        page += 1


async def _languages(client: httpx.AsyncClient, repo: dict) -> dict[str, int]:
    r = await client.get(repo["languages_url"])
    return r.json() if r.status_code == 200 else {}


async def build_portfolio() -> dict:
    cfg = load_config()
    username = os.getenv("GITHUB_USERNAME", "finuom")
    private_mode = os.getenv("PRIVATE_REPOS", "stats")
    ignored = set(cfg.get("ignored_languages", []))
    include_forks = set(cfg.get("include_forks", []))
    hidden = set(cfg.get("hidden", []))
    overrides = cfg.get("projects", {})

    async with httpx.AsyncClient(headers=_headers(), timeout=20) as client:
        user_r = await client.get(f"{API}/users/{username}")
        user_r.raise_for_status()
        user = user_r.json()
        all_repos = await _list_repos(client, username)
        repos = [
            r for r in all_repos
            if r["owner"]["login"].lower() == username.lower()
            and r["name"] not in hidden
            and (not r["fork"] or r["name"] in include_forks)
        ]
        langs_per_repo = await asyncio.gather(*(_languages(client, r) for r in repos))

    # Linguagens: cada repo contribui com a sua proporção (soma 1), para que um
    # notebook gigante não engula todo o resto.
    share = defaultdict(float)
    used_in = defaultdict(int)
    projects = []
    for repo, langs in zip(repos, langs_per_repo):
        langs = {k: v for k, v in langs.items() if k not in ignored}
        total = sum(langs.values()) or 1
        for name, size in langs.items():
            share[name] += size / total
            used_in[name] += 1

        is_private = repo["private"]
        if is_private and private_mode == "stats":
            continue
        ov = overrides.get(repo["name"], {})
        lang_list = sorted(langs, key=langs.get, reverse=True)
        card = {
            "name": repo["name"],
            "title": ov.get("title", repo["name"].replace("_", " ").replace("-", " ").title()),
            "description": ov.get("description") or repo["description"] or "",
            "category": ov.get("category", "Projetos"),
            "tags": ov.get("tags", repo.get("topics", [])),
            "languages": [
                {"name": n, "percent": round(langs[n] / total * 100, 1), "color": LANG_COLORS.get(n, "#7c7c9c")}
                for n in lang_list[:4]
            ],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "url": None if is_private else repo["html_url"],
            "homepage": repo.get("homepage") or None,
            "created_at": repo["created_at"],
            "pushed_at": repo["pushed_at"],
            "private": is_private,
        }
        if is_private and private_mode == "anonymous":
            card.update(name=f"private-{len(projects)}", title="Projeto privado", description="", homepage=None)
        projects.append(card)

    total_share = sum(share.values()) or 1
    languages = sorted(
        (
            {"name": n, "percent": round(v / total_share * 100, 1), "repos": used_in[n],
             "color": LANG_COLORS.get(n, "#7c7c9c")}
            for n, v in share.items()
        ),
        key=lambda x: x["percent"], reverse=True,
    )

    featured = cfg.get("featured", [])
    rank = {name: i for i, name in enumerate(featured)}
    projects.sort(key=lambda p: (rank.get(p["name"], len(rank)), p["pushed_at"] or ""), reverse=False)
    # Não destacados: mais recentes primeiro
    head = [p for p in projects if p["name"] in rank]
    tail = sorted((p for p in projects if p["name"] not in rank), key=lambda p: p["pushed_at"] or "", reverse=True)
    for p in head:
        p["featured"] = True
    for p in tail:
        p["featured"] = False

    timeline = defaultdict(int)
    for r in repos:
        timeline[int(r["created_at"][:4])] += 1

    created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    last_push = max((r["pushed_at"] for r in repos if r["pushed_at"]), default=None)

    return {
        "profile": {
            "login": user["login"],
            "name": cfg.get("display_name") or user.get("name") or user["login"],
            "headline": cfg.get("headline") or user.get("bio") or "",
            "bio": user.get("bio") or "",
            "about": cfg.get("about", ""),
            "roles": cfg.get("roles", []),
            "avatar_url": user["avatar_url"],
            "html_url": user["html_url"],
            "location": user.get("location"),
            "contacts": cfg.get("contacts", {}),
        },
        "stats": {
            "repos": len(repos),
            "public": sum(not r["private"] for r in repos),
            "private": sum(r["private"] for r in repos),
            "languages": len(languages),
            "stars": sum(r["stargazers_count"] for r in repos),
            "years": datetime.now(timezone.utc).year - created.year,
            "last_push": last_push,
        },
        "languages": languages,
        "projects": head + tail,
        "timeline": [{"year": y, "repos": timeline[y]} for y in sorted(timeline)],
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
