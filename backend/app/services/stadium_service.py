from sqlalchemy.orm import Session

from app import crud


def map_stadium_api_data_to_payload(stadium_raw: dict) -> dict:
    return {
        "id": stadium_raw.get("id"),
        "name": stadium_raw.get("name", "Unknown"),
        "city": stadium_raw.get("city") or "Unknown",
        "address": stadium_raw.get("address") or "Unknown",
        "capacity": stadium_raw.get("capacity") or 0,
        "image": stadium_raw.get("image", "Unknown"),
    }


def ensure_stadium_exists(db: Session, stadium_id: int, stadium_data: dict):
    stadium = crud.stadium_crud.get_stadium(db, stadium_id)

    if not stadium:
        return crud.stadium_crud.create_stadium(db, stadium_data)

    if (stadium.name != stadium_data["name"] or 
        stadium.city != stadium_data["city"] or
        stadium.address != stadium_data["address"] or
        stadium.capacity != stadium_data["capacity"] or
        stadium.image != stadium_data["image"]):
        
        try:
            stadium.name = stadium_data["name"]
            stadium.city = stadium_data["city"]
            stadium.address = stadium_data["address"]
            stadium.capacity = stadium_data["capacity"]
            stadium.image = stadium_data["image"]
            db.commit()
            db.refresh(stadium)
        except Exception as e:
            db.rollback()
            db.refresh(stadium)

    return stadium
