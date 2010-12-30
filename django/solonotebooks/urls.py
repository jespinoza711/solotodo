from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'solonotebooks.cotizador.views.index'),
    (r'^catalog/$', 'solonotebooks.cotizador.views.catalog'),
    (r'^notebooks/(?P<notebook_id>\d+)/$', 'solonotebooks.cotizador.views.notebook_details'),
    (r'^processor_line_families/(?P<processor_line_family_id>\d+)/$', 'solonotebooks.cotizador.views.redirect_processor_line_family_details'),
    (r'^processor_line_families/$', 'solonotebooks.cotizador.views.redirect_all_processor_line_families'),
    (r'^processor_line/(?P<processor_line_id>\d+)/$', 'solonotebooks.cotizador.views.processor_line_details'),
    (r'^processor_line/$', 'solonotebooks.cotizador.views.processor_line'),
    (r'^video_card_line/(?P<video_card_line_id>\d+)/$', 'solonotebooks.cotizador.views.video_card_line_details'),
    (r'^video_card_line/$', 'solonotebooks.cotizador.views.video_card_line'),
    (r'^store_notebook/(?P<store_notebook_id>\d+)/$', 'solonotebooks.cotizador.views.store_notebook_redirect'),
    (r'^stores/$', 'solonotebooks.cotizador.views.store_index'),
    (r'^stores/(?P<store_id>\d+)/$', 'solonotebooks.cotizador.views.store_details'),
    (r'^allnotebooks/$', 'solonotebooks.cotizador.views.all_notebooks'),
    (r'^search/$', 'solonotebooks.cotizador.views.search'),
    (r'^ad_visited/(?P<advertisement_id>\d+)/$', 'solonotebooks.cotizador.views.ad_visited'),    
    (r'^advertisement/manage/$', 'solonotebooks.cotizador.views_advertisement.manage'),    
    (r'^advertisement/get_advertisement_options/$', 'solonotebooks.cotizador.views_advertisement.get_advertisement_options'),        
    (r'^advertisement/submit/$', 'solonotebooks.cotizador.views_advertisement.submit'),
    (r'^advertisement/remove/$', 'solonotebooks.cotizador.views_advertisement.remove'),    
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('cotizador.views_account',
    (r'^account/login/$', 'login'),
    (r'^account/logout/$', 'logout'),
    (r'^account/validate_email/$', 'validate_email'),
    (r'^account/ajax_login/$', 'ajax_login'),     
    (r'^account/signup/$', 'signup'),
    (r'^account/request_password_regeneration/$', 'request_password_regeneration'),
    (r'^account/regenerate_password/$', 'regenerate_password'),
    (r'^account/subscriptions/$', 'subscriptions'),
    (r'^account/$', 'subscriptions'),
    (r'^account/change_email/$', 'change_email'),
    (r'^account/change_password/$', 'change_password'),
    (r'^account/send_confirmation_mail/$', 'send_confirmation_mail'),    
    (r'^account/add_subscription/$', 'add_subscription'),
    (r'^account/enable_subscription_mail/$', 'enable_subscription_mail'),
    (r'^account/disable_subscription_mail/$', 'disable_subscription_mail'),    
    (r'^account/remove_subscription/(?P<subscription_id>\d+)/$', 'remove_subscription'),
)

urlpatterns += patterns('cotizador.views_manager',
    (r'^manager/$', 'news'),
    (r'^manager/news/$', 'news'),
    (r'^manager/comments/$', 'comments'),
    (r'^manager/new_notebooks/$', 'new_notebooks'),
    (r'^manager/delete/(?P<comment_id>\d+)$', 'delete_comment'),
    (r'^manager/hide_notebook/(?P<store_has_notebook_id>\d+)$', 'hide_notebook'),
    (r'^manager/validate_all$', 'validate_all'),
    (r'^manager/analyze_searches$', 'analyze_searches'), 
)
