app.controller('homePageCtrl', ['$scope','loginSrv', function($scope,loginSrv) {
    var self = this;
    self.userRights = loginSrv.getCurrentUserRights();
}]);
