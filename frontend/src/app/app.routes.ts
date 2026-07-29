import { Routes } from '@angular/router';

import { Home } from './pages/home/home';
import { Login } from './pages/login/login';
import { NotFound } from './pages/not-found/not-found';
import { Dashboard } from './pages/dashboard/dashboard';

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
		path: '**',
		component: NotFound,
	},
];
