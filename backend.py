from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# CORS pour autoriser les appels depuis votre frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mot de passe sécurisé via variable d'environnement
PASSWORD = os.getenv("APP_PASSWORD", "bloomberg2026")

# ===== AUTHENTIFICATION =====
class AuthRequest(BaseModel):
    password: str

@app.post("/api/auth")
async def authenticate(request: AuthRequest):
    if request.password == PASSWORD:
        return {"status": "success", "authenticated": True}
    raise HTTPException(status_code=401, detail="Mot de passe incorrect")

# ===== DCF ANALYSIS =====
class DCFRequest(BaseModel):
    ticker: str
    mode: str = "auto"
    revenue_growth: float = None
    ebit_margin: float = None
    fcf_conversion: float = None

@app.post("/api/dcf")
async def run_dcf(request: DCFRequest):
    try:
        # TODO : Intégrer vos fonctions DCF.ipynb ici
        # Pour l'instant, données de test
        return {
            "status": "success",
            "ticker": request.ticker,
            "data": {
                "intrinsic_value": 364.97,
                "current_price": 230.82,
                "upside": 58.1,
                "wacc": 11.71,
                "enterprise_value": 3875.44,
                "equity_value": 3901.59
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== EQUITY SCREENER =====
class EQSRequest(BaseModel):
    universe: str  # "1", "2", ou "3"
    sector_index: int

@app.post("/api/eqs")
async def run_eqs(request: EQSRequest):
    try:
        # TODO : Intégrer vos fonctions EQS.ipynb ici
        # Données de test
        return {
            "status": "success",
            "universe": request.universe,
            "sector_index": request.sector_index,
            "data": [
                {
                    "symbol": "WMT",
                    "name": "Walmart Inc.",
                    "mkt_cap": 888.26,
                    "pe_ratio": 38.95,
                    "fcf_yield": 1.17,
                    "div_yield": 84.0,
                    "roe": 23.66
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== PAGE D'ACCUEIL =====
@app.get("/")
def root():
    return {
        "message": "Terminal Financier API",
        "status": "En ligne ✅",
        "endpoints": ["/api/auth", "/api/dcf", "/api/eqs"]
    }
