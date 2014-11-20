from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/', 'articles.views.getMainPage'),
    url(r'^logout/', 'articles.views.userLogout'),
    url(r'^regist/', 'articles.views.userRegister'),
    url(r'^addarticle/', 'articles.views.addArticle'),
    url(r'^article/', 'articles.views.showArticle'),
    url(r'^userinfo/', 'articles.views.getUser'),
    url(r'^delcomment/', 'articles.views.delComment'),
    url(r'^delarticle/', 'articles.views.delArticle'),
    url(r'^support/', 'articles.views.showSupport'),
    url(r'^editarticle/', 'articles.views.editActicle'),
    url(r'^facetid/', 'articles.views.getFaceIdList'),
    url(r'^trustedapps', 'articles.views.getTrustedApps'),
    url(r'^bind', 'articles.views.bindUsers'),
    url(r'^authenticate', 'articles.views.getAuthenticated'),
    url(r'^admin/', include(admin.site.urls)),
)
