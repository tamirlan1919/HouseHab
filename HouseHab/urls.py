from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from estatemaster import views


router = DefaultRouter()
router.register(r'promotion-configs', views.PromotionConfigViewSet)
router.register(r'builders', views.BuilderViewSet)
router.register(r'promotions', views.PromotionViewSet)
router.register(r'sale-residential', views.SaleResidentialViewSet)  # Добавьте этот маршрут
router.register(r'rent-long-advertisements', views.RentLongAdvertisementViewSet)
router.register(r'rent-day-advertisements', views.RentDayAdvertisementViewSet)
router.register(r'sale-commercial-advertisements', views.SaleCommercialAdvertisementViewSet)
router.register(r'rent-commercial-advertisements', views.RentCommercialAdvertisementViewSet)
router.register(r'location', views.LocationViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('auth/users/create/', views.CustomUserCreateView.as_view(), name='user-create'),
    path('auth/check_email/',views.CheckEmail.as_view(), name = 'check_email'),
    path('api/', include(router.urls)),  # Include the router's URLs


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)