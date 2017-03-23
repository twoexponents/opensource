
var app = angular.module('webApp', []);


app.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}')

}]);


app.controller('qosCtrl', ['$rootScope', '$scope', '$http', function($rootScope, $scope, $http) {
  $scope.hideform = true;
  $scope.options = {
    devices:['wired', 'wireless']
  };

  $scope.submit_form = {
    ssid: '',
    ap_ip: '',
    target_ip: '',
    target_prefix: '',
    target_ports:'',
    uplink:'',
    downlink:''
  };

  $scope.getList = function() {
    $http.get("http://interest.snu.ac.kr:8000/api/qos/all")
      .success(function(response) {
        $scope.aps = response;
      });
  };


  $scope.getList();

  $scope.editRecord = function(ap) {
    $scope.hideform = false;
    if (ap== 'new') {
      $scope.edit = true;
      $scope.incomplete = true;
      $scope.modified = false;

      $scope.submit_form.id ='';

      $scope.submit_form.ssid = '';
      $scope.submit_form.ap_ip= '';
      $scope.submit_form.target_ip = '';
      $scope.submit_form.target_prefix= '';
      $scope.submit_form.target_ports='';
      $scope.submit_form.uplink='';
      $scope.submit_form.downlink='';

    } else {
      $scope.edit = false;
      $scope.modified = true;

      $scope.submit_form.id =ap.id;

      $scope.submit_form.ssid = ap.ssid; 
      $scope.submit_form.ap_ip= ap.ap_ip;
      $scope.submit_form.target_ip = ap.target_ip;
      $scope.submit_form.target_prefix= ap.target_ip_prefix_bits;
      $scope.submit_form.target_ports=ap.target_ports;
      $scope.submit_form.uplink=ap.qos_bandwidth_uplink;
      $scope.submit_form.downlink=ap.qos_bandwidth_downlink;

    }

  };

  $scope.delRecord = function(ap) {
    var _url = "http://interest.snu.ac.kr:8000/api/qos/" + ap.id;
      $http.delete(_url).success(function(response) {
        $scope.getList();
        $scope.hideform = true;
      });
  };

  $scope.submit = function() {
    var _url = "http://interest.snu.ac.kr:8000/api/qos/" + $scope.submit_form.d;
    var req = {
      method:'POST',
      url:_url,
      headers:{'Content-Type':undefined},
      data:$scope.submit_form
    };

    if ($scope.modified) {
      req.method = 'PUT'; // temporary!
      $http(req).success(function(response) {
        $scope.getList();
        $scope.hideform = true;
      });
    } else {
      $http(req).success(function(response) {
        $scope.getList();
        $scope.hideform = true;
      });
    }
  };


  $scope.$watch('submit_form.ssid', function() {$scope.test();});
  $scope.$watch('submit_form.ap_ip', function() {$scope.test();});
  $scope.$watch('submit_form.target_ip', function() {$scope.test();});
  $scope.$watch('submit_form.target_prefix', function() {$scope.test();});
  $scope.$watch('submit_form.target_ports', function() {$scope.test();});
  $scope.$watch('submit_form.uplink', function() {$scope.test();});
  $scope.$watch('submit_form.downlink', function() {$scope.test();});
  

  $scope.test = function() {
    $scope.incomplete = true;
    if ($scope.submit_form.ssid !== "" && 
        $scope.submit_form.ap_ip !== "") {
      $scope.incomplete = false;
    }

    if ($scope.submit_form.target_ip == "" &&
        $scope.submit_form.target_ports == "") {
      $scope.incomplete = true;
    }
    else if ($scope.submit_form.target_ip !== "" &&
            $scope.submit_form.target_prefix == "") {
      $scope.incomplete = true;
    }
    else if ($scope.submit_form.uplink == "" &&
            $scope.submit_form.downlink == "") {
      $scope.incomplete = true;
    }

  };



}]);


