from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mot de passe
PASSWORD = os.getenv("APP_PASSWORD", "jejna3-jibjeZ-pikbun")

# Modèles
class AuthRequest(BaseModel):
    password: str

class DCFRequest(BaseModel):
    ticker: str
    mode: str = "auto"

class EQSRequest(BaseModel):
    universe: str
    sector_index: int

# Routes
@app.get("/")
def root():
    return {
        "message": "Terminal Financier API",
        "status": "En ligne",
        "endpoints": ["/api/auth", "/api/dcf", "/api/eqs"]
    }

@app.post("/api/auth")
async def authenticate(request: AuthRequest):
    if request.password == PASSWORD:
        return {"status": "success", "authenticated": True}
    raise HTTPException(status_code=401, detail="Mot de passe incorrect")

@app.post("/api/dcf")
async def run_dcf(request: DCFRequest):
    try:
        return {
            "status": "success",
            "ticker": request.ticker,
            "data": {
                "intrinsic_value": 364.97,
                "current_price": 230.82,
                "upside": 58.1
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/eqs")
async def run_eqs(request: EQSRequest):
    try:
        return {
            "status": "success",
            "data": [
                {
                    "symbol": "WMT",
                    "name": "Walmart Inc.",
                    "mkt_cap": 888.26
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
