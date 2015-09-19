'use strict';

/* Controllers */

function IndexController($scope) {

}

function AboutController($scope) {

}

function SongListController($scope, Song) {
	var songsQuery = Song.get({}, function(songs) {
		$scope.songs = songs.objects;
        $scope.convert = function(url){
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            var match = url.match(regExp);

            if (match && match[2].length == 11) {
                        return match[2];

            } else {
                        return 'error';

            }
        }
	});
}

function SongDetailController($scope, $routeParams, Song) {
	var songQuery = Song.get({ songId: $routeParams.songId }, function(song) {
		$scope.song = song;
        $scope.convert = function(url){

            var video_id = url.split('v=')[1];
            try {
                var ampersandPosition = video_id.indexOf('&');
            }
            catch(err) {
                return "http://youtube.com/embed/" + video_id
            }
            if(ampersandPosition != -1) {
                  video_id = video_id.substring(0, ampersandPosition);
            }

            return "http://youtube.com/embed/" + video_id
        }
	});
}

function QueueListController($scope, Queue){
    var queueQuery =Queue.get ({},function(queues){
        $scope.queues = queues.objects;
    });
}

function QueueDetailController($scope, $routeParams, Queue) {
    var queueQuery = Queue.get({queueId: $routeParams.queueId }, function(queue){
        $scope.queue = queue;
    });
}

function QueueDJController($scope, $routeParams, Queue){
    var queueQuery = Queue.get({queueId: $routeParams.queueId }, function(queue){
        $scope.queue = queue;
    });
}

function QueueClientController($scope, $routeParams, Queue){
    var queueQuery = Queue.get({queueId: $routeParams.queueId }, function(queue){
        $scope.queue = queue;
    });
}
