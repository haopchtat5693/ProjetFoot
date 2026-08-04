import { Routes } from '@angular/router';

import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { NotFound } from './pages/not-found/not-found';
import { Teams } from './pages/teams/teams';
import { Players } from './pages/players/players';
import { Leagues } from './pages/leagues/leagues';
import { LeagueDetail } from './pages/league-detail/league-detail';
import { Stadiums } from './pages/stadiums/stadiums';
import { TeamDetail } from './pages/team-detail/team-detail';
import { PlayerDetail } from './pages/player-detail/player-detail';
import { StadiumDetail } from './pages/stadium-detail/stadium-detail';
import { SearchResults } from './pages/search-results/search-results';

export const routes: Routes = [
	{
		path: '',
		component: Home,
		pathMatch: 'full',
	},
	{
		path: 'login',
		component: Login,
	},
	{
		path: 'search',
		component: SearchResults,
	},
	{
		path: 'teams',
		component: Teams,
	},
	{
		path: 'teams/:teamId',
		component: TeamDetail,
	},
	{
		path: 'players',
		component: Players,
	},
	{
		path: 'players/:playerId',
		component: PlayerDetail,
	},
	{
		path: 'leagues',
		component: Leagues,
	},
	{
		path: 'leagues/:leagueId',
		component: LeagueDetail,
	},
	{
		path: 'stadiums',
		component: Stadiums,
	},
	{
		path: 'stadiums/:stadiumId',
		component: StadiumDetail,
	},
	{
		path: '**',
		component: NotFound,
	},
];
