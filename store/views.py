from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order, ProductImage
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductImageSerializer, ProductSerializer,CreateOrderSerializer, CollectionSerializer,OrderSerializer ,CustomerSerializer, ReviewSerializer,UpdateCartItemSerializer, CartSerializer,AddcartItemSerializer, CartItemSerialiser, UpdateOrderSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from .filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser, IsAuthenticated
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter 
    search_fields = ['title']
    ordering_fields = ['unit_price', 'updated_at']
    #filterset_fields = ['collection_id']
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset


    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count()>0:
            return Response({'error':'This product cannot be deleted because it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ProductImageViewSet(ModelViewSet):

    serializer_class = ProductImageSerializer

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        return ProductImage.objects.filter(product_id= self.kwargs['product_pk'])
        
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count = Count('products'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count()>0:
            return Response({'error':'This product cannot be deleted because it is associated with OrderItem'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['patch', 'delete', 'get', 'post']
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddcartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerialiser
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['carts_pk']}
    
    def get_queryset(self):
        return CartItem.objects.filter(cart_id= self.kwargs['carts_pk']).select_related('product')
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CustomerSerializer(customer, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return[IsAdminUser()]
        return[IsAuthenticated()]
        
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer  # This uses your custom save()
        elif self.request.method == 'PUT':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        
        customer_id = Customer.objects.values_list('id', flat=True).get(user_id=user.id)
        return Order.objects.prefetch_related('items__product').filter(customer_id=customer_id)

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

