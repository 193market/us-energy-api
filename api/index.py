from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import os
from datetime import datetime

app = FastAPI(
    title="US Energy Prices API",
    description="Real-time US energy prices including crude oil, natural gas, gasoline, and electricity. Powered by FRED (Federal Reserve Economic Data).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
API_KEY = os.environ.get("FRED_API_KEY", "")


async def fetch_fred(series_id: str, limit: int = 12):
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.get(BASE_URL, params={
            "series_id": series_id,
            "api_key": API_KEY,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        })
        data = res.json()
        return data.get("observations", [])


@app.get("/")
def root():
    return {
        "api": "US Energy Prices API",
        "version": "1.0.0",
        "provider": "GlobalData Store",
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "endpoints": ["/summary", "/crude-oil", "/natural-gas", "/gasoline", "/electricity", "/heating-oil"],
        "updated_at": datetime.utcnow().isoformat(),
    }


@app.get("/summary")
async def summary(limit: int = Query(default=10, ge=1, le=60)):
    """All energy price indicators snapshot"""
    crude_oil, natural_gas, gasoline, electricity = await asyncio.gather(
        fetch_fred("DCOILWTICO", limit),
        fetch_fred("MHHNGSP", limit),
        fetch_fred("GASREGCOVW", limit),
        fetch_fred("APU000072610", limit),
    )
    return {
        "source": "FRED - Federal Reserve Bank of St. Louis",
        "updated_at": datetime.utcnow().isoformat(),
        "data": {
            "crude_oil": crude_oil,
            "natural_gas": natural_gas,
            "gasoline": gasoline,
            "electricity": electricity,
        }
    }


@app.get("/crude-oil")
async def crude_oil(limit: int = Query(default=12, ge=1, le=60)):
    """WTI crude oil price"""
    data = await fetch_fred("DCOILWTICO", limit)
    return {
        "indicator": "Crude Oil Prices: West Texas Intermediate (WTI)",
        "series_id": "DCOILWTICO",
        "unit": "Dollars per Barrel",
        "frequency": "Daily",
        "source": "FRED - U.S. Energy Information Administration",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/natural-gas")
async def natural_gas(limit: int = Query(default=12, ge=1, le=60)):
    """Henry Hub natural gas spot price"""
    data = await fetch_fred("MHHNGSP", limit)
    return {
        "indicator": "Henry Hub Natural Gas Spot Price",
        "series_id": "MHHNGSP",
        "unit": "Dollars per Million BTU",
        "frequency": "Monthly",
        "source": "FRED - U.S. Energy Information Administration",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/gasoline")
async def gasoline(limit: int = Query(default=12, ge=1, le=60)):
    """US regular conventional gasoline price"""
    data = await fetch_fred("GASREGCOVW", limit)
    return {
        "indicator": "US Regular Conventional Gas Price",
        "series_id": "GASREGCOVW",
        "unit": "Dollars per Gallon",
        "frequency": "Weekly",
        "source": "FRED - U.S. Energy Information Administration",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/electricity")
async def electricity(limit: int = Query(default=12, ge=1, le=60)):
    """US average electricity price (residential)"""
    data = await fetch_fred("APU000072610", limit)
    return {
        "indicator": "Average Retail Price of Electricity: Residential",
        "series_id": "APU000072610",
        "unit": "Cents per Kilowatt-Hour",
        "frequency": "Monthly",
        "source": "FRED - U.S. Bureau of Labor Statistics",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }


@app.get("/heating-oil")
async def heating_oil(limit: int = Query(default=12, ge=1, le=60)):
    """US heating oil price"""
    data = await fetch_fred("DHOILNYH", limit)
    return {
        "indicator": "Heating Oil Prices: New York Harbor",
        "series_id": "DHOILNYH",
        "unit": "Dollars per Gallon",
        "frequency": "Daily",
        "source": "FRED - U.S. Energy Information Administration",
        "updated_at": datetime.utcnow().isoformat(),
        "data": data,
    }

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if request.url.path == "/":
        return await call_next(request)
    key = request.headers.get("X-RapidAPI-Key", "")
    if not key:
        return JSONResponse(status_code=401, content={"detail": "Missing X-RapidAPI-Key header"})
    return await call_next(request)
