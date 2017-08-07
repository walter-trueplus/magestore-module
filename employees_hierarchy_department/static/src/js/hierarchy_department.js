var run_call_back ;
odoo.define('hierarchy_department', function (require) {
    "use strict";
    var self = this;
    var Model = require('web.Model');
    var chart= new Model('chart_config');
    run_call_back = function (fun){
        chart.call("search_department").then(function(result){
           fun(result);
        });
    }
});
run_call_back(function(result){
      chart_config = result;
});
