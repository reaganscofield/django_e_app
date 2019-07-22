from django.contrib import admin
from django.urls import path, include
from e_app import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('e_app.urls'), name='e_app'),

    url(r'^api/products_search/', views.ProductsSearch.as_view(), name="products-search"),
   
    path('api/bought_list', views.BoughtView.as_view(), name='bought-view'),
    path('api/bought_create', views.BoughtCreate.as_view(), name='bought-create'),
    url(r'^api/bought_update/(?P<id>[0-9a-f-]+)/$', views.BoughtUpdate.as_view(), name='bought-update'),
    url(r'^api/bought_details/(?P<id>[0-9a-f-]+)/$', views.BoughtDetails.as_view(), name='bought-details'),
    url(r'^api/bought_destroy/(?P<id>[0-9a-f-]+)/$', views.BoughtDestroy.as_view(), name='bought-destroy'),

    url(r'^api/users_details_or_update/(?P<id>[0-9a-f-]+)/$', views.UsersRetrieveUpdate.as_view(), name="users-retrieve-update"),
    path('api/users_list', views.UsersView.as_view(), name='users-view'),
    path('api/users_create/', views.UserCreate.as_view(), name="user-create"),
    url(r'^api/users_details_or_destroy/(?P<id>[0-9a-f-]+)/$', views.UsersRetrieveDestroy.as_view(), name="users-retrieve-destroy"),

    path('api/system/login', views.LoginView.as_view(), name="login-view"),
    path('api/system/logout', views.LougoutView.as_view(), name="logout-view"),
    path('api/system/is_logged_in', views.IfLoggedIn.as_view(), name="loogged-in"),


    #url(r'^api/messages/(?P<sender>[0-9a-f-]+)/(?P<receiver>[0-9a-f-]+)/', views.message_list, name='message-detail'), 
    #path('api/messages/', views.message_list, name='message-list'), 
    url(r'^api/users_message/(?P<id>[0-9a-f-]+)/$', views.user_list, name='user-detail'), 
    path('api/users_message/', views.user_list, name='user-list'),
   
]
