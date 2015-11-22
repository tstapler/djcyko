'use strict';

angular.module('angularFlaskServices', ['ngResource'])
	.factory('Song', function($resource) {
		return $resource('/api/song/:songId', {}, {
            get:{
                method: 'GET'
            },
			query: {
				method: 'GET',
                params: { songId: '' },
				isArray: true
			},
            update:{
                method: 'POST'
            }
		});
	})

    .factory('Queue', function($resource) {
        return $resource('/api/queue/:queueId',{},{
            query: {
                method: 'GET',
                params: { queueId: '' },
                isArray: true
            },
            update:{
                method: 'POST',
                params: { queueId: '' },
                headers: {
                     'Content-Type': 'application/json'

            }},
            save:{
                 method: 'PUT',
                params: { queueId: '@id' },
                headers: {
                     'Content-Type': 'application/json'
                },
                data: ''
            }
        });
    })

    .factory('socket', function (socketFactory){
        return socketFactory();
    })

    .factory('AuthService', ['$q', '$timeout', '$http', function($q, $timeout, $http) {
        //create user variable
        var user = null;
        // return available functions for use in controllers
        function isLoggedIn() {
            if(user) {
                return true;
            } else {
                return false;
            }
        }

        function login(username, password) {

            // create a new instance of deferred
            var deferred = $q.defer();

            // send a post request to the server
            $http.post('/api/login', {username: username, password: password})
            // handle success
            .success(function (data, status) {
                if(status === 200 && data.result){
                    user = true;
                    deferred.resolve();
                } else {
                    user = false;
                    deferred.reject();
                }
            })
            // handle error
            .error(function (data) {
                user = false;
                deferred.reject();
            });

            // return promise object
            return deferred.promise;

        }

        function logout() {

            // create a new instance of deferred
            var deferred = $q.defer();

            // send a get request to the server
            $http.get('/api/logout')
            // handle success
            .success(function (data) {
                user = false;
                deferred.resolve();
            })
            // handle error
            .error(function (data) {
                user = false;
                deferred.reject();
            });

            // return promise object
            return deferred.promise;

        }

        function register(username, password) {

            // create a new instance of deferred
            var deferred = $q.defer();

            // send a post request to the server
            $http.post('/api/register', {username: username, password: password})
            // handle success
            .success(function (data, status) {
                if(status === 200 && data.result){
                    deferred.resolve();
                } else {
                    deferred.reject();
                }
            })
            // handle error
            .error(function (data) {
                deferred.reject();
            });

            // return promise object
            return deferred.promise;

        }

        return ({
            isLoggedIn: isLoggedIn,
            login: login,
            logout: logout,
            register: register
        });
    }]);

