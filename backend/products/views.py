from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

#from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer




# Create your views here.

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content')
        if content is None:
            content = title
        serializer.save(content=content)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'

'''
Not gonna use this method
'''
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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