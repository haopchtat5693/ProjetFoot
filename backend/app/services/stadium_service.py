from sqlalchemy.orm import Session

from app import crud


def ensure_stadium_exists(db: Session, stadium_id: int, stadium_data: dict):
    stadium = crud.stadium_crud.get_stadium(db, stadium_id)

    city = stadium_data.get("city") or "Unknown"
    address = stadium_data.get("address") or "Unknown"
    name = stadium_data.get("name", f"Stadium {stadium_id}")
    capacity = stadium_data.get("capacity") or 0

    if not stadium:
        return crud.stadium_crud.create_stadium(
            db,
            {
                "id": stadium_id,
                "name": name,
                "city": city,
                "address": address,
                "capacity": capacity,
            },
        )

    stadium.name = name
    stadium.city = city
    stadium.address = address
    stadium.capacity = capacity
    db.commit()
    db.refresh(stadium)

    return stadium
