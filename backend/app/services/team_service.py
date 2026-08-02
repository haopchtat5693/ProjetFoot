from sqlalchemy.orm import Session
from typing import Optional

from app import crud, schemas
from app.services.football_api_client import fetch_from_api
from app.services.stadium_service import (
    ensure_stadium_exists,
    map_stadium_api_data_to_payload,
)


def map_team_api_data_to_payload(
    team_raw: dict,
    venue_raw: Optional[dict] = None,
    team_id: int | None = None,
    coach_id: Optional[int] = None,
):
    stadium_id = venue_raw.get("id") if venue_raw else None
    city = (venue_raw.get("city") if venue_raw else None) or "Unknown"
    country = (team_raw.get("country") if team_raw else None) 
    name = team_raw.get("name") or f"Team {team_id}"

    return {
        "id": team_id if team_id is not None else team_raw.get("id"),
        "name": name,
        "country": country,
        "city": city,
        "logo": team_raw.get("logo", None),
        "coach_id": coach_id,
        "stadium_id": stadium_id,
    }


def ensure_team_exists(db: Session, team_data: schemas.TeamCreate):
    team = crud.team_crud.get_team(db, team_data.id)

    if not team:
        return crud.team_crud.create_team(
            db,
            {
                "id": team_data.id,
                "name": team_data.name,
                "country": team_data.country,
                "city": team_data.city,
                "logo": team_data.logo,
                "coach_id": team_data.coach_id,
                "stadium_id": team_data.stadium_id,
            },
        )

    team.name = team_data.name
    team.country = team_data.country
    team.logo = team_data.logo

    if team_data.city and team_data.city != "Unknown":
        team.city = team_data.city
    if team_data.coach_id:
        team.coach_id = team_data.coach_id
    if team_data.stadium_id:
        team.stadium_id = team_data.stadium_id

    db.commit()
    db.refresh(team)
    return team


async def search_teams_by_name(db: Session, name: str, limit: int = 20):
    search_term = name.strip()
    if not search_term:
        return []

    print(f"Recherche equipe par nom: '{search_term}'")

    teams = crud.team_crud.get_teams_by_name(db, search_term, limit=limit)
    if teams:
        print(f"Résultats trouvés en base: {len(teams)}")
        return teams

    print("Aucun résultat en base, appel de l'API externe")
    data = await fetch_from_api("/teams", {"name": search_term})
    response = data.get("response") if data else []
    if not response:
        print("Aucun résultat côté API externe")
        return []

    matched_teams = []
    for item in response[:limit]:
        team_raw = item.get("team", {})
        venue_raw = item.get("venue") or {}
        team_id = team_raw.get("id")
        if not team_id:
            continue

        team_payload = map_team_api_data_to_payload(team_raw, venue_raw, team_id)

        stadium_id = team_payload.get("stadium_id")
        if stadium_id and venue_raw:
            stadium_payload = map_stadium_api_data_to_payload(venue_raw)
            ensure_stadium_exists(db, stadium_id, stadium_payload)

        team = ensure_team_exists(db, schemas.TeamCreate(**team_payload))
        if team:
            print(f"Équipe trouvée et sauvegardée: {team.name} (ID: {team.id})")
            matched_teams.append(team)

    return matched_teams
