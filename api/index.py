"""Ponto de entrada da função serverless da Vercel: expõe o app FastAPI."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app  # noqa: E402,F401
