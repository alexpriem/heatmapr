from django.conf.urls import patterns, include, url
from webmap import views
import os

from django.contrib import admin
admin.autodiscover()


base_dir = os.path.dirname(os.path.dirname(__file__))+'/..'
base_url = 'heatmap/'
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/js'}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/img'}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/css'}),    
    url(r'^lib/(?P<path>.*)$', 'django.views.static.serve', {'document_root':base_dir+'/lib'}),
                       
    url(r'^$', views.top, name='index'),
    url(r'^dataset/(?P<dataset>.*)/', views.dataset),
    url(r'^heatmap/(?P<dataset>.*)/$', views.heatmap),
    url(r'^admin/', include(admin.site.urls)),
    
)
