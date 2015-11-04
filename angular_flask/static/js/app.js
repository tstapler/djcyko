'use strict';

angular.module('AngularFlask', ['angularFlaskServices'])
.config(['$routeProvider', '$locationProvider',
        function($routeProvider, $locationProvider) {
            $routeProvider
            .when('/', {
                templateUrl: '/static/partials/landing.html',
                controller: IndexController
            })
            .when('/about', {
                templateUrl: '/static/partials/about.html',
                controller: AboutController
            })
            .when('/song', {
                templateUrl: '/static/partials/song-list.html',
                controller: SongListController
            })
            .when('/song/:songId', {
                templateUrl: '/static/partials/song-detail.html',
                controller: SongDetailController
            })
            .when('/songs', {
                templateUrl: '/static/partials/song-list.html',
                controller: SongListController
            })
            .when('/queue', {
                templateUrl: '/static/partials/queue-list.html',
                controller: QueueListController
            })
            .when('/queue/:queueId',{
                templateUrl: '/static/partials/queue-detail.html',
                controller: QueueDetailController
            })
            .when('/queue/:queueId/dj',{
                templateUrl: '/static/partials/queue-dj.html',
                controller: QueueDJController
            })
            .when('/queue/:queueId/client', {
                templateUrl: '/static/partials/queue-client.html',
                controller: QueueClientController
            })
            .when('/login', {
                templateUrl: 'static/partials/login.html',
                controller: loginController
            })
            .when('/logout', {
                controller: logoutController
            })
            .when('/register', {
                templateUrl: 'static/partials/register.html'
                , controller: registerController
            })
            .otherwise({
                redirectTo: '/'
            })


            $locationProvider.html5Mode(true);
        }])
        ;
