odoo.define('employees_hierarchy_department.button_hierarchy', function (require) {
    "use strict";
    var core = require('web.core');
    var config = require('web.config');
    var data = require('web.data');
    var DataExport = require('web.DataExport');
    var Pager = require('web.Pager');
    var pyeval = require('web.pyeval');
    var session = require('web.session');
    var Sidebar = require('web.Sidebar');
    var utils = require('web.utils');
    var View = require('web.View');
    var Bus = require('web.Bus');
    var Widget = require('web.Widget');
    var view_manager = require('web.ViewManager');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var form_view = require('web.FormView');
    var _t = core._t;
    var _lt = core._lt;

    var MyView = View.extend({
        icon: 'fa-sitemap',
        display_name: _lt("Hierarchy Chart"),

        do_show: function () {
            this.do_push_state({});
            return this._super();
        },
        reload_content: function () {
            this.do_push_state({
                min: this.current_min,
                limit: this._limit
            });
        },
        render_buttons: function ($node) {
            var $buttons = $('<div/>');
            $buttons.append(
                QWeb.render("MyView.buttons", {'widget': this})
            );
            $node.append($buttons);
        },
        on_create: function () {
            this.dataset.index = null;
            this.do_show();
        },
        render_sidebar: function ($node) {
            var sidebar = new Sidebar(this, {});
            sidebar.appendTo($node);
        },
        render_pager: function($node, options) {
            var self = this;
            this.pager = new Pager(this, this.dataset.size(), 1, this.limit, options);
            this.pager.appendTo($node);
            this.pager.on('pager_changed', this, function (state) {
                var limit_changed = (self.limit !== state.limit);
                self.limit = state.limit;
                self.load_records(state.current_min - 1)
                    .then(function (data) {
                        self.data = data;

                        // Reset the scroll position to the top on page changed only
                        if (!limit_changed) {
                            self.scrollTop = 0;
                            self.trigger_up('scrollTo', {offset: 0});
                        }
                    })
                    .done(this.proxy('render'));
            });
            this.update_pager();
        },

        update_pager: function() {
            if (this.pager) {
                if (this.grouped) {
                    this.pager.do_hide();
                } else {
                    this.pager.update_state({size: this.dataset.size(), current_min: 1});
                }
            }
        },
        render_switch_buttons: function () {
            var self = this;
            // Partition the views according to their multi-/mono-record status
            var views = _.partition(this.view_order, function (view) {
                return view.multi_record === true;
            });
            var multi_record_views = views[0];
            var mono_record_views = views[1];
            var _render_switch_buttons = function (views) {
                if (views.length > 1) {
                    var $switch_buttons = $(QWeb.render('ViewManager.switch-buttons', {views: views}));
                    // Create bootstrap tooltips
                    _.each(views, function (view) {
                        $switch_buttons.filter('.o_cp_switch_' + view.type).tooltip();
                    });
                    // Add onclick event listener
                    $switch_buttons.filter('button').click(_.debounce(function (event) {
                        var view_type = $(event.target).data('view-type');
                        self.switch_mode(view_type);
                    }, 200, true));
                    return $switch_buttons;
                }
            };
            // Render switch buttons but do not append them to the DOM as this will
            // be done later, simultaneously to all other ControlPanel elements
            this.switch_buttons = {};
            this.switch_buttons.$multi = _render_switch_buttons(multi_record_views);
            this.switch_buttons.$mono = _render_switch_buttons(mono_record_views);
        },

    });
    core.view_registry.add('myview', MyView);
});
