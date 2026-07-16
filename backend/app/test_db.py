from app.database import engine, Base
from app.models import Team

print("Trying to connect to the database...")

try:
    Base.metadata.create_all(bind=engine)
    print("Success!")
except Exception as e:
    print(f"Error : {e}")
    