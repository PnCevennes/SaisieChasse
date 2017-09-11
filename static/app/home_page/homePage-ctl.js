app.controller('homePageCtrl', ['$scope', 'loginSrv', '$http', function($scope,
  loginSrv, $http) {
  var self = this;

  self.taxons = {};

  $http({
    method: 'GET',
    url: 'api/bilan/nomvern_massif'
  }).then(
    function successCallback(response) {
      self.taxons = response.data;
    },
    function errorCallback(response) {
      // called asynchronously if an error occurs
      // or server returns response with an error status.
    }
  );


  self.userRights = loginSrv.getCurrentUserRights();

  self.drawGraphs = function() {
    $http({
      method: 'GET',
      url: 'api/bilan/attribution_massif?nom_vern=' + self.selectedTaxon +
        '&massif=' + self.selectedMassif
    }).then(
      function successCallback(response) {
        if (self.chart) {
          self.chart.destroy();
          self.chart = undefined;
        }
        var data = response.data;
        if (data.length == 0) {
          return;
        }
        var formated = {};
        //traitement des données
        formated.categories = data.map(function(n, i) {
          return (n.saison);
        });
        formated.series = [{
          type: 'column',
          name: 'nb_affecte_min',
          data: data.map(function(n, i) {
            return (n.nb_affecte_min);
          })
        }, {
          type: 'column',
          name: 'nb_affecte_max',
          data: data.map(function(n, i) {
            return (n.nb_affecte_max);
          })
        }, {
          type: 'spline',
          name: 'nb_realise_avant11',
          data: data.map(function(n, i) {
            return (n.nb_realise_avant11);
          }),
          marker: {
            lineWidth: 2,
            lineColor: Highcharts.getOptions().colors[3],
            fillColor: 'white'
          }
        }, {
          type: 'spline',
          name: 'nb_realise',
          data: data.map(function(n, i) {
            return (n.nb_realise);
          }),
          marker: {
            lineWidth: 2,
            lineColor: Highcharts.getOptions().colors[3],
            fillColor: 'white'
          }
        }];

        self.chart = new Highcharts.chart('graphs', {
          title: {
            text: 'Réalisation pan de chasse ' + data[0].nom_vern +
              ' - ' + data[0].massif
          },
          xAxis: {
            categories: formated.categories,
            title: {
              text: 'Saison'
            }
          },
          yAxis: {
            title: {
              text: 'Nombre'
            }
          },
          series: formated.series
        });

        self.chart.redraw();

      },
      function errorCallback(response) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
      });
  }


}]);
