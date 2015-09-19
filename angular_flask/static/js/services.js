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
;



