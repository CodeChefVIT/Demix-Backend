from django.urls import path, include
from .views import(
    CategoryCreateView,
    SubCategoryCreateView,
    ProductCreateView,
    ProductImageCreateView,
    ProductImageDeleteView,
    CategoryUpdateDeleteView,
    SubCategoryUpdateDeleteView,
    PopularProductListView,
    ProductbyCategoryListView,
    ProductbySubCategoryListView,
    ProductbyArtistListView,
    ParticularProductView,
    ParticularProductModifyView,
    AllCategoriesView,
    AllSubCategoriesView,
    ProductSearchView,
    ReviewRatingView,
    NoAuthReviewRatingListView,
    AuthReviewRatingListView
)

urlpatterns = [
    path('create/product/', ProductCreateView.as_view()),
    path('create/product/add_image/', ProductImageCreateView.as_view()),
    path('delete/product/delete_image/<pi_id>/', ProductImageDeleteView.as_view()),
    path('create/category/', CategoryCreateView.as_view()),
    path('create/subcategory/', SubCategoryCreateView.as_view()),
    path('modify/category/<category>/', CategoryUpdateDeleteView.as_view()),
    path('modify/subcategory/<subcategory>/', SubCategoryUpdateDeleteView.as_view()),
    path('view/allcategories/', AllCategoriesView.as_view()),
    path('view/allsubcategories/<category>/', AllSubCategoriesView.as_view()),
    path('view/product/category/<category>/', ProductbyCategoryListView.as_view()),
    path('view/product/subcategory/<subcategory>/', ProductbySubCategoryListView.as_view()),
    path('view/product/artist/<artist>/', ProductbyArtistListView.as_view()),
    path('view/product/popular/', PopularProductListView.as_view()),
    path('view/product/<pid>/', ParticularProductView.as_view()),
    path('modify/product/<pid>/', ParticularProductModifyView.as_view()),
    path('search/product/', ProductSearchView.as_view()),
    path('review/<pid>/', ReviewRatingView.as_view()),
    path('reviews/noauth/<pid>/', NoAuthReviewRatingListView.as_view()),
    path('reviews/auth/<pid>/', AuthReviewRatingListView.as_view())
]
