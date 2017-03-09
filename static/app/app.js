var app = angular.module(
    'saisieChasseApp',
    ['ngRoute','ui.bootstrap','ngCookies','toaster']
);
app.service('locationHistoryService', function(){
    return {
        previousLocation: null,

        store: function(location){
            //@TODO COMPRENDRE
            this.previousLocation = location.replace('#!/', '');
        },

        get: function(){
            return this.previousLocation;
        }
      }
})
.run(['$rootScope', '$location', 'locationHistoryService','loginSrv','toaster',
  function($rootScope, $location, locationHistoryService,loginSrv, toaster){
    $rootScope.$on('$routeChangeStart', function (event, next, current) {
      //Stockage de la dernière route
      if (current) {
        locationHistoryService.store(location.hash);
      }
      else{
        current = '/';
      }
      if (!next.access) return;

      if (next.access.restricted) {
        (next.access.level === undefined) ? level = 0 : level= next.access.level;
        if ((loginSrv.getToken() !== undefined) && (level <= loginSrv.getCurrentUser().id_droit_max)) return;
        toaster.pop('error', 'Vous devez être identifié et avoir un niveau de droit suffisant', '', 2000, 'trustedHtml');
        $location.path(current);
      }
    });
}]);
app.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider
            .when('/login', {
                templateUrl: 'static/app/login/form.html',
                controller: 'loginFormCtrl',
                controllerAs: 'ctrl'
            })
            .when('/saisie_chasse', {
                templateUrl: 'static/app/saisie_chasse/saisieChasse-tpl.html',
                controller: 'saisieChasseCtrl',
                controllerAs: 'ctrl',
                access: {restricted: true, "level":3}
            })
            .when('/', {
                templateUrl: 'static/app/home_page/home-tpl.html',
                controller: 'homePageCtrl',
                controllerAs: 'ctrl'
            }).
            otherwise({
                redirectTo: '/'
            });
    }
]);
