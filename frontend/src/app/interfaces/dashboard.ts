export interface Team {
  id: number;
  name: string;
  country?: string | null;
  city?: string | null;
  logo?: string | null;
  stadium_id?: number | null;
}

export interface Stadium {
  id: number;
  name: string;
  city: string;
  address: string;
  capacity: number;
  image?: string | null;
}

export interface League {
  id: number;
  name: string;
  country: string;
  logo?: string | null;
  league_type?: string | null;
  seasons?: Season[];
}

export interface LeagueLookupQuery {
  id?: number;
  search?: string;
  season?: number;
  team?: number;
  type?: string;
}

export interface Season {
  id: number;
}

export interface Player {
  id: number;
  name: string;
  nationality?: string | null;
  position?: string | null;
  age?: number | null;
  photo?: string | null;
}

export interface PlayerSeasonStats {
  id: number;
  player_id: number;
  season_id: number;
  total_goals?: number | null;
  total_assists?: number | null;
  total_minutes?: number | null;
  avg_rating?: string | null;
}

export interface CoachCareerTeam {
  id: number;
  name: string;
  logo?: string | null;
}

export interface CoachCareer {
  team: CoachCareerTeam;
  start: string;
  end?: string | null;
}

export interface Coach {
  id: number;
  name: string;
  age?: number | null;
  nationality?: string | null;
  photo?: string | null;
  career?: CoachCareer[];
}

export interface PlayerWithSeasonStats {
  player: Player;
  stats: PlayerSeasonStats;
}

export interface TeamSeasonStats {
  id: number;
  team_id: number;
  league_id: number;
  season_id: number;
  fixtures?: Record<string, unknown> | null;
  goals?: Record<string, unknown> | null;
  clean_sheet?: Record<string, unknown> | null;
  failed_to_score?: Record<string, unknown> | null;
  penalty?: Record<string, unknown> | null;
  cards?: Record<string, unknown> | null;
}
