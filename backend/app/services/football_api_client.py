import httpx
import os
from dotenv import load_dotenv

load_dotenv()  
API_KEY = os.getenv("API_FOOTBALL_DATA_KEY")
BASE_URL = "https://v3.football.api-sports.io"

async def fetch_from_api(endpoint: str, params: dict = None):
    headers = {
        "x-apisports-key": API_KEY
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status() 
        return response.json()