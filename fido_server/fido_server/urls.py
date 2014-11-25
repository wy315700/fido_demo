from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fido_server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^userpub/', 'authServer.views.getuserpub'),
    url(r'^policy/', 'authServer.views.getpolicy'),
    url(r'^meta/', 'authServer.views.getAuthenticatorMeta'),
    url(r'^logout/', 'authServer.views.userLogout'),
    url(r'^index/', 'authServer.views.getMainPage'),
    url(r'^others/', 'authServer.views.getAlgsAndScheme'),
    url(r'^admin/', include(admin.site.urls)),
)
