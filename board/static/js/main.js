app = angular.module('demoapp', ['ngResource']);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller('DemoCtrl', ['$scope', function($scope) {
    $scope.num = 0;
    $scope.save = function() {
      $(".data").html("Click: " + $scope.num);
      $scope.num += 1;
    };
}]);


app.controller('NameCtrl', ['$scope', function($scope) {
  $scope.users = [
    {'first_name': 'Buddy', 'last_name': 'Lindsey'},
    {'first_name': 'John', 'last_name': 'Doe'}
  ];
}]);



app.controller('AddNameCtrl', ['$scope', function($scope) {
    $scope.save = function(name) {
      $.ajax({
        url: "/name/",
        method: "POST",
        data: {
          first_name: name.first_name,
          last_name: name.last_name
        },
        dataType: "json",
        success: function(data){
          $(".message").html(data.message);
        },
        error: function(data){
          $(".message").html(data);
        }
      });
    };
}]);




app.factory('Name', ['$resource', function($resource) {
    return $resource('/api/names/:id', {"id": this.id});
}]);

app.config([
  '$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  }
]);

app.controller('NameTwoCtrl', ['$scope', 'Name', function($scope, Name) {
    $scope.names = Name.query();
    $scope.save = function(name) {
      var newName = new Name(name);
      newName.$save().then(function(result){
        $scope.names.push(result)
      });
    };
}]);


