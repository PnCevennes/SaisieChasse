var app = angular.module(
    'saisieChasseApp',
    ['ngRoute','ui.bootstrap']
);

app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'static/app/listeBracelet.html',
                controller: 'listeBraceletCtrl'
            }).
            otherwise({
                redirectTo: '/'
            });
    }
]);
