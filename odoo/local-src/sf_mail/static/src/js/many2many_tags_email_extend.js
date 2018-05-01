odoo.define('sf_mail.FieldMany2ManyTagsEmail', function (require) {
"use strict";

var core = require('web.core');
var many2many_tags_email = require('mail.many2manytags');

var FieldMany2ManyTagsEmail = core.form_widget_registry.get('many2many_tags_email');

FieldMany2ManyTagsEmail.include({

    get_render_data: function(ids){
        /**
         *  override to add 'email' to fields
         */
        this.dataset.cancel_read();
        var fields = this.fields.color ? ['display_name', 'email', 'name', 'color'] : ['display_name', 'email', 'name']; // TODO master: remove useless 'name'
        return this.dataset.read_ids(ids, fields);
    },
    render_value: function() {
       /**
        * override to format display_name with email
        */
        var self = this;
        var values = this.get("value");
        var handle_names = function(_data) {
            _.each(_data, function(el) {
                var email = el.email ? ' <'+el.email+'>' : '';
                el.display_name = el.display_name.trim() ? _.str.escapeHTML(el.display_name + email) : data.noDisplayContent;
            });
            self.render_tag(_data);
        };
        if (!values || values.length > 0) {
            return this.alive(this.get_render_data(values)).done(handle_names);
        } else {
            handle_names([]);
        }
    }
});

});
