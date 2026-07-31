export interface Team {
  id: number;
  name: string;
  city?: string | null;
  logo?: string | null;
  coach_id?: number | null;
  stadium_id?: number | null;
}

export interface Season {
  id: number;
}

export interface Player {
  id: number;
  name: string;
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

export interface PlayerWithSeasonStats {
  player: Player;
  stats: PlayerSeasonStats;
}
