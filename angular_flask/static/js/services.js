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
            }
        });
    })

    .factory('socket', function (socketFactory){
        return socketFactory({
            prefix: '',
	    ioSocket: io.connect('http://localhost:5000/client')
        }
        );
    })

    .factory('AuthService', ['$q', '$timeout', '$http', function($q, $timeout, $http) {
        //create user variable
        var user = null;
	var name = '';
	var user_id = -1;
        // return available functions for use in controllers
        
	var statusMessage = 'lol';

	function getStatusMessage() {
		return statusMessage;
	}

	function getUserID(){
		return user_id;
	}

	// return available functions for use in controllers
        function isLoggedIn() {
            if(user) {
                return true;
            } else {
                return false;
            }
        }

	function updateUserID(){
            var deferred = $q.defer();

	    	var filters = [{name: "username", op: "eq", val: name}];
		$http.get('api/user',{"params": { "q": {"filters": filters, "single":true}}, "content-headers": "application/json"}) 
		.success(function (data, status) {
			user_id = data.id;
			deferred.resolve();
		})
		.error(function (data) {
			deferred.reject();
			user_id = -2;
		});
		return deferred.promise;
	}

        function login(username, password) {

            // create a new instance of deferred
            var deferred = $q.defer();

            // send a post request to the server
            $http.post('/api/login', {username: username, password: password})
            // handle success
            .success(function (data, status) {
                if(status === 200 && data.result){
		    name = username
                    user = true;
		    updateUserID()
                    deferred.resolve();
                } else {
		    name = ''
                    user = false;
                    deferred.reject();
                }
            })
            // handle error
            .error(function (data) {
	        name = ''
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
	    $http.post('/api/logout', {username: name})
            // handle success
            .success(function (data) {
		name = ''
                user = false;
                deferred.resolve();
            })
            // handle error
            .error(function (data) {
		name = ''
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
                if(data.result == 'Success'){
                    deferred.resolve();
		} else {
		    statusMessage = data.result;
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

	function nameIs() {
		return name
	}

        return ({
	    getStatusMessage: getStatusMessage,
            isLoggedIn: isLoggedIn,
            login: login,
            logout: logout,
            register: register,
	    nameIs : nameIs,
	    getUserID: getUserID,
	    updateUserID: updateUserID
        });
    }]);

