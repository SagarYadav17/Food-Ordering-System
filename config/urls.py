from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register("tags", core_views.TagsViewset, basename="core-tags")
router.register("categories", core_views.CategoryViewset, basename="core-category")
router.register("menu-items", core_views.MenuItemViewset, basename="core-menu-items")
router.register("ordered-items", core_views.OrderedItemViewset, basename="core-ordered-items")
router.register("orders", core_views.OrderViewset, basename="core-orders")
router.register("payments", core_views.PaymentViewset, basename="core-payments")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("login/", core_views.AuthTokenPairView.as_view(), name="auth-token"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("logout/", core_views.LogoutView.as_view(), name="auth-logout"),
]
