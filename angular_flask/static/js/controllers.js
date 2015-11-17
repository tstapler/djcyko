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
            });
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

function QueueClientController($scope, $routeParams, Queue, Song){
    var queueQuery = Queue.get({queueId: $routeParams.queueId }, function(queue){
            $scope.queue = queue;
            });
    $scope.get_song = function(){
    $scope.model
    }
    $scope.save = function () {
        if(this.queue.songId === undefined) {
            $scope.alert = {showAlert:true, msg: 'Select something please!', alertClass: 'warning'};
        }
         else {
            this.queue.songs[this.queue.songId].votes += 1
            delete this.queue.songId

            this.queue.$save()

        };

    };
    $scope.vote = function() {
     if(this.queue.song_title === undefined || this.queue.song_url === undefined)
     {
        alert("Please fill out both fields")
     }
     else {
    var newSong = new Song({title: this.queue.song_title, url: this.queue.song_url, votes: 0, playing: 1, queue_id: $routeParams.queueId})
    newSong.$save()
    $scope.queue.$get({queueId: $routeParams.queueId})
     }
    }
}

function loginController($scope, $location, AuthService){
    console.log(AuthService.isLoggedIn());
    $scope.login = function () {
        console.log("Logging In....");

        // initial values
        $scope.error = false;
        $scope.disabled = true;

        // call login from service
        AuthService.login($scope.loginForm.username, $scope.loginForm.password)
        // handle success
        .then(function () {
            $location.path('/');
            $scope.disabled = false;
            $scope.loginForm = {};
        })
        // handle error
        .catch(function () {
            $scope.error = true;
            $scope.errorMessage = "Invalid username and/or password";
            $scope.disabled = false;
            $scope.loginForm = {};
        });

    };
}

function logoutController($scope, $location, AuthService) {

    $scope.logout = function () {

        console.log(AuthService.isLoggedIn());

        // call logout from service
        AuthService.logout()
        .then(function () {
            $location.path('/login');
        });

    };
}

function registerController($scope, $location, AuthService) {

    $scope.register = function () {

        // initial values
        $scope.error = false;
        $scope.disabled = true;

        // call register from service
        AuthService.register($scope.registerForm.email, $scope.registerForm.password)
        // handle success
        .then(function () {
            $location.path('/login');
            $scope.disabled = false;
            $scope.registerForm = {};
        })
        // handle error
        .catch(function () {
            $scope.error = true;
            $scope.errorMessage = "Something went wrong!";
            $scope.disabled = false;
            $scope.registerForm = {};
        });

    };
}
