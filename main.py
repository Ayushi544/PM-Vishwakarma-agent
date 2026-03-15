import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai

# ── APP ───────────────────────────────────────────────────────
app = FastAPI(
    title="PM Vishwakarma AI Agent",
    description="Multilingual AI agent for PM Vishwakarma Yojana artisans — Ministry of MSME · ACU · IndiaAI Mission",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── DATA ──────────────────────────────────────────────────────
TRADES = [
    {"id": 1,  "name": "Carpenter (Suthar/Badhai)",          "hindi": "बढ़ई",               "category": "Wood Based"},
    {"id": 2,  "name": "Boat Maker",                          "hindi": "नाव बनाने वाला",     "category": "Wood Based"},
    {"id": 3,  "name": "Armourer",                            "hindi": "शस्त्रकार",          "category": "Iron/Metal"},
    {"id": 4,  "name": "Blacksmith (Lohar)",                  "hindi": "लोहार",              "category": "Iron/Metal"},
    {"id": 5,  "name": "Hammer and Tool Kit Maker",           "hindi": "हथौड़ा बनाने वाला",  "category": "Iron/Metal"},
    {"id": 6,  "name": "Locksmith",                           "hindi": "ताला बनाने वाला",    "category": "Iron/Metal"},
    {"id": 7,  "name": "Goldsmith (Sunar)",                   "hindi": "सुनार",              "category": "Gold/Silver"},
    {"id": 8,  "name": "Potter (Kumhaar)",                    "hindi": "कुम्हार",            "category": "Clay Based"},
    {"id": 9,  "name": "Sculptor / Stone Carver",             "hindi": "मूर्तिकार",          "category": "Stone Based"},
    {"id": 10, "name": "Cobbler / Footwear Artisan",          "hindi": "मोची",               "category": "Leather"},
    {"id": 11, "name": "Mason (Raajmistri)",                  "hindi": "राजमिस्त्री",        "category": "Construction"},
    {"id": 12, "name": "Basket / Mat / Broom Maker",          "hindi": "टोकरी बनाने वाला",  "category": "Others"},
    {"id": 13, "name": "Doll & Toy Maker (Traditional)",      "hindi": "खिलौना बनाने वाला", "category": "Others"},
    {"id": 14, "name": "Barber (Naai)",                       "hindi": "नाई",                "category": "Others"},
    {"id": 15, "name": "Garland Maker (Malakaar)",            "hindi": "मालाकार",            "category": "Others"},
    {"id": 16, "name": "Washerman (Dhobi)",                   "hindi": "धोबी",               "category": "Others"},
    {"id": 17, "name": "Tailor (Darzi)",                      "hindi": "दर्जी",              "category": "Others"},
    {"id": 18, "name": "Fishing Net Maker",                   "hindi": "मछली जाल बनाने वाला","category": "Others"},
]

SYSTEM_PROMPT = """You are Vishwakarma Mitra, a friendly AI assistant for traditional Indian artisans under PM Vishwakarma Yojana, Government of India.

LANGUAGE RULE: Always reply in the SAME language the user writes in. Hindi to Hindi. English to English. Hinglish to Hinglish.

SCHEME FACTS:
- 18 eligible trades (carpenter, potter, tailor, blacksmith, goldsmith etc.)
- Benefits: PM Vishwakarma Certificate + ID card, Rs 500/day training stipend, Rs 15000 toolkit grant, Rs 1 lakh first loan + Rs 2 lakh second loan at 5% interest, Rs 1 per digital transaction
- Eligibility: 18+ years, unorganized sector, one family member only, no PMEGP/Mudra/SVANidhi loan in last 5 years
- Portal: pmvishwakarma.gov.in

Keep replies SHORT under 150 words. Use simple language for non-tech users aged 35-60. Be warm and encouraging."""

# ── MODELS ────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "auto"
    trade: Optional[str] = None

# ── ENDPOINTS ─────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "rb") as f:
            return HTMLResponse(content=f.read().decode("utf-8"))
    return HTMLResponse(content="<h1>Place index.html next to main.py</h1>")

@app.get("/health")
def health():
    return {"status": "ok"}

from groq_generation import generate_groq

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        context = f"[User trade: {req.trade}]\n" if req.trade else ""
        prompt = SYSTEM_PROMPT + "\n\n" + context + "User: " + req.message
        response = generate_groq(prompt)
        print(response)
        return {
            "reply": response,
            "timestamp": datetime.now().isoformat(),
            "source": "PM Vishwakarma AI Agent · MoMSME"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trades")
def get_trades():
    return {"total": 18, "trades": TRADES}

@app.get("/scheme")
def get_scheme():
    return {
        "name": "PM Vishwakarma Yojana",
        "portal": "https://pmvishwakarma.gov.in",
        "benefits": {
            "recognition": "PM Vishwakarma Certificate + ID Card",
            "training_stipend": "Rs 500 per day",
            "toolkit_grant": "Rs 15000",
            "loan_first": "Rs 1 lakh at 5% interest",
            "loan_second": "Rs 2 lakh at 5% interest",
            "digital_incentive": "Rs 1 per transaction max 100 per month"
        }
    }

@app.get("/course")
def get_course():
    return {
        "title": "AI Aapke Haath Mein",
        "duration": "2.5 hours",
        "target": "PM Vishwakarma artisans aged 35-60",
        "tools": ["ChatGPT", "Gemini", "Sarvam AI"],
        "modules": [
            {"no": 1, "title": "AI Kya Hai?", "duration": "25 min"},
            {"no": 2, "title": "AI Se Vishwakarma Ko Kya Faayda?", "duration": "25 min"},
            {"no": 3, "title": "ChatGPT Demo", "duration": "35 min"},
            {"no": 4, "title": "Gemini Demo", "duration": "30 min"},
            {"no": 5, "title": "Sarvam AI - India Ka Apna AI", "duration": "20 min"},
            {"no": 6, "title": "Hands-On Practice", "duration": "25 min"}
        ]
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)