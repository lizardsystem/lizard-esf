{% load get_portal_template %}

{
    itemId: 'esf-1',
    title: 'ESF details',
    xtype: 'portalpanel',
    breadcrumbs: [
        {
            name: 'watersysteemkaart',
            link: 'homepage'
        },
        {
            name: 'ESF details'
        }
    ],
	items: [{
		width:360,
		items: [{
            flex:2,
            title: "Opbouw ESF'en",
            xtype: 'esf_grid',
        {% if user.is_authenticated %}
            editable:true,
            tools: [{
                type: 'search',
                handler: function (e, target, panelHeader, tool) {
                    Ext.create('Ext.window.Window', {
                        title: 'Geschiedenis van ESF-configuratie',
                        width: 800,
                        height: 600,
                        modal: true,
                        constrainHeader: true,
                        loader:{
                            loadMask: true,
                            autoLoad: true,
                            url: '/esf/history/',
                            baseParams: {
                               object_id: Lizard.CM.getContext().object.id
                            },
                            ajaxOptions: {
                                method: 'GET'
                            },
                            renderer: 'html'
                        }
                    }).show();
                }
            }],
        {% else %}
            editable:false,
        {% endif %}
            closable: false

        }]
    },{
        flex:1,
        items: {
            title: 'Grafieken',
            flex: 1,
            xtype: 'multigraph',
            open_map: function(workspace_slug, title) {
                Ext.create('Ext.window.Window', {
                    modal: true,
                    title: title,
                    width: 600,
                    height: 600,
		    constrainHeader: true,
                    layout: {
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items: [{
                        flex:1,
                        title: null,
                        xtype: "mapportlet",
                        initZoomOnRender: false,
                        plugins:[],
                        extent: new OpenLayers.Bounds(
                            Lizard.CM.getContext().init_zoom[0],
                            Lizard.CM.getContext().init_zoom[1],
                            Lizard.CM.getContext().init_zoom[2],
                            Lizard.CM.getContext().init_zoom[3]
                        ),
                        autoLoadWorkspaceStore: {
                            object_slug: workspace_slug
                        },
                        init_workspace: false,
                        workspaceStore: Lizard.store.WorkspaceStore.get_or_create('popup_' + workspace_slug),
                        listeners: {
                            afterRender: function() {
                                var me = this;
                                debugger
                                //me.callParent(arguments)
                                me.setLoading(true);
                                if (!this.init_workspace && this.autoLoadWorkspaceStore) {
                                    this.workspaceStore.load({
                                        params: me.autoLoadWorkspaceStore
                                    });
                                    this.init_workspace = true
                                }
                                Ext.Ajax.request({
                                     url: '/area/api/area_special/'+ Lizard.CM.getContext().object.id +'/',
                                     method: 'GET',
                                     params: {
                                         _accept: 'application/json'
                                     },
                                     success: function(xhr) {
                                         var area_data = Ext.JSON.decode(xhr.responseText).area;
                                         me.default_zoom = area_data.extent
                                         me.map.zoomToExtent(new OpenLayers.Bounds.fromArray(area_data.extent));
                                         return me.setLoading(false);
                                     },
                                     failure: function() {
                                         Ext.Msg.alert("portal creation failed", "Server communication failure");
                                         return me.setLoading(false);
                                     }
                                });
                            }
                        }
                    }]
               }).show()
            },
            graph_service_url: '/graph/',
            context_manager: Lizard.CM,
            bbar: [{
                text: 'PO4 op kaart',
                handler: function (button) {
                    button.up('panel').open_map('po4_map', 'PO4 op de kaart ')
                }
            },{
                text: 'P op kaart',
                handler: function (button) {
                    button.up('panel').open_map('P_map', 'P op de kaart ')
                }
            },{
            text: 'AqMad op kaart',
            handler: function (button) {
                button.up('panel').open_map('aqmad_map', 'AqMad op de kaart ')
            }
        }],
            graphs: {% get_portal_template graphs-esf %}
        }
	}]
}
