'use strict';

angular.module('angularFlaskServices', ['ngResource'])
	.factory('Song', function($resource) {
		return $resource('/api/song/:songId', {}, {
			query: {
				method: 'GET',
				params: { songId: '' },
				isArray: true
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
;



