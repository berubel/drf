from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

#from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer
from api.permissions import isStaffEditorPermission
from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin

# Create your views here.

class ProductListCreateAPIView(
    StaffEditorPermissionMixin,
    UserQuerySetMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    user_field = 'user'
    # allow_staff_view = False

    def perform_create(self, request, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(user=request.user, content=content)

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=request.user)
         
       


class ProductDetailAPIView(
    StaffEditorPermissionMixin,
    UserQuerySetMixin,
    generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser, isStaffEditorPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'

class ProductUpdateAPIView(
    StaffEditorPermissionMixin,
    UserQuerySetMixin,
    generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser, isStaffEditorPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance =  serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDeleteAPIView(
    StaffEditorPermissionMixin,
    UserQuerySetMixin,
    generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser, isStaffEditorPermission]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
       # instance
       super().perform_destroy(instance)


'''
Not gonna use this method
'''
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ProductMixinView(
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)

        # list view
        qs = Product.objects.all()
        data = ProductSerializer(qs, many=True).data
        return Response(data)

    if method == "POST":
        # create an item 
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # instance = serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response({'invalid':'Not good data'}, status=400)