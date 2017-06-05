odoo.define('custom_web_logo.change_title', function (require) {
"use strict";

    var webAbstractClient=require('web.AbstractWebClient');

    var ProductScreenWidget=webAbstractClient.include({

        _title_changed: function() {
            var parts = _.sortBy(_.keys(this.get("title_part")), function(x) { return x; });
            var tmp = "";
            _.each(parts, function(part) {
                var str = this.get("title_part")[part];
                if (str) {
                    tmp = tmp ? tmp + " - " + str : str;
                }
            }, this);
            this._get_custom_title(tmp);
        },

        _get_custom_title: function(web_title){
            self=this;
            var Model = require('web.DataModel');
            var model=new Model('base.config.settings')
            model.call('get_custom_title',[]).then(function(result){
            var index = web_title.indexOf("Odoo");
            if (index>-1){
            var custom_title=web_title.replace("Odoo",result);
            document.title=custom_title;

            }


        });

        },


        })

});
