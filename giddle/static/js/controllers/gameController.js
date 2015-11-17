angular.module('GiddleApp.controllers', [])
    .controller('gameController', ['$scope', '$timeout', 'giddleService', function($scope, $timeout, giddleService) {
        $scope.newQuestion = function() {
            if (!$scope.score)
                $scope.score = 0;
            $scope.status = null;
            $scope.question = "";
            $scope.answers = [];

            giddleService.getQuestion().then(function(response) {
                $scope.question = response.data.question + '...';
                $scope.status = 'guessing';
            });
        }

        $scope.propose = function() {
            giddleService.propose($scope.proposal).then(function(response) {
                console.log(response.data);
                $scope.answers = response.data.answers;
                $scope.score = response.data.score;
                $scope.status = null;
                $scope.correct = response.data.correct;
                $timeout(function() {
                    $scope.correct = undefined;
                    $scope.proposal = response.data.hint ? response.data.hint+' ' : '';
                    $scope.status = response.data.status;
                }, 1000);
            });
        }

        $scope.newQuestionIfNeeded = function(){
            if ($scope.status == 'won' || $scope.status == 'lost')
                $scope.newQuestion();
        }
    }]);