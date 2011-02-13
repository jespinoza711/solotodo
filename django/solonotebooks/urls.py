from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^admin/', include(admin.site.urls)))

urlpatterns += patterns('solonotebooks.cotizador.views_notebooks',
    (r'^notebooks/processor_lines/(?P<processor_line_id>\d+)/$', 'processor_line_details'),
    (r'^notebooks/processor_lines/$', 'processor_line'),
    (r'^notebooks/video_card_lines/(?P<video_card_line_id>\d+)/$', 'video_card_line_details'),
    (r'^notebooks/video_card_lines/$', 'video_card_line'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_videocards',
    (r'^video_cards/gpu_details/(?P<gpu_id>\d+)/$', 'gpu_details'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_advertisement',
    (r'^advertisement/manage/$', 'manage'),    
    (r'^advertisement/get_advertisement_options/$', 'get_advertisement_options'),        
    (r'^advertisement/submit/$', 'submit'),
    (r'^advertisement/remove/$', 'remove'))

urlpatterns += patterns('solonotebooks.cotizador.views_account',
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
    (r'^account/enable_subscription_mail/(?P<subscription_id>\d+)$', 'enable_subscription_mail'),
    (r'^account/disable_subscription_mail/(?P<subscription_id>\d+)$', 'disable_subscription_mail'),    
    (r'^account/remove_subscription/(?P<subscription_id>\d+)/$', 'remove_subscription'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_manager',
    (r'^manager/$', 'news'),
    (r'^manager/news/$', 'news'),
    (r'^manager/comments/$', 'comments'),
    (r'^manager/new_entities/$', 'new_entities'),
    (r'^manager/delete/(?P<comment_id>\d+)$', 'delete_comment'),
    (r'^manager/validate/(?P<comment_id>\d+)$', 'validate_comment'),
    (r'^manager/hide_entity/(?P<store_has_product_entity_id>\d+)$', 'hide_entity'),
    (r'^manager/storehasproductentity/(?P<store_has_product_entity_id>\d+)/edit$', 'storehasproductentity_edit'),
    (r'^manager/validate_all$', 'validate_all'),
    (r'^manager/delete_all$', 'delete_all'),
    (r'^manager/analyze_searches$', 'analyze_searches'), 
)

urlpatterns += patterns('solonotebooks.cotizador.views_legacy',
    (r'^notebooks/(?P<notebook_id>\d+)/$', 'notebook_details'),
    (r'^processor_line_families/(?P<processor_line_family_id>\d+)/$', 'processor_line_family_details'),
    (r'^processor_line_families/$', 'all_processor_line_families'),
    (r'^video_card_line/(?P<video_card_line_id>\d+)/$', 'video_card_line_details'),
    (r'^video_card_line/$', 'video_card_line'),
    )
    
urlpatterns += patterns('solonotebooks.cotizador.views',
    (r'^$', 'index'),
    (r'^products/(?P<product_id>\d+)/$', 'product_details'),
    (r'^store_product/(?P<store_product_id>\d+)/$', 'store_product_redirect'),
    (r'^stores/$', 'store_index'),
    (r'^stores/(?P<store_id>\d+)/$', 'store_details'),
    (r'^all_products/$', 'all_products'),
    (r'^search/$', 'search'),
    (r'^ad_visited/(?P<advertisement_id>\d+)/$', 'ad_visited'),    
    (r'^search/$', 'search'),
    (r'^(?P<product_type_urlname>\w+)/catalog/$', 'product_type_catalog'),
    (r'^(?P<product_type_urlname>\w+)/$', 'product_type_index'),
)
