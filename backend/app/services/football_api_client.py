import httpx
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_DATA_KEY")
BASE_URL = "https://v3.football.api-sports.io"
DEFAULT_TIMEOUT_SECONDS = 10.0


async def fetch_from_api(endpoint: str, params: dict = None):
    headers = {"x-apisports-key": API_KEY}
    timeout = httpx.Timeout(DEFAULT_TIMEOUT_SECONDS)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                f"{BASE_URL}{endpoint}", headers=headers, params=params
            )
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Le service externe met trop de temps à répondre.",
        )
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Erreur du service externe "
                f"(status {exc.response.status_code})."
            ),
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service externe indisponible pour le moment.",
        )
