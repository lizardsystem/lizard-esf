{% load history_extras %}

{
  title: "{{view.area.name}} " + 
         "({{view.history.datetime|format_date_string}})",
  xtype: 'panel',
  flex: 1,
  items: [
    {
      title: 'Tree here please.',
      xtype: 'esf_grid',
      store: Ext.data.StoreManager.lookup('esf')
    }
  ]
}
{% comment %}
  xtype: 'esf_grid',
    editable:false,
  store: Ext.getStore('esf')
{% endcomment %}
