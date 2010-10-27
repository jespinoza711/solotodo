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
    (r'^$', 'solonotebooks.cotizador.views.index'),
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
    (r'^ad_visited/(?P<advertisement_id>\d+)/$', 'solonotebooks.cotizador.views.ad_visited'),    
    (r'^manager/$', 'solonotebooks.cotizador.views.news'),
    (r'^manager/news/$', 'solonotebooks.cotizador.views.news'),
    (r'^manager/comments/$', 'solonotebooks.cotizador.views.comments'),
    (r'^manager/new_notebooks/$', 'solonotebooks.cotizador.views.new_notebooks'),
    (r'^manager/delete/(?P<comment_id>\d+)$', 'solonotebooks.cotizador.views.delete_comment'),
    (r'^manager/hide_notebook/(?P<store_has_notebook_id>\d+)$', 'solonotebooks.cotizador.views.hide_notebook'),
    (r'^manager/validate_all$', 'solonotebooks.cotizador.views.validate_all'),
    (r'^manager/analyze_searches$', 'solonotebooks.cotizador.views.analyze_searches'),
    (r'^account/login/$', 'solonotebooks.cotizador.views.login'), 
    (r'^account/ajax_login/$', 'solonotebooks.cotizador.views.ajax_login'),     
    (r'^account/logout/$', 'solonotebooks.cotizador.views.logout'),
    (r'^account/signup/$', 'solonotebooks.cotizador.views.signup'),
    (r'^account/validate_email/$', 'solonotebooks.cotizador.views.validate_email'),
    (r'^account/request_password_regeneration/$', 'solonotebooks.cotizador.views.request_password_regeneration'),
    (r'^account/regenerate_password/$', 'solonotebooks.cotizador.views.regenerate_password'),    
    (r'^account/$', 'solonotebooks.cotizador.views.subscriptions'),
    (r'^account/subscriptions/$', 'solonotebooks.cotizador.views.subscriptions'),
    (r'^account/change_email/$', 'solonotebooks.cotizador.views.change_email'),
    (r'^account/change_password/$', 'solonotebooks.cotizador.views.change_password'),
    (r'^account/send_confirmation_mail/$', 'solonotebooks.cotizador.views.send_confirmation_mail'),    
    (r'^account/add_subscription/$', 'solonotebooks.cotizador.views.add_subscription'),
    (r'^account/enable_subscription_mail/(?P<subscription_id>\d+)/$', 'solonotebooks.cotizador.views.enable_subscription_mail'),
    (r'^account/disable_subscription_mail/(?P<subscription_id>\d+)/$', 'solonotebooks.cotizador.views.disable_subscription_mail'),    
    (r'^account/remove_subscription/(?P<subscription_id>\d+)/$', 'solonotebooks.cotizador.views.remove_subscription'),
    (r'^advertisement/manage/$', 'solonotebooks.cotizador.views_advertisement.manage'),    
    (r'^advertisement/get_advertisement_options/$', 'solonotebooks.cotizador.views_advertisement.get_advertisement_options'),        
    (r'^advertisement/submit/$', 'solonotebooks.cotizador.views_advertisement.submit'),
    (r'^advertisement/remove/$', 'solonotebooks.cotizador.views_advertisement.remove'),    
    (r'^admin/', include(admin.site.urls)),
)
