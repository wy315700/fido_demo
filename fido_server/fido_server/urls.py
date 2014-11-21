from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
import authServer.views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fido_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^bind/request', authServer.views.getBindRequest),
    url(r'^auth/request', authServer.views.getAuthRequest),
    url(r'^admin/', include(admin.site.urls)),
    
)
