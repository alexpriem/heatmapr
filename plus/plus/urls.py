from django.conf.urls import patterns, include, url
from webmap import view_data, view_histogram, view_heatmap, view_makemap, views
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

    url(r'^js-data/(?P<dataset>.*)/(?P<path>.*)$', view_heatmap.serve_heatmap_js),

    url(r'^$', views.top, name='index'),

    url(r'^set_filter/(?P<dataset>.*)/', view_data.set_filter),
    url(r'^set_recode/(?P<dataset>.*)/', view_data.set_recode),
    
    url(r'^heatmap/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/(?P<indexnr>.*)/$', view_heatmap.view_heatmap),
    url(r'^heatmap/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/$', view_heatmap.view_heatmap),
    url(r'^heatmap/(?P<dataset>.*)/$', view_heatmap.view_heatmaps),
    url(r'^data/(?P<dataset>.*)/$', view_data.view_data),
    url(r'^dataset/(?P<dataset>.*)/', view_data.dataset),
    url(r'^makemap/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/(?P<indexnr>.*)/$', view_makemap.make_heatmap),
    url(r'^makemap/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/$', view_makemap.make_heatmap),
    url(r'^makemap/(?P<dataset>.*)/$', view_makemap.make_heatmap),
    url(r'^histogram/(?P<dataset>.*)/(?P<variable>.*)/$', view_histogram.histogram),
    url(r'^admin/', include(admin.site.urls)),
    
)
