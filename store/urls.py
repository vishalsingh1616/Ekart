from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers # type: ignore


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename = 'products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='carts')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-review')
products_router.register('images', views.ProductImageViewSet, basename = 'product-image')


carts_router = routers.NestedDefaultRouter(router, 'carts', lookup = 'carts')
carts_router.register('items', views.CartItemViewSet, basename = 'cart-items')



urlpatterns = router.urls + products_router.urls + carts_router.urls
#     path('products/',views.ProductList.as_view()),
#     path('products/<int:pk>/', views.product_detail),
#     path('collections/', views.collection_list),
#     path('collections/<int:pk>/', views.collection_detail)
 
