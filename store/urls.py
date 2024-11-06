from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested.routers import  NestedDefaultRouter

# route = SimpleRouter()
route = DefaultRouter()
route.register("collections", views.CollectionViewSet, basename="collections")
route.register("products", views.ProductViewSet, basename="products")
product_router = NestedDefaultRouter(route, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="products-review")

urlpatterns = route.urls + product_router.urls

# urlpatterns = [
#     path('', include(route.urls)),
#     path('', include(product_router.urls)),
#     path('collections/', views.CollectionListApiView.as_view(), name='collections'),
#     path('collection/<int:pk>/', views.CollectionDetailAPIView.as_view(), name='collection-detail'),
#     path('collection/<int:pk>/', views.CollectionDetailsAPIView.as_view(), name='collection'),
# ]
