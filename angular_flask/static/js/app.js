'use strict';

var AngularFlask = angular.module('AngularFlask', ['angularFlaskServices','ngRoute','ui.bootstrap'])
.config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $routeProvider
            .when('/', {
                templateUrl: '/static/partials/landing.html',
                access: {restricted: false}
            })
            .when('/about', {
                templateUrl: '/static/partials/about.html',
                controller: AboutController,
                access: {restricted: false}
            })
            .when('/song', {
                templateUrl: '/static/partials/song-list.html',
                controller: SongListController,
                access: {restricted: true}
            })
            .when('/song/:songId', {
                templateUrl: '/static/partials/song-detail.html',
                controller: SongDetailController,
                access: {restricted: true}
            })
            .when('/songs', {
                templateUrl: '/static/partials/song-list.html',
                controller: SongListController,
                access: {restricted: true}
            })
            .when('/queue', {
                templateUrl: '/static/partials/queue-list.html',
                controller: QueueListController,
                access: {restricted: true}
            })
            .when('/queue/:queueId',{
                templateUrl: '/static/partials/queue-detail.html',
                controller: QueueDetailController,
                access: {restricted: true}
            })
            .when('/queue/:queueId/dj',{
                templateUrl: '/static/partials/queue-dj.html',
                controller: QueueDJController,
                access: {restricted: true}
            })
            .when('/queue/:queueId/client', {
                templateUrl: '/static/partials/queue-client.html',
                controller: QueueClientController,
                access: {restricted: true}
            })
            .when('/login', {
                templateUrl: 'static/partials/login.html',
                controller: loginController,
                access: {restricted: false}
            })
            .when('/logout', {
                controller: logoutController,
                access: {restricted: false}
            })
            .when('/register', {
                templateUrl: 'static/partials/register.html',
                controller: registerController,
                access: {restricted: false}
            })
            .otherwise({
                redirectTo: '/'
            })


            $locationProvider.html5Mode(true);
        }])
        ;
        AngularFlask.run (function ($rootScope, $location, $route, AuthService) {
            $rootScope.$on('$routeChangeStart', function (event, next, current){
                if(next.access.restricted && AuthService.isLoggedIn() === false) {
                    $location.path('/login');
                    $route.reload();
                }
            });
        });
