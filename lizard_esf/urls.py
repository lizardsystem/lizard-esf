# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin

from lizard_ui.urls import debugmode_urlpatterns

from lizard_esf.views import EsfConfigurationHistoryView
from lizard_esf.views import EsfConfigurationArchiveView
from lizard_esf.views import EsfMainEditor

admin.autodiscover()

API_URL_NAME = 'lizard_esf_api_root'
NAME_PREFIX = 'lizard_esf_'

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('lizard_esf.api.urls')),
    url(r'^esf_overview/(?P<area_ident>.*)/$',
        'lizard_esf.views.esf_overview',
        name='esf_overview'
    ),
    (r'^history/$',
     EsfConfigurationHistoryView.as_view(),
     {},
     "lizard_esf.history"),
    (r'^archive/(?P<log_entry_id>\d+)/$',
     EsfConfigurationArchiveView.as_view(),
     {},
     "lizard_esf.archive"),
    (r'^main_esf_editor/$',
     EsfMainEditor.as_view(),
         {},
     "lizard_esf.main_esf_editor"),
    )
urlpatterns += debugmode_urlpatterns()
