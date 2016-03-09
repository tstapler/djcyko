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

function QueueListController($scope, Queue, AuthService){
    function sortByUser(array){
	    var users_object = {}
	    for (var i in array) {
		    if(array[i].user != null){
		    var username = array[i].user.username
			    if(!users_object.hasOwnProperty(username)) {
				    users_object[username] = [];
				    users_object[username].push(array[i])
			    }
			    else {
				    users_object[username].push(array[i])
			    }
		    }
	    }
	    return users_object
    }
    var queueQuery = Queue.get ({},function(data){
		    $scope.queues = sortByUser(data.objects);
    });
    $scope.user = AuthService.nameIs;
    $scope.queue_name = "";
    $scope.newQueue = function() {
	    var to_add = new Queue({"title": $scope.queue_name, "user_id": AuthService.getUserID()})
	    to_add.$save();
	    Queue.get({}, function(data){
		    $scope.queues = sortByUser(data.objects);
	    });
    };
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

function NavController($scope, $routeParams, AuthService){
	$scope.logged_in = AuthService.isLoggedIn;
	$scope.nameIs = AuthService.nameIs;
}

function QueueClientController($scope, $routeParams, $location, socket, Queue, Song, youtubeEmbedUtils, AuthService){
    //The Video id of the current song
    $scope.current_song = "YQHsXMglC9A";
    $scope.player;

    //The control parameters for the youtube player
    $scope.playerVars = {
        controls: 0,
        autoplay: 1

    };

    //Begin Websocket Connection
    socket.connect;

    socket.on("connect", function(){
        socket.emit('join', {"queue": $scope.queue.id});
    });

    /* Control signals for the youtube player */
    socket.on("player-change", function(message, player) {
        switch(message["action"]) {
            case "new":
                $scope.player.loadVideoById(youtubeEmbedUtils.getIdFromURL(message["url"]));
                break;
            case "stop":
                $scope.player.pauseVideo();
                break;
            case "start":
                $scope.player.playVideo();
                break;
            case "seek":
		$scope.player.loadVideoById(youtubeEmbedUtils.getIdFromURL(message["url"], message["start"]));
                break;
        }
    });

    /* Voting updates */
    socket.on("vote", function(message) {
        var updated_songs = message['updated']
        for(var song in updated_songs){
            for(var exist_song in $scope.queue.songs){
                if($scope.queue.songs[exist_song].id === updated_songs[song]['id']){
                    $scope.queue.songs[exist_song].votes = updated_songs[song]['votes'];
                    return;
                }
            }
        }
    });

    //Request the next song to be played
    $scope.next = function() {
        socket.emit('player-control', {'new': 'True', 'queue': $scope.queue.id});
    };

    /* Controls for the stop and start button */
    $scope.button_state = "Stop Song"

    $scope.stop_start = function() {

        if($scope.button_state === "Stop Song")
            {
         socket.emit('player-control', {'stop': 'True', 'queue':$scope.queue.id});
            $scope.button_state = "Start Video";
            }
            else{
         socket.emit('player-control', {'start': 'True', 'queue':$scope.queue.id});
            $scope.button_state = "Stop Song";
            }
    }

    /* Submit a vote on the vote event */
    $scope.vote = function () {
        if(this.queue.songId === undefined) {
            $scope.alert = {showAlert:true, msg: 'Select something please!', alertClass: 'warning'};
        }
        else {
            socket.emit('vote', {"vote_for": this.queue.songId})
            delete this.queue.songId
        };
    };

    /* Submit a song suggestion */
    $scope.submit = function() {
        if(this.queue.song_title === undefined || this.queue.song_url === undefined)
            {
                alert("Please fill out both fields")
            }
            else {
                var newSong = new Song({title: this.queue.song_title, url: this.queue.song_url, votes: 0, playing: "False", queue_id: $routeParams.queueId})
                newSong.$save()
                $scope.queue.$get({queueId: $routeParams.queueId})
            }
    }

    //Old http request based stuff
    var queueQuery = Queue.get({queueId: $routeParams.queueId }, function(queue){
        $scope.queue = queue;
    });

    $scope.get_song = function(){
        $scope.model
    }

    $scope.deleteQueue = function() {
	    if(AuthService.getUserID() === $scope.queue.user_id)
	    {
	    Queue.delete({queueId: $scope.queue.id})
	    $location.path("/queue")
	    }
    }

    $scope.ownsQueue = function () {
	    try {
	    return AuthService.getUserID() === $scope.queue.user_id;
		} catch (e) {
	
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
            $location.path('/queue');
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

    $scope.logout = (function () {

        console.log(AuthService.isLoggedIn());

        // call logout from service
        AuthService.logout()
        .then(function () {
            $location.path('/login');
        });

    });
    $scope.logout();
    
}

function registerController($scope, $location, AuthService) {

    $scope.register = function () {

        // initial values
        $scope.error = false;
        $scope.disabled = true;

        // call register from service
        AuthService.register($scope.registerForm.username, $scope.registerForm.password)
        // handle success
        .then(function () {
            $location.path('/login');
            $scope.disabled = false;
            $scope.registerForm = {};
        })
        // handle error
        .catch(function () {
            $scope.error = true;
            $scope.errorMessage = AuthService.getStatusMessage();
            $scope.disabled = false;
            $scope.registerForm = {};
        });

    };
}
