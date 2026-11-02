import os
import time

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, Response  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from .github import build_portfolio  # noqa: E402

CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
# Na Vercel cada chamada pode cair numa instância nova, então quem segura o
# cache de verdade é a CDN (s-maxage). O cache em memória ajuda localmente.
CDN_CACHE = f"public, s-maxage={CACHE_TTL}, stale-while-revalidate=86400"
_cache: dict = {"data": None, "at": 0.0}

app = FastAPI(title="Portfolio API", docs_url="/api/docs", openapi_url="/api/openapi.json")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"ok": True}


@app.get("/api/portfolio")
async def portfolio(response: Response):
    response.headers["Cache-Control"] = CDN_CACHE
    if _cache["data"] is not None and time.time() - _cache["at"] < CACHE_TTL:
        return _cache["data"]
    try:
        data = await build_portfolio()
    except Exception as exc:
        # GitHub fora do ar ou limite de requisições: serve o último resultado.
        if _cache["data"] is not None:
            return _cache["data"]
        response.headers["Cache-Control"] = "no-store"
        raise HTTPException(status_code=502, detail=f"Falha ao consultar o GitHub: {exc}") from exc
    _cache.update(data=data, at=time.time())
    return data
