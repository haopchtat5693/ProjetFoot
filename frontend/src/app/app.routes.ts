import { Routes } from '@angular/router';

import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { NotFound } from './pages/not-found/not-found';
import { Teams } from './pages/teams/teams';
import { Players } from './pages/players/players';
import { Coaches } from './pages/coaches/coaches';
import { Leagues } from './pages/leagues/leagues';
import { LeagueDetail } from './pages/league-detail/league-detail';
import { Stadiums } from './pages/stadiums/stadiums';
import { TeamDetail } from './pages/team-detail/team-detail';
import { PlayerDetail } from './pages/player-detail/player-detail';
import { CoachDetail } from './pages/coach-detail/coach-detail';
import { StadiumDetail } from './pages/stadium-detail/stadium-detail';
import { SearchResults } from './pages/search-results/search-results';
import { Fixtures } from './pages/fixtures/fixtures';
import { FixtureDetail } from './pages/fixture-detail/fixture-detail';

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
		path: 'coaches',
		component: Coaches,
	},
	{
		path: 'coaches/:coachId',
		component: CoachDetail,
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
		path: 'fixtures',
		component: Fixtures,
	},
	{
		path: 'fixtures/:fixtureId',
		component: FixtureDetail,
	},
	{
		path: '**',
		component: NotFound,
	},
];
