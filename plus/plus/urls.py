from django.conf.urls import patterns, include, url
from webmap import view_data, view_histogram, view_heatmap, view_makemap, views, view_labels
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
    url(r'^print/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/(?P<indexnr>.*)/$', view_heatmap.print_heatmap),
    url(r'^print/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/$', view_heatmap.print_heatmap),

    url(r'^heatmap/(?P<dataset>.*)/$', view_heatmap.view_heatmaps),

    url(r'^heatmap_subsel/(?P<dataset>.*)/$', view_heatmap.make_subsel),
    url(r'^heatmap_histogram/(?P<dataset>.*)/$', view_heatmap.make_histogram),


    url(r'^labels/(?P<dataset>.*)/(?P<variable>.*)/$', view_labels.view_var_key_labels),
    url(r'^labels/(?P<dataset>.*)/$', view_labels.view_dataset_var_labels),


    url(r'^set-config/(?P<dataset>.*)/$', view_data.set_config),
    url(r'^set-filter/(?P<dataset>.*)/$', view_data.set_filter),
    url(r'^set-recode/(?P<dataset>.*)/$', view_data.set_recode),
    url(r'^set-labels/(?P<dataset>.*)/$', view_labels.set_labels),


    url(r'^data-config/(?P<dataset>.*)/$', view_data.view_dataconfig),
    url(r'^data-filter/(?P<dataset>.*)/$', view_data.view_data_filter),
    url(r'^data-recode/(?P<dataset>.*)/$', view_data.view_data_recode),
    url(r'^data/(?P<dataset>.*)/$', view_data.view_data),
    url(r'^dataset/(?P<dataset>.*)/', view_data.dataset),
    url(r'^makemap/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/(?P<indexnr>.*)/$', view_makemap.make_heatmap),
    url(r'^makemap/(?P<dataset>.*)/(?P<x_var>.*)/(?P<y_var>.*)/$', view_makemap.make_heatmap),
    url(r'^makemap/(?P<dataset>.*)/$', view_makemap.make_heatmap),
    url(r'^editmap/(?P<dataset>.*)/(?P<filename>.*)/$', view_makemap.edit_heatmap),
    url(r'^histogram/(?P<dataset>.*)/(?P<variable>.*)/$', view_histogram.histogram),
    url(r'^admin/', include(admin.site.urls)),
    
)
