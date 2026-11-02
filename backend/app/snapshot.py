"""Gera um snapshot estático (frontend/public/snapshot.json).

O frontend mostra o snapshot instantaneamente enquanto o backend gratuito
"acorda", e depois troca pelos dados ao vivo.

    python -m app.snapshot
"""
import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from .github import build_portfolio  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "frontend" / "public" / "snapshot.json"

if __name__ == "__main__":
    data = asyncio.run(build_portfolio())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"snapshot salvo em {OUT} ({len(data['projects'])} projetos)")
