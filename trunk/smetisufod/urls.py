from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smetisufod.views.home', name='home'),
    # url(r'^smetisufod/', include('smetisufod.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'mainsite.views.search', name='home'),
    url(r'^search.html$', 'mainsite.views.search', name='search'),
    url(r'^developper.html$', 'mainsite.views.devs', name='dev'),
    url(r'^contact.html$', 'mainsite.views.contact', name='contact'),
)
