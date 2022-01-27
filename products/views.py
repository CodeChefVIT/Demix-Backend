from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from accounts.permissions import IsDemixAdmin, IsArtist
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, \
    DestroyAPIView, RetrieveUpdateDestroyAPIView
from .serializers import(
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    ParticularProductSerializer,
    ProductsPerArtistSerializer,
    ProductImageSerializer,
    ProductImageCRUDSerializer,
    ReviewRatingSerializer,
    ReviewRatingCreateSerializer
)
from .models import Category, SubCategory, Product, ProductImage, ReviewRating
from .pagination import ResultSetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated, IsDemixAdmin]
    serializer_class = CategorySerializer
    parser_classes = [JSONParser]


class SubCategoryCreateView(CreateAPIView):
    queryset = SubCategory.objects.all()
    permission_classes = [IsAuthenticated, IsDemixAdmin]
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
    serializer_class = ProductImageCRUDSerializer
    parser_classes = [FormParser, MultiPartParser]


class ProductImageDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ProductImageCRUDSerializer
    parser_classes = [JSONParser]

    def delete(self, request, pi_id):
        user = request.user.id
        try:
            obj = ProductImage.objects.get(id=pi_id, product__artist=user)
            obj.delete()
            return Response({
                'status': 'success',
                'details': 'Successfully deleted product image.'
            }, status=200)
        except:
            return Response({
                'status': 'error',
                'details': 'Error in deleting product image.'
            }, status=400)


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
    serializer_class = ProductsPerArtistSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    lookup_url_kwarg = "artist"

    def get_queryset(self):
        artist = self.kwargs.get(self.lookup_url_kwarg)
        products = Product.objects.filter(
            artist=artist
        )
        return products


class ParticularProductView(RetrieveAPIView):
    serializer_class = ParticularProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    lookup_url_kwarg = "pid"

    def get_object(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.get(pid=pid)
        # Update click count
        product.click_count += 1
        product.save()
        return product


class ParticularProductModifyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ParticularProductSerializer
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination
    lookup_url_kwarg = "pid"

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        pid = self.kwargs.get(self.lookup_url_kwarg)
        product = Product.objects.filter(artist=user, pid=pid)
        return product


class ProductSearchView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description', 'category__name',
                     'category__description']
    parser_classes = [FormParser, MultiPartParser, JSONParser]
    pagination_class = ResultSetPagination


class ReviewRatingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewRatingSerializer
    parser_classes = [JSONParser]

    def get(self, request, pid):
        user = request.user.id
        try:
            obj = ReviewRating.objects.get(user=user, product=pid)
            serializer = ReviewRatingSerializer(obj)
            return Response({
                'status': 'success',
                'details': serializer.data
            }, status=200)
        except ReviewRating.DoesNotExist:
            return Response({
                'status': 'does not exist',
                'details': 'Rating and review does not exist for this product by this user.'
            }, status=400)

    def post(self, request, pid):
        user = request.user.id
        if ReviewRating.objects.filter(user=user, product=pid).exists():
            return Response({
                'status': 'error',
                'details': 'Rating and review already given for this product.'
            }, status=400)
        else:
            try:
                request.data['product'] = pid
                request.data['user'] = user
                serializer = ReviewRatingCreateSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': 'success',
                        'details': serializer.data
                    }, status=201)
                else:
                    return Response({
                        'status': 'error',
                        'details': serializer.errors
                    }, status=400)
            except:
                return Response({
                    'status': 'error',
                    'details': ''
                }, status=400)

    def delete(self, request, pid):
        user = request.user.id
        try:
            obj = ReviewRating.objects.get(user=user, product=pid)
            obj.delete()
            return Response({
                'status': 'success',
                'details': 'Successfully deleted review.'
            }, status=200)
        except:
            return Response({
                'status': 'error',
                'details': 'Error in deleting review.'
            }, status=400)


class NoAuthReviewRatingListView(ListAPIView):
    serializer_class = ReviewRatingSerializer
    parser_classes = [JSONParser]
    lookup_url_kwarg = 'pid'

    def get_queryset(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        reviewratings = ReviewRating.objects.filter(
            product=pid
        )
        return reviewratings

    def get_review_stats(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        user = self.request.user.id
        reviewratings = ReviewRating.objects.filter(
            product=pid
        )
        count = ReviewRating.objects.filter(
            product=pid
        ).count()
        average_rating = 0.0
        for review in reviewratings:
            if review.rating is not None:
                average_rating += review.rating
        average_rating /= count
        custom_dict = {
            'average_rating': round(average_rating, 2),
            'count': count 
        }
        return custom_dict

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        reviews_stats = self.get_review_stats()
        custom_response = {
            'results': serializer.data
        }
        custom_response.update(reviews_stats)
        return Response(custom_response)


class AuthReviewRatingListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewRatingSerializer
    parser_classes = [JSONParser]
    lookup_url_kwarg = 'pid'

    def get_queryset(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        user = self.request.user.id
        reviewratings = ReviewRating.objects.filter(
            product=pid
        ).exclude(user=user)
        return reviewratings
    
    def get_review_stats(self):
        pid = self.kwargs.get(self.lookup_url_kwarg)
        user = self.request.user.id
        reviewratings = ReviewRating.objects.filter(
            product=pid
        )
        count = ReviewRating.objects.filter(
            product=pid
        ).count()
        average_rating = 0.0
        for review in reviewratings:
            if review.rating is not None:
                average_rating += review.rating
        average_rating /= count
        custom_dict = {
            'average_rating': round(average_rating, 2),
            'count': count
        }
        return custom_dict

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        reviews_stats = self.get_review_stats()
        custom_response = {
            'results': serializer.data
        }
        custom_response.update(reviews_stats)
        return Response(custom_response)