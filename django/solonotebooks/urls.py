from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^solonotebooks/', include('solonotebooks.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'solonotebooks.cotizador.views.browse'),
    (r'^notebooks/(?P<notebook_id>\d+)/$', 'solonotebooks.cotizador.views.notebook_details'),
    (r'^processor_line_families/(?P<processor_line_family_id>\d+)/$', 'solonotebooks.cotizador.views.processor_line_family_details'),
    (r'^processor_line_families/$', 'solonotebooks.cotizador.views.all_processor_line_families'),    
    (r'^video_card_line/(?P<video_card_line_id>\d+)/$', 'solonotebooks.cotizador.views.video_card_line_details'),
    (r'^video_card_line/$', 'solonotebooks.cotizador.views.all_video_card_lines'),    
    (r'^store_notebook/(?P<store_notebook_id>\d+)/$', 'solonotebooks.cotizador.views.store_notebook_redirect'),
    (r'^stores/$', 'solonotebooks.cotizador.views.store_index'),
    (r'^stores/(?P<store_id>\d+)/$', 'solonotebooks.cotizador.views.store_data'),
    (r'^allnotebooks/$', 'solonotebooks.cotizador.views.all_notebooks'),
    (r'^search/$', 'solonotebooks.cotizador.views.search'),
    (r'^manager/$', 'solonotebooks.cotizador.views.news'),
    (r'^manager/login/$', 'solonotebooks.cotizador.views.login_page'),
    (r'^manager/news/$', 'solonotebooks.cotizador.views.news'),
    (r'^manager/comments/$', 'solonotebooks.cotizador.views.comments'),
    (r'^manager/new_notebooks/$', 'solonotebooks.cotizador.views.new_notebooks'),
    (r'^manager/delete/(?P<comment_id>\d+)$', 'solonotebooks.cotizador.views.delete_comment'),
    (r'^manager/hide_notebook/(?P<store_has_notebook_id>\d+)$', 'solonotebooks.cotizador.views.hide_notebook'),
    (r'^manager/validate_all$', 'solonotebooks.cotizador.views.validate_all'),
    (r'^admin/', include(admin.site.urls)),

)
