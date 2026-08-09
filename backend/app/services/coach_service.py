from datetime import date

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.services.football_api_client import fetch_from_api
from app.services.team_service import ensure_team_exists, map_team_api_data_to_payload


def map_coach_api_data_to_schema(coach_raw: dict) -> schemas.CoachCreate:
	return schemas.CoachCreate(
		name=coach_raw.get("name") or "Unknown",
		age=coach_raw.get("age") or 0,
		nationality=coach_raw.get("nationality") or "Unknown",
		photo=coach_raw.get("photo"),
	)


def ensure_coach_exists(db: Session, coach_id: int, coach_data: schemas.CoachCreate):
	coach = crud.coach_crud.get_coach(db, coach_id)

	if not coach:
		payload = coach_data.model_dump()
		payload["id"] = coach_id
		return crud.coach_crud.create_coach(db, payload)

	coach.name = coach_data.name
	coach.age = coach_data.age
	coach.nationality = coach_data.nationality
	coach.photo = coach_data.photo
	db.commit()
	db.refresh(coach)
	return coach


def _sync_coach_career(db: Session, coach_id: int, career_raw: list[dict]):
	existing = (
		db.query(models.CoachCareer).filter(models.CoachCareer.coach_id == coach_id).all()
	)
	existing_keys = {
		(
			item.team_id,
			item.start,
			item.end,
		): item
		for item in existing
	}

	incoming_keys = set()
	for entry in career_raw:
		team_raw = entry.get("team") or {}
		team_id = team_raw.get("id")
		start_raw = entry.get("start")
		end_raw = entry.get("end")

		if not team_id or not start_raw:
			continue

		try:
			start = date.fromisoformat(start_raw)
			end = date.fromisoformat(end_raw) if end_raw else None
		except ValueError:
			continue

		team_payload = map_team_api_data_to_payload(team_raw, None, team_id)
		ensure_team_exists(db, schemas.TeamCreate(**team_payload))

		key = (team_id, start, end)
		incoming_keys.add(key)
		if key not in existing_keys:
			db.add(
				models.CoachCareer(
					coach_id=coach_id,
					team_id=team_id,
					start=start,
					end=end,
				)
			)

	for key, item in existing_keys.items():
		if key not in incoming_keys:
			db.delete(item)

	db.commit()


def _save_coach_from_response_item(db: Session, item: dict):
	coach_id = item.get("id")
	if not coach_id:
		return None

	coach_schema = map_coach_api_data_to_schema(item)
	coach = ensure_coach_exists(db, coach_id, coach_schema)

	career_raw = item.get("career") or []
	_sync_coach_career(db, coach_id, career_raw)

	return crud.coach_crud.get_coach(db, coach_id)


async def sync_and_save_coach(db: Session, coach_id: int):
	data = await fetch_from_api("/coachs", {"id": coach_id})
	response = data.get("response") if data else []
	if not response:
		return None

	return _save_coach_from_response_item(db, response[0])


async def sync_and_save_coaches_by_team(db: Session, team_id: int):
	data = await fetch_from_api("/coachs", {"team": team_id})
	response = data.get("response") if data else []
	if not response:
		return []

	coaches = []
	seen_ids = set()
	for item in response:
		coach = _save_coach_from_response_item(db, item)
		if coach and coach.id not in seen_ids:
			seen_ids.add(coach.id)
			coaches.append(coach)

	return coaches


async def search_coaches_by_name(db: Session, name: str, limit: int = 50):
	search_term = name.strip()
	if not search_term:
		return []

	coaches = crud.coach_crud.get_coaches_by_name(db, search_term, limit=limit)
	if coaches:
		return coaches

	data = await fetch_from_api("/coachs", {"search": search_term})
	response = data.get("response") if data else []
	if not response:
		return []

	matched = []
	for item in response[:limit]:
		coach = _save_coach_from_response_item(db, item)
		if coach:
			matched.append(coach)

	return matched
