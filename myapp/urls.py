from django.urls import re_path
from .import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	re_path(r'^admin_log$', views.admin_log, name='admin_log'),
    re_path(r'^admin_login$', views.admin_login, name='admin_login'),
    re_path(r'^admin_logout$', views.admin_logout, name='admin_logout'),
    re_path(r'^user_logout$', views.user_logout, name='user_logout'),
    re_path(r'^admin_settings$', views.admin_settings, name='admin_settings'),
    re_path(r'^admin_edit_picture$', views.admin_edit_picture, name='admin_edit_picture'),
    re_path(r'^admin_edit_profile$', views.admin_edit_profile, name='admin_edit_profile'),
    re_path(r'^admin_edit_password$', views.admin_edit_password, name='admin_edit_password'),
    re_path(r'^modelshow/(?P<id>\d+)$', views.modelshow, name='modelshow'),
    re_path(r'^admin_dashboard$', views.admin_dashboard, name='admin_dashboard'),
    re_path(r'^registration$', views.registration, name='registration'),
    re_path(r'^Signup_emailval$', views.Signup_emailval, name='Signup_emailval'),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^userhome$', views.userhome, name='userhome'),
    re_path(r'^search$', views.search, name='search'),
    re_path(r'^new_page/(?P<id>\d+)$', views.new_page, name='new_page'),
    re_path(r'^sub/(?P<id>\d+)$', views.sub, name='sub'),
    
    #category
    re_path(r'^category$', views.show_category, name="category"),
    re_path(r'^Sub_categories$', views.Sub_categories, name="Sub_categories"),
    re_path(r'^add_subcategory$', views.add_subcategory, name="add_subcategory"),
    re_path(r'^add_category$', views.add_category, name="add_category"),
    re_path(r'^cat_delete/(?P<cat_id>\d+)$', views.cat_delete, name="cat_delete"),
    re_path(r'^subcat_delete/(?P<id>\d+)$', views.subcat_delete, name="subcat_delete"),
    
    #models
    re_path(r'^admin_models$', views.admin_models, name='admin_models'),
    
    #add model
    re_path(r'^addmodel$', views.addmodel, name="addmodel"),
    re_path(r'^createmodel$', views.createmodel, name="createmodel"),
    
    #payment history
    re_path(r'^admin_payment_history$', views.admin_payment_history, name='admin_payment_history'),
    re_path(r'^payment_table$', views.payment_table, name='payment_table'),
    
    #registered users
    re_path(r'^registeredusers$', views.registeredusers, name='registeredusers'),
    re_path(r'^delete/(?P<reg_id>\d+)$', views.delete, name='delete'),
    
    #model edit
    re_path(r'^adminedit/(?P<id>\d+)$', views.adminedit,name="adminedit"),
    re_path(r'^admin_editmodel/(?P<id>\d+)$', views.admin_editmodel,name="admin_editmodel"),
    re_path(r'^modeledit/(?P<id>\d+)$', views.modeledit,name="modeledit"),

    #current models
    re_path(r'^admin_current_models$', views.admin_current_models, name='admin_current_models'),
    re_path(r'^model_delete/(?P<id>\d+)$', views.model_delete,name="model_delete"),
    re_path(r'^test_page$', views.test_page,name="test_page"),
    
    
   
	#Leave as empty string for base url
	# re_path(r'^store$', views.store, name="store"),
	re_path(r'^cart/$', views.cart, name="cart"),
	re_path(r'^checkout/$', views.checkout, name="checkout"),

	re_path(r'^update_item/$', views.updateItem, name="update_item"),
	re_path(r'^process_order/$', views.processOrder, name="process_order"),
	
	re_path(r'^login/$', views.login, name="login"),
	re_path(r'^logout/$', views.logout, name="logout"),
    re_path(r'^newcart/$',views.newcart,name='newcart'),
    re_path(r'^request/$',views.request,name='request'),
    re_path(r'^request_not_logedin/$',views.request_not_logedin,name='request_not_logedin'),
    re_path(r'^reqlist/$',views.reqlist,name='reqlist'),
    re_path(r'^savereq/$',views.savereq,name='savereq'),
    re_path(r'deletereq/(?P<id>\d+)$',views.deletereq,name='deletereq'),
    



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)