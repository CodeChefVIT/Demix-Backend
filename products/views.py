from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from accounts.permissions import IsKalafexAdmin, IsArtist
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView, RetrieveUpdateDestroyAPIView
from .serializers import(
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    ParticularProductSerializer,
    ProductImageSerializer,
    ProductImageCreateSerializer
)
from .models import Category, SubCategory, Product, ProductImage
from .pagination import ResultSetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsKalafexAdmin]
    serializer_class = CategorySerializer
    parser_classes = [JSONParser]


class SubCategoryCreateView(CreateAPIView):
    queryset = SubCategory.objects.all()
    permission_classes = [IsAuthenticated, IsKalafexAdmin]
    serializer_class = SubCategorySerializer
    parser_classes = [JSONParser]


class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]

    def create(self, request, *args, **kwargs):
        #request.data['artist'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductImageCreateView(CreateAPIView):
    queryset = ProductImage.objects.all()
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ProductImageCreateSerializer
    parser_classes = [FormParser, MultiPartParser]


class CategoryUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    parser_classes = [JSONParser]
    lookup_url_kwarg = "category"

    def get_queryset(self):
        category = self.kwargs.get(self.lookup_url_kwarg)
        required_category_obj = Category.objects.filter(
            name=category
        )
        return required_category_obj


class SubCategoryUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategorySerializer
    parser_classes = [JSONParser]
    lookup_url_kwarg = "subcategory"

    def get_queryset(self):
        subcategory = self.kwargs.get(self.lookup_url_kwarg)
        required_subcategory_obj = SubCategory.objects.filter(
            name=subcategory
        )
        return required_subcategory_obj


class AllCategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    parser_classes = [JSONParser]


class AllSubCategoriesView(ListAPIView):
    serializer_class = SubCategorySerializer
    parser_classes = [JSONParser]
    lookup_url_kwarg = 'category'

    def get_queryset(self):
        category = self.kwargs.get(self.lookup_url_kwarg)
        subcategories = SubCategory.objects.filter(
            category=category
        )
        return subcategories


class PopularProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination


class ProductbyCategoryListView(ListAPIView):
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    lookup_url_kwarg = "category"

    def get_queryset(self):
        category = self.kwargs.get(self.lookup_url_kwarg)
        products = Product.objects.filter(
            category=category
        )#
        return products


class ProductbySubCategoryListView(ListAPIView):
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    lookup_url_kwarg = "subcategory"

    def get_queryset(self):
        subcategory = self.kwargs.get(self.lookup_url_kwarg)
        products = Product.objects.filter(
            subcategory=subcategory
        )
        return products


class ProductbyArtistListView(ListAPIView):
    serializer_class = ProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    lookup_url_kwarg = "artist"

    def get_queryset(self):
        artist = self.kwargs.get(self.lookup_url_kwarg)
        products = Product.objects.filter(
            artist=artist
        )
        return products


class ParticularProductView(ListAPIView):
    serializer_class = ParticularProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    lookup_url_kwarg = "pid"

    def get_queryset(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.filter(pid=pid)
        return product


class ParticularProductModifyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ParticularProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    lookup_url_kwarg = "pid"

    def get_queryset(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.filter(pid=pid)
        return product


class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    