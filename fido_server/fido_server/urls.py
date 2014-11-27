from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
import authServer.views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fido_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^userpub/', 'authServer.views.getuserpub'),
    url(r'^validated/', 'authServer.views.validated'),
    url(r'^policy/', 'authServer.views.getpolicy'),
    url(r'^meta/', 'authServer.views.getAuthenticatorMeta'),
    url(r'^logout/', 'authServer.views.userLogout'),
    url(r'^index/', 'authServer.views.getMainPage'),
    url(r'^others/', 'authServer.views.getAlgsAndScheme'),
    url(r'^bind/request', authServer.views.getBindRequest),
    url(r'^auth/request', authServer.views.getAuthRequest),
    url(r'^bind/response', authServer.views.postBindResponse),
    url(r'^auth/response', authServer.views.postAuthResponse),
    url(r'^admin/', include(admin.site.urls)),
    
)
