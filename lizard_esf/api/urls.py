# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

#from djangorestframework.views import InstanceModelView
#from djangorestframework.views import ListOrCreateModelView

#from lizard_esf.api.resources import AreaConfigurationResource

from lizard_esf.api.views import RootView

from lizard_esf.api.views import ConfigurationListView
from lizard_esf.api.views import ConfigurationDetailView
from lizard_esf.api.views import ConfigurationCreateView
from lizard_esf.api.views import ConfigurationTreeView

from lizard_esf.api.views import ValueTypeRootView
from lizard_esf.api.views import ValueTypeView

from lizard_esf.api.views import ConfigurationTypeRootView
from lizard_esf.api.views import ConfigurationTypeView

admin.autodiscover()

NAME_PREFIX = 'lizard_esf_api_'

urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),

    url(r'^configuration/$',
        ConfigurationListView.as_view(),
        name=NAME_PREFIX + 'configuration_root'),
    url(r'^configuration/create/$',
        ConfigurationCreateView.as_view(),
        name=NAME_PREFIX + 'configuration_create'),
    url(r'^configuration/tree/$',
        ConfigurationTreeView.as_view(),
        name=NAME_PREFIX + 'configuration_tree'),
    url(r'^configuration/(?P<pk>[^/]+)/$',
        ConfigurationDetailView.as_view(),
        name=NAME_PREFIX + 'configuration_detail'),

    url(r'^configuration_type/$',
        ConfigurationTypeRootView.as_view(),
        name=NAME_PREFIX + 'configuration_type_root'),
    url(r'^configuration_type/(?P<pk>[0-9]+)/$',
        ConfigurationTypeView.as_view(),
        name=NAME_PREFIX + 'configuration_type'),

    url(r'^value_type/$',
        ValueTypeRootView.as_view(),
        name=NAME_PREFIX + 'value_type_root'),
    url(r'^value_type/(?P<pk>[0-9]+)/$',
        ValueTypeView.as_view(),
        name=NAME_PREFIX + 'value_type'),

    #url(r'^area_configuration/$',
        #ListOrCreateModelView.as_view(resource=AreaConfigurationResource),
        #name=NAME_PREFIX + 'area_configuration_root'),
    #url(r'^area_configuration/(?P<pk>[^/]+)/$',
        #InstanceModelView.as_view(resource=AreaConfigurationResource),
        #name=NAME_PREFIX + 'area_configuration'),
    #)
