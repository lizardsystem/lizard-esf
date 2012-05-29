

{
    title: 'editor',
    xtype: 'esf_main_editor',
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
            url: '/esf/api/configuration/tree/',
            extraParams: {
                _accept: 'application/json',
                object_id: '{{ view.object_id }}',
                only_main_esf: true
            },
            reader: {
                type: 'json'
            },
            writer: {
                type: 'json',
                writeAllFields: false,
                root: 'data',
                successProperty: 'success',
                encode:true
            },
            afterRequest: function(request,success){
                if (request.method == 'POST') {
                    if (success) {
                        Ext.MessageBox.alert('Opslaan gelukt');
                    } else {
                        Ext.MessageBox.alert('Opslaan mislukt');
                    }
                }
            }
        },
        listeners: {
            write: function(store, record, operation){
                store.getUpdatedRecords().forEach(function(rec) {
                    if (rec.dirty === true) {
                        rec.commit();
                    }
                });
            }
        },
        rejectChanges : function(){

            Ext.each(this.removed, function(rec) {
                rec.join(this);
                this.data.add(rec);
                if(Ext.isDefined(this.snapshot)){
                    this.snapshot.add(rec);
                }
            }, this);
            this.removed = [];

            this.getUpdatedRecords().forEach(function(rec) {
                if (rec.dirty === true) {
                    rec.reject();
                }

                if (rec.phantom === true) {
                    rec.unjoin(this);
                    this.data.remove(rec);
                    if(Ext.isDefined(this.snapshot)){
                        this.snapshot.remove(rec);
                    }
                }
            },this);
            this.fireEvent('datachanged', this);
        }
    }

}
{% comment %}
{{ view.history.tree }}
xtype: 'esf_grid',
    editable:false,
  store: Ext.getStore('esf')
{% endcomment %}
