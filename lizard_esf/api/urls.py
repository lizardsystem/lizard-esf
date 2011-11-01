# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
# from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from djangorestframework.views import InstanceModelView
from djangorestframework.views import ModelView
from djangorestframework.views import ListModelView
from djangorestframework.views import ListOrCreateModelView

from lizard_esf.api.resources import ConfigurationTypeResource
from lizard_esf.api.resources import ValueTypeResource
from lizard_esf.api.resources import ConfigurationResource
from lizard_esf.api.resources import AreaConfigurationResource

from lizard_esf.api.views import RootView
from lizard_esf.api.views import ConfigurationTypeRootView
from lizard_esf.api.views import ValueTypeRootView
from lizard_esf.api.views import ConfigurationRootView
from lizard_esf.api.views import AreaConfigurationRootView


admin.autodiscover()

NAME_PREFIX = 'lizard_esf_api_'

urlpatterns = patterns(
    '',
    url(r'^$',
        RootView.as_view(),
        name=NAME_PREFIX + 'root'),

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

    url(r'^configuration/$',
        ListOrCreateModelView.as_view(resource=ConfigurationResource),
        name=NAME_PREFIX + 'configuration_root'),
    url(r'^configuration/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=ConfigurationResource),
        name=NAME_PREFIX + 'configuration'),

    url(r'^area_configuration/$',
        ListOrCreateModelView.as_view(resource=AreaConfigurationResource),
        name=NAME_PREFIX + 'area_configuration_root'),
    url(r'^area_configuration/(?P<pk>[^/]+)/$',
        InstanceModelView.as_view(resource=AreaConfigurationResource),
        name=NAME_PREFIX + 'area_configuration'),
    )
