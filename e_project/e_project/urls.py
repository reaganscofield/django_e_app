from django.contrib import admin
from django.urls import path, include
from e_app import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('e_app.urls'), name='e_app'),
    path('api/bought', views.BoughtView.as_view(), name='bought-view'),
    path('api/bought_create', views.BoughtCreate.as_view(), name='bought-create'),
    url(r'^api/bought_update/(?P<id>[0-9a-f-]+)/$', views.BoughtUpdate.as_view(), name='bought-update'),
    url(r'^api/bought_details/(?P<id>[0-9a-f-]+)/$', views.BoughtUpdate.as_view(), name='bought-details'),
    url(r'^api/bought_destroy/(?P<id>[0-9a-f-]+)/$', views.BoughtDestroy.as_view(), name='bought-destroy'),
    path('api/users', views.UsersView.as_view()),
    path('api/v1/auth/login', views.LoginView.as_view()),
    path('api/v1/auth/logout', views.LougoutView.as_view())
]
