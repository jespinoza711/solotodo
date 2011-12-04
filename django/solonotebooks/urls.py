from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

handler500 = 'solonotebooks.cotizador.views.index'
handler404 = 'solonotebooks.cotizador.views.index'

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

urlpatterns += patterns('solonotebooks.cotizador.views_cellphones',
    (r'^cellphones/plans/(?P<plan_id>\d+)/$', 'plan_details'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_account',
    (r'^account/facebook_login/$', 'facebook_login'),
    (r'^account/facebook_fusion/$', 'facebook_fusion'),
    (r'^account/facebook_ajax_login/$', 'facebook_ajax_login'),
    (r'^account/login/$', 'login'),
    (r'^account/logout/$', 'logout'),
    (r'^account/validate_email/$', 'validate_email'),
    (r'^account/fuse_facebook_account/$', 'fuse_facebook_account'),
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

urlpatterns += patterns('solonotebooks.cotizador.views_store',
    (r'^store/$', 'index'),
    (r'^store/registry/$', 'registry'),
    (r'^store/entities/(?P<shpe_id>\d+)/$', 'entity_details'),
    (r'^store/entities/(?P<shpe_id>\d+)/refresh_price/$', 'entity_refresh_price'),
    (r'^store/advertisement/$', 'advertisement'),
    (r'^store/advertisement/reserve_slots/$', 'reserve_slots'),
    (r'^store/advertisement/free_slots/$', 'free_slots'),
    (r'^store/statistics/$', 'statistics'),
    (r'^store/update_prices/$', 'update_prices'),
    (r'^store/competition_report/$', 'competition_report'),
    (r'^store/competition_report/excel$', 'competition_report_excel'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_manager',
    (r'^manager/$', 'news'),
    (r'^manager/news/$', 'news'),
    (r'^manager/analyze_searches$', 'analyze_searches'),
    (r'^manager/statistics$', 'statistics'),  
    (r'^manager/stores/$', 'stores'),
    (r'^manager/stores/(?P<store_id>\d+)$', 'store_details'),
    (r'^manager/stores/(?P<store_id>\d+)/advertisement/$', 'store_advertisement'),
    (r'^manager/stores/(?P<store_id>\d+)/statistics/$', 'store_statistics'),
    (r'^manager/staff/$', 'staff'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_staff',
    (r'^staff/(?P<staff_id>\d+)/new_entities$', 'new_entities'),
    (r'^staff/(?P<staff_id>\d+)/storehasproductentity/(?P<store_has_product_entity_id>\d+)$', 'storehasproductentity_edit'),
    (r'^staff/(?P<staff_id>\d+)/storehasproductentity/(?P<store_has_product_entity_id>\d+)/hide$', 'storehasproductentity_hide'),
    (r'^staff/(?P<staff_id>\d+)/storehasproductentity/(?P<store_has_product_entity_id>\d+)/show$', 'storehasproductentity_show'),
    (r'^staff/(?P<staff_id>\d+)/storehasproductentity/(?P<store_has_product_entity_id>\d+)/refresh_price$', 'storehasproductentity_refresh_price'),
    (r'^staff/(?P<staff_id>\d+)/polymorphic_admin_request/(?P<product_id>\d+)$', 'polymorphic_admin_request'),
    (r'^staff/(?P<staff_id>\d+)/clone_product/(?P<product_id>\d+)$', 'clone_product'),
    (r'^staff/(?P<staff_id>\d+)/storehasproductentity/(?P<store_has_product_entity_id>\d+)/change_ptype$', 'storehasproductentity_change_ptype'),
    (r'^staff/(?P<staff_id>\d+)/statistics$', 'statistics'),  
    (r'^staff/(?P<staff_id>\d+)/registry$', 'registry'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_legacy',
    (r'^notebooks/(?P<notebook_id>\d+)/$', 'notebook_details'),
    (r'^processor_line_families/(?P<processor_line_family_id>\d+)/$', 'processor_line_family_details'),
    (r'^processor_line_families/$', 'all_processor_line_families'),
    (r'^video_card_line/(?P<video_card_line_id>\d+)/$', 'video_card_line_details'),
    (r'^video_card_line/$', 'video_card_line'),
    (r'^store_notebook/(?P<store_notebook_id>\d+)/$', 'store_notebook_redirect'),
    )
 
urlpatterns += patterns('solonotebooks.cotizador.views_services',
    (r'^products/(?P<product_id>\d+)/details/$', 'product_details'),
)

urlpatterns += patterns('solonotebooks.cotizador.views_chw',
    (r'^mini/(?P<product_id>\d+)/$', 'inline_forum_post'),
)
   
urlpatterns += patterns('solonotebooks.cotizador.views',
    (r'^$', 'index'),
    (r'^products/(?P<product_id>\d+)/$', 'product_details_legacy'),
    (r'^products/(?P<product_url>\S+)/$', 'product_details'),
    (r'^store_product/(?P<store_product_id>\d+)/$', 'store_product_redirect'),
    (r'^sponsored_product/(?P<shp_id>\d+)/$', 'sponsored_product_redirect'),
    (r'^all_products/$', 'all_products'),
    (r'^search/$', 'search'),
    (r'^ad_visited/(?P<advertisement_id>\d+)/$', 'ad_visited'),    
    (r'^search/$', 'search'),
    (r'^(?P<product_type_urlname>\w+)/catalog/$', 'product_type_catalog'),
    (r'^(?P<product_type_urlname>\w+)/$', 'product_type_index'),
)
