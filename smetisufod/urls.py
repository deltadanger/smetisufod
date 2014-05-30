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
    url(r'^search$', 'mainsite.views.search', name='search-simple'),
    url(r'^developer.html$', 'mainsite.developers.developers', name='dev'),
    url(r'^get_item$', 'mainsite.views.get_item', name='get_item'),
    url(r'^flag_invalid$', 'mainsite.views.flag_invalid', name='flag_invalid'),
    
    url(r'^contact.html$', 'mainsite.contact.contact', name='contact'),
    
    
    url(r'^smetisufod.itemlookup.js$', 'mainsite.jquery_plugin.js', name='jquery_plugin'),
    url(r'^smetisufod.itemlookup.css$', 'mainsite.jquery_plugin.css', name='jquery_plugin_css'),
)
