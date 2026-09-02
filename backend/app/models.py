from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, Date
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from app.core.constants import VIEWER


class Fixture(Base):
    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=True, index=True)
    stadium_id = Column(Integer, ForeignKey("stadiums.id"), nullable=True, index=True)
    
    date = Column(String, index=True)
    location = Column(String)
    result = Column(String, nullable=True)
    status = Column(String, nullable=True, index=True)
    timezone = Column(String, nullable=True)
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)
    
    referee_id = Column(Integer, ForeignKey("referees.id"), nullable=True, index=True)
    
    statistics = Column(JSONB, nullable=True)

    home_team = relationship(
        "Team", foreign_keys=[home_team_id], back_populates="home_fixtures"
    )
    away_team = relationship(
        "Team", foreign_keys=[away_team_id], back_populates="away_fixtures"
    )
    referee = relationship("Referee", back_populates="fixtures")
    league = relationship("League")
    stadium = relationship("Stadium")
    players_stats = relationship("PlayerMatchStats", back_populates="fixture")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String, nullable=True, index=True)
    city = Column(String)
    logo = Column(String, nullable=True)

    stadium_id = Column(Integer, ForeignKey("stadiums.id"), nullable=True, index=True)

    stadium = relationship("Stadium", back_populates="teams")

    home_fixtures = relationship(
        "Fixture", foreign_keys=[Fixture.home_team_id], back_populates="home_team"
    )
    away_fixtures = relationship(
        "Fixture", foreign_keys=[Fixture.away_team_id], back_populates="away_team"
    )
    contracts = relationship("Contract", back_populates="team")
    season_stats = relationship("TeamSeasonStats", back_populates="team")


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    nationality = Column(String, nullable=True, index=True)
    position = Column(String, index=True)
    age = Column(Integer, nullable=True, index=True)
    photo = Column(String, nullable=True, index=True)

    match_stats = relationship("PlayerMatchStats", back_populates="player")
    season_stats = relationship("PlayerSeasonStats", back_populates="player")
    contracts = relationship("Contract", back_populates="player")


class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    nationality = Column(String, nullable=True, index=True)
    photo = Column(String, nullable=True, index=True)

    career = relationship(
        "CoachCareer",
        back_populates="coach",
        cascade="all, delete-orphan",
        order_by="CoachCareer.start.desc()",
    )

    @property
    def current_team(self):
        for entry in self.career:
            if entry.end is None:
                return entry.team
        return None


class CoachCareer(Base):
    __tablename__ = "coach_careers"

    id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=False, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False, index=True)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=True)

    coach = relationship("Coach", back_populates="career")
    team = relationship("Team")

    
class Stadium(Base):
    __tablename__ = "stadiums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    address = Column(String)
    capacity = Column(Integer)
    image = Column(String, nullable=True)

    teams = relationship("Team", back_populates="stadium")


class Referee(Base):
    __tablename__ = "referees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    salary = Column(Integer)

    fixtures = relationship("Fixture", back_populates="referee")


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    league_type = Column(String)
    logo = Column(String, nullable=True)

    season_stats = relationship("TeamSeasonStats", back_populates="league")

    @property
    def seasons(self):
        seasons = [
            team_season_stat.season
            for team_season_stat in self.season_stats
            if team_season_stat.season
        ]
        unique_seasons = {season.id: season for season in seasons}
        return [unique_seasons[season_id] for season_id in sorted(unique_seasons)]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=VIEWER)

    tokens = relationship("Token", back_populates="user")


class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    expires_at = Column(TIMESTAMP(timezone=True), index=True)

    user = relationship("User", back_populates="tokens")


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)

    contracts = relationship("Contract", back_populates="season")
    player_season_stats = relationship("PlayerSeasonStats", back_populates="season")
    team_season_stats = relationship("TeamSeasonStats", back_populates="season")


class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    season_id = Column(Integer, ForeignKey("seasons.id"))

    player = relationship("Player", back_populates="contracts")
    team = relationship("Team", back_populates="contracts")
    season = relationship("Season", back_populates="contracts")


class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"

    __table_args__ = (
        UniqueConstraint("player_id", "fixture_id", name="_player_fixture_uc"),
    )

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    fixture_id = Column(Integer, ForeignKey("fixtures.id"), index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), index=True)

    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)

    player = relationship("Player", back_populates="match_stats")
    fixture = relationship("Fixture", back_populates="players_stats")


class PlayerSeasonStats(Base):
    __tablename__ = "player_season_stats"

    __table_args__ = (
        UniqueConstraint("player_id", "season_id", name="_player_season_uc"),
    )

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), index=True)

    total_goals = Column(Integer, default=0)
    total_assists = Column(Integer, default=0)
    total_minutes = Column(Integer, default=0)
    avg_rating = Column(String, default=None)

    player = relationship("Player", back_populates="season_stats")
    season = relationship("Season", back_populates="player_season_stats")


class TeamSeasonStats(Base):
    __tablename__ = "team_season_stats"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)

    fixtures = Column(JSONB, nullable=True)
    goals = Column(JSONB, nullable=True)
    clean_sheet = Column(JSONB, nullable=True)
    failed_to_score = Column(JSONB, nullable=True)
    penalty = Column(JSONB, nullable=True)
    cards = Column(JSONB, nullable=True)

    team = relationship("Team", back_populates="season_stats")
    season = relationship("Season", back_populates="team_season_stats")
    league = relationship("League", back_populates="season_stats")
