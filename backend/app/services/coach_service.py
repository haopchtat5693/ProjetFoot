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
	print(f"\n[DEBUG] _sync_coach_career for coach_id={coach_id}")
	print(f"[DEBUG] Incoming career entries: {len(career_raw)}")
	for i, entry in enumerate(career_raw):
		team = entry.get("team") or {}
		print(f"  [{i}] Team: {team.get('name')}, Start: {entry.get('start')}, End: {entry.get('end')}")
	
	existing = (
		db.query(models.CoachCareer).filter(models.CoachCareer.coach_id == coach_id).all()
	)
	print(f"[DEBUG] Existing career entries in DB: {len(existing)}")
	for item in existing:
		print(f"  - {item.team.name}, Start: {item.start}, End: {item.end}")

	existing_by_team_start = {
		(item.team_id, item.start): item
		for item in existing
	}

	added_count = 0
	updated_count = 0
	
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

		key = (team_id, start)
		
		if key in existing_by_team_start:
			# Update existing entry if end date changed
			career_entry = existing_by_team_start[key]
			if career_entry.end != end:
				print(f"[DEBUG] Updating career entry: team_id={team_id}, start={start}, end {career_entry.end} -> {end}")
				career_entry.end = end
				updated_count += 1
		else:
			print(f"[DEBUG] Adding new career entry: team_id={team_id}, start={start}, end={end}")
			db.add(
				models.CoachCareer(
					coach_id=coach_id,
					team_id=team_id,
					start=start,
					end=end,
				)
			)
			added_count += 1

	print(f"[DEBUG] Sync summary: added {added_count}, updated {updated_count}, kept {len(existing)}")
	db.commit()


def _save_coach_from_response_item(db: Session, item: dict):
	coach_id = item.get("id")
	if not coach_id:
		return None

	print(f"\n[DEBUG] _save_coach_from_response_item: coach_id={coach_id}, name={item.get('name')}")
	
	coach_schema = map_coach_api_data_to_schema(item)
	coach = ensure_coach_exists(db, coach_id, coach_schema)

	career_raw = item.get("career") or []
	print(f"[DEBUG] Career data in API response: {len(career_raw)} entries")
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

	print(f"\n[DEBUG] search_coaches_by_name: '{search_term}'")
	
	local_coaches = crud.coach_crud.get_coaches_by_name(db, search_term, limit=limit)
	print(f"[DEBUG] Found {len(local_coaches)} coaches in local DB")
	
	data = await fetch_from_api("/coachs", {"search": search_term})
	response = data.get("response") if data else []
	print(f"[DEBUG] API returned {len(response)} coaches")
	for coach in response:
		career = coach.get("career") or []
		print(f"  - {coach.get('name')}: {len(career)} career entries")
	
	saved_ids = {c.id for c in local_coaches}
	matched = list(local_coaches)

	for item in response[:limit]:
		coach = _save_coach_from_response_item(db, item)
		if coach and coach.id not in saved_ids:
			matched.append(coach)
			saved_ids.add(coach.id)

	return matched
