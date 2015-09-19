'use strict';

angular.module('AngularFlask', ['angularFlaskServices'])
	.config(['$routeProvider', '$locationProvider',
		function($routeProvider, $locationProvider) {
		$routeProvider
		.when('/', {
			templateUrl: 'static/partials/landing.html',
			controller: IndexController
		})
		.when('/about', {
			templateUrl: 'static/partials/about.html',
			controller: AboutController
		})
		.when('/song', {
			templateUrl: 'static/partials/song-list.html',
			controller: SongListController
		})
		.when('/song/:songId', {
			templateUrl: '/static/partials/song-detail.html',
			controller: SongDetailController
		})
		/* Create a "/blog" route that takes the user to the same place as "/song" */
		.when('/songs', {
			templateUrl: 'static/partials/song-list.html',
			controller: SongListController
		})
		.otherwise({
			redirectTo: '/'
		})
		;

		$locationProvider.html5Mode(true);
	}])
;
