angular.module('GiddleApp.services', [])
    .factory('giddleService', function($http) {
        var giddleAPI = {};

        giddleAPI.getQuestion = function() {
            return $http({
                method: 'JSON',
                url: 'http://'+document.location.host+'/get_question'
            });
        };

        giddleAPI.propose = function(proposal) {
            return $http({
                method: 'GET',
                url: 'http://'+document.location.host+'/evaluate_answer',
                params: {proposal: proposal}
            });
        };

        return giddleAPI;
    });