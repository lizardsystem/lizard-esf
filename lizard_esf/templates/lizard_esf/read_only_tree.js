{% load history_extras %}

{
    title: "{{view.area.name}} " +
         "({{view.history.datetime|format_date_string}})",
    xtype: 'esf_grid_history',
    autoScroll: true,
    height: 560,
    store: {
        xtype: 'tree',
        indexOf: Ext.emptyFn,
        fields: [
            {
                name: 'id',
                mapping: 'id',
                type: 'auto'
            }, {
                name: 'config_id',
                type: 'auto'
            }, {
                name: 'name',
                type: 'string'
            }, {
                name: 'source_name',
                type: 'auto'
            }, {
                name: 'manual_value',
                type: 'auto'
            }, {
                name: 'auto_value',
                type: 'auto'
            }, {
                name: 'auto_value_ts',
                type: 'auto'
            }, {
                name: 'manual',
                type: 'int'
            }, {
                name: 'is_manual',
                type: 'boolean'
            }, {
                name: 'type',
                type: 'string'
            }, {
                name: 'comment',
                type: 'string'
            }, {
                name: 'config_type',
                type: 'string'
            }, {
                name: 'last_edit_by',
                type: 'string'
            }, {
                name: 'last_edit_date',
                type: 'string'
            }, {
                name: 'iconCls',
                type: 'string'
            }
        ],
        proxy: {
            type: 'ajax',
            url: '/history/other_object/{{ view.history.log_entry_id }}/',
            extraParams: {
                _accept: 'application/json'
            },
            reader: {
                type: 'json'
            }
        }
    }

}
{% comment %}
{{ view.history.tree }}
xtype: 'esf_grid',
    editable:false,
  store: Ext.getStore('esf')
{% endcomment %}
