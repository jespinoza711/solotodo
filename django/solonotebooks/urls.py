from django.conf.urls.defaults import *
from django.conf import settings

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
    (r'^ad_visited/(?P<advertisement_id>\d+)/$', 'solonotebooks.cotizador.views.ad_visited'),    
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
    (r'^latest_notebooks/$', 'solonotebooks.cotizador.views.latest_notebooks'),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('solonotebooks.cotizador.views_manager',
    (r'^manager/$', 'news'),
    (r'^manager/news/$', 'news'),
    (r'^manager/comments/$', 'comments'),
    (r'^manager/new_entities/$', 'new_entities'),
    (r'^manager/delete/(?P<comment_id>\d+)$', 'delete_comment'),
    (r'^manager/hide_entity/(?P<store_has_product_entity_id>\d+)$', 'hide_entity'),
    (r'^manager/storehasproductentity/(?P<store_has_product_entity_id>\d+)/edit$', 'storehasproductentity_edit'),
    (r'^manager/validate_all$', 'validate_all'),
    (r'^manager/analyze_searches$', 'analyze_searches'), 
)

