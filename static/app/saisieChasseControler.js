app.controller('listeBraceletCtrl',
  function($scope, $http,  $filter) {
	$scope.listBracelets= [],
	$scope.listCommunes= [],
	$scope.listLieuDits = [],
	$scope.listAuteurs= [],
	$scope.listZi=[],
	$scope.errors=[],
	$scope.currentBracelet=undefined,

  //@TODO : mettre en paramètre la saison de chasse
	$http.get("/api/plan_chasse/bracelets_list/4")
		.then(function(response) {
        	$scope.listBracelets = response.data
    	})
    	.catch( function(response) {
        	$scope.errors.push(response.data.message);
    	});

    $http.get('/api/lieux/communes')
	    .then(function(response) {
	    	response.data.push({"id":-1, "value":"INCONNU"});
	    	$scope.listCommunes = response.data;
		})
		.catch( function(response) {
			$scope.errors.push(response.data.message);
		});

    $http.get('/api/plan_chasse/auteurs')
	    .then(function(response) {
	    	$scope.listAuteurs = response.data
		})
		.catch( function(response) {
			$scope.errors.push(response.data.message);
		});

    $http.get('/api/thesaurus/vocabulary/4?ilikeHierachie=004.00%25.%25')
	    .then(function(response) {
	    	$scope.listZi = response.data;
	    	angular.forEach($scope.listZi, function(value, key) {
			 $scope.listZi[key].code = parseInt(value.code);
			});
		})
		.catch( function(response) {
			$scope.errors.push(response.data.message);
		});
  $scope.onSelectBracelet = function ($item, $model, $label) {
    $http.get("/api/plan_chasse/bracelet/"+$item.id)
    .then(function(response) {
      data = response.data
      $scope.selectedCommune=undefined;
      $scope.selectedLieuDit=undefined;
          $scope.currentBracelet = data;
          if ($scope.currentBracelet.date_exacte) $scope.currentBracelet.date_exacte = new Date($filter('date')(data.date_exacte, 'yyyy-MM-dd'));
          if (data.cd_com) {
            $scope.selectedCommune = $filter('filter')($scope.listCommunes, {id:data.cd_com})[0];
          }
          if (data.pk_nom_lieudit) {
            $http.get('/api/lieux/'+data.pk_nom_lieudit)
        .then(function(response) {
            $scope.selectedLieuDit =response.data[0];
        }).catch(function(response) {
          $scope.errors.push(response.data.message);});
          }
      })
      .catch(function(response) {
          $scope.errors.push(response.data.message);
      });
  };

  $scope.onSelectCommune = function ($item, $model, $label) {
	   $http.get("/api/lieux/?code_com="+$item.id)
			.then(function(response) {
	        	$scope.listLieuDits = response.data;
	    	})
	    	.catch( function(response) {
	        	$scope.errors.push(response.data.message);
	    	});
	};

	$scope.update = function() {
		 //if form is not valid then return the form.
	     if(!$scope.saisieform.$valid) {
	       alert("formulaire non valide");
	       return;
	     }

		var currentData = $scope.currentBracelet;
		if (!currentData.date_exacte) currentData.date_exacte = new Date('0001-01-01');
		currentData.date_exacte = $filter('date')(currentData.date_exacte, 'yyyy-MM-ddT00:00:00Z');
    currentData.auteur_constat = [].concat(currentData.auteur_constat).join();
    currentData.auteur_tir = [].concat(currentData.auteur_tir).join();
		$http.post('/api/plan_chasse/bracelet/'+currentData.id, currentData)
	        .then(function(response) {
	            alert(response.data.message);
	            $scope.currentBracelet=undefined;
	            $scope.selectedBracelet=undefined;
	        })
	        .catch( function(response) {
	            alert("Error: "+response.error+" Post to server failed.\nStatus: "+response.status);
	        });
	};

	$scope.open = function($event) {
	    $scope.status.opened = true;
  	};

	$scope.status = {
		opened: false
	};

	$scope.parseInt = parseInt;
});



app.directive('thesaurus', ['$http', function ($http) {
    return {
        scope: {
        	idtype: '@idtype',
        	storageField: '@stf',
        	queryParam : '@queryparam',
        	myDirectiveVar: '=',
        	isDisabled:'=?',
        	isRequired:'=?',
        },
        template: '<select ng-disabled="isDisabled"  ng-required="isRequired" ng-model="myDirectiveVar" class="form-control" req><option ng-repeat="obj in list" value="{{obj[storageField]}}">{{obj.libelle}}</option></select>',
		controller: function($scope, $http){
			$scope.isDisabled = angular.isDefined($scope.isDisabled) ? $scope.isDisabled : false;
			$scope.isRequired = angular.isDefined($scope.isRequired) ? $scope.isRequired : false;

			var query = $scope.idtype;
		    if ($scope.queryParam) query += '?'+$scope.queryParam
			$http.get("/api/thesaurus/vocabulary/"+query)
				.then(function(response) {
		        	$scope.list = response.data
		    	})
		    	.catch( function(response) {
		        	console.log(response);
		    	});
		},
    };

}]);
