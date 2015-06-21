from django.conf.urls import patterns, include, url
from webmap import views

from django.contrib import admin
admin.autodiscover()

base_dir='..'
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^heatmap/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/js'}),
    url(r'^heatmap/img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/img'}),
    url(r'^heatmap/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/css'}),    
    url(r'^heatmap/lib/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/lib'}),
                       
    url(r'^$', views.top, name='index'),
    url(r'^heatmap/$', views.heatmap, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    
)
