from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from account import views
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.routers import DefaultRouter

routers=DefaultRouter()
routers.register(r'account',views.UserDataViewSet )

urlpatterns = [
    path('signup/', views.SignupView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('api/', include(routers.urls)),
    path('api-token-auth/', obtain_auth_token)
    
]
