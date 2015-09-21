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
;



