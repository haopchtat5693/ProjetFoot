from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from app.core.constants import VIEWER


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    away_team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    date = Column(String)
    location = Column(String)
    result = Column(String)
    referee_id = Column(Integer, ForeignKey("referees.id"), index=True)

    home_team = relationship("Team", foreign_keys=[home_team_id], back_populates="home_matches")
    away_team = relationship("Team", foreign_keys=[away_team_id], back_populates="away_matches")
    referee = relationship("Referee", back_populates="matches")
    stats = relationship("PlayerMatchStats", back_populates="match")

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    logo = Column(String, nullable=True)

    coach_id = Column(Integer, ForeignKey("coaches.id"), nullable=True, index=True)
    stadium_id = Column(Integer, ForeignKey("stadiums.id"), nullable=True, index=True)

    stadium = relationship("Stadium", back_populates="teams")
    coach = relationship("Coach", back_populates="team")
    players = relationship("Player", back_populates="team")
    home_matches = relationship("Match", foreign_keys=[Match.home_team_id], back_populates="home_team")
    away_matches = relationship("Match", foreign_keys=[Match.away_team_id], back_populates="away_team")
    contracts = relationship("Contract", back_populates="team")
    season_stats = relationship("TeamSeasonStats", back_populates="team")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    age = Column(Integer, index=True)
    salary = Column(Integer)
    main_foot = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id"), index=True)

    team = relationship("Team", back_populates="players")
    match_stats = relationship("PlayerMatchStats", back_populates="player")
    season_stats = relationship("PlayerSeasonStats", back_populates="player")
    contracts = relationship("Contract", back_populates="player")

class Coach(Base):
    __tablename__ = "coaches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    salary = Column(Integer)

    team = relationship("Team", back_populates="coach")

class Stadium(Base):
    __tablename__ = "stadiums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    address = Column(String)
    capacity = Column(Integer)

    teams = relationship("Team", back_populates="stadium")

class Referee(Base):
    __tablename__ = "referees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)
    salary = Column(Integer)

    matches = relationship("Match", back_populates="referee")

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    country = Column(String)

    season_stats = relationship("TeamSeasonStats", back_populates="league")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default=VIEWER)

    tokens = relationship("Token", back_populates="user")

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user = relationship("User", back_populates="tokens")

class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    contracts = relationship("Contract", back_populates="season")
    match_stats = relationship("PlayerMatchStats", back_populates="season")
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

    __table_args__ = (UniqueConstraint('player_id', 'match_id', name='_player_match_uc'),)
    
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True) 
    season_id = Column(Integer, ForeignKey("seasons.id"), index=True) 
    
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    yellow_cards = Column(Integer, default=0)
    red_cards = Column(Integer, default=0)
    minutes_played = Column(Integer, default=0)

    player = relationship("Player", back_populates="match_stats")
    match = relationship("Match" , back_populates="stats")
    season = relationship("Season", back_populates="match_stats")

class PlayerSeasonStats(Base):
    __tablename__ = "player_season_stats"

    __table_args__ = (UniqueConstraint('player_id', 'season_id', name='_player_season_uc'),)
    
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
    
