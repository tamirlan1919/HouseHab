from django.contrib import admin
from django.urls import path, include
from estatemaster import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/users/create/', views.CustomUserCreateView.as_view(), name='user-create'),


]
