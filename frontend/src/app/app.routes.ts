import { Routes } from '@angular/router';

import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { NotFound } from './pages/not-found/not-found';
import { Dashboard } from './pages/dashboard/dashboard';
import { Teams } from './pages/teams/teams';
import { Players } from './pages/players/players';
import { Stadiums } from './pages/stadiums/stadiums';
import { Stats } from './pages/stats/stats';

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
		path: 'dashboard',
		component: Dashboard,
	},
	{
		path: 'teams',
		component: Teams,
	},
	{
		path: 'players',
		component: Players,
	},
	{
		path: 'stadiums',
		component: Stadiums,
	},
	{
		path: 'stats',
		component: Stats,
	},
	{
		path: '**',
		component: NotFound,
	},
];
