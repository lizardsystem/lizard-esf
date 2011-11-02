# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
# from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_ui.urls import debugmode_urlpatterns

admin.autodiscover()

API_URL_NAME = 'lizard_esf_api_root'
NAME_PREFIX = 'lizard_esf_'

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('lizard_esf.api.urls')),
    # url(r'^something/',
    #     direct.import.views.some_method,
    #     name="name_it"),
    )
urlpatterns += debugmode_urlpatterns()
