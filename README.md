# US Energy Prices API

Real-time US energy prices including crude oil, natural gas, gasoline, and electricity. Powered by FRED (Federal Reserve Economic Data).

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API info and available endpoints |
| `GET /summary` | All energy price indicators snapshot |
| `GET /crude-oil` | WTI crude oil price (DCOILWTICO) |
| `GET /natural-gas` | Henry Hub natural gas spot price (MHHNGSP) |
| `GET /gasoline` | US regular conventional gasoline price (GASREGCOVW) |
| `GET /electricity` | Average retail electricity price: residential (APU000072610) |
| `GET /heating-oil` | Heating oil price: New York Harbor (DHOILNYH) |

## Data Source

FRED - Federal Reserve Bank of St. Louis
https://fred.stlouisfed.org/

## Authentication

Requires `X-RapidAPI-Key` header via RapidAPI.
