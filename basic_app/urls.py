from django.urls import path

from . import views

# For Template URLs
app_name = 'basic_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),

    path('user_login/', views.user_login, name='user-login')
]
