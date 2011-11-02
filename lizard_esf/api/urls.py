# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from djangorestframework.views import InstanceModelView
from djangorestframework.views import ListOrCreateModelView

from lizard_esf.api.resources import ConfigurationTypeResource
from lizard_esf.api.resources import ValueTypeResource
from lizard_esf.api.resources import AreaConfigurationResource

from lizard_esf.api.views import RootView
from lizard_esf.api.views import ConfigurationListView
from lizard_esf.api.views import ConfigurationDetailView
from lizard_esf.api.views import ConfigurationCreateView
from lizard_esf.api.views import ConfigurationTreeView


admin.autodiscover()

NAME_PREFIX = 'lizard_esf_api_'

urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),

    url(r'^configuration/$',
        ConfigurationListView.as_view(),
        name=NAME_PREFIX + 'configuration_list'),
    url(r'^configuration/create/$',
        ConfigurationCreateView.as_view(),
        name=NAME_PREFIX + 'configuration_create'),
    url(r'^configuration/(?P<pk>[^/]+)/$',
        ConfigurationDetailView.as_view(),
        name=NAME_PREFIX + 'configuration_detail'),
    url(r'^tree/$',
        ConfigurationTreeView.as_view(),
        name=NAME_PREFIX + 'configuration_tree'),

    url(r'^configuration_type/$',
        ListOrCreateModelView.as_view(resource=ConfigurationTypeResource),
        name=NAME_PREFIX + 'configuration_type_root'),
    url(r'^configuration_type/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=ConfigurationTypeResource),
        name=NAME_PREFIX + 'configuration_type'),

    url(r'^value_type/$',
        ListOrCreateModelView.as_view(resource=ValueTypeResource),
        name=NAME_PREFIX + 'value_type_root'),
    url(r'^value_type/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=ValueTypeResource),
        name=NAME_PREFIX + 'value_type'),


    url(r'^area_configuration/$',
        ListOrCreateModelView.as_view(resource=AreaConfigurationResource),
        name=NAME_PREFIX + 'area_configuration_root'),
    url(r'^area_configuration/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=AreaConfigurationResource),
        name=NAME_PREFIX + 'area_configuration'),
    )
